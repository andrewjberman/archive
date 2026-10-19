"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY reader of the Cottonwood landing function's scheduled fire (packet REVISION 2, Act 6 / ledger leg L8; the CTO's msgs 10875 and 10892).

  python <this file> [YYYY-MM-DD]      default: the newest weekday on or before today (UTC); run from the repository root; GET, LIST and log reads only

For the fire day it prints, for EVERY invocation of `irpt-cot-account-return-daily-lambda` between 12:00Z and 13:30Z (the schedule is cron(15 8 ? * MON-FRI *) New York, 12:15Z in October): the REPORT
line's start, duration and Max Memory Used (the DENOMINATOR is the number of invocations printed); the stage's own lines counted by name (OWED, OWED_TRANSACTION, `transaction rows=`,
TRANSACTION_SKIPPED, SETTLE_FAILED, HOLD, timeouts, other error-class lines); and what the fire WROTE, read from S3 (the settle step's result is not in the logs): the keys under the returns prefix
and the transaction prefix whose version was written in the window, by day, with how many are NEW keys and how many OVERWRITE a landed key (a key with an earlier version). Days and counts only.
The verdict: PASS when there is at least one invocation, no timeout, no SETTLE_FAILED or TRANSACTION_SKIPPED line, every duration under 720 s and every peak under 819 MB (80 percent of 900 s and 1,024 MB).
A roll-back is the CTO's word and the applier's act: this tool decides nothing. No client value is read.
"""
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
AWS = str(ROOT / ".tools" / "aws.cmd")
LG = "/aws/lambda/irpt-cot-account-return-daily-lambda"
BUCKET = "opal-data-cottonwood"
RETURNS = "irpt/cottonwood/gold/account_return_daily/"
TX = "irpt/cottonwood/gold/account_transaction/"
LIMIT_S = 720.0
PEAK_LIMIT_MB = 819
START_HHMM, WINDOW_MIN = "12:00", 90
REPORT = re.compile(r"REPORT RequestId: (\S+)\s+Duration: ([\d.]+) ms.*?Max Memory Used: (\d+) MB")
DAY_KEY = re.compile(r"date=(\d{4}-\d{2}-\d{2})/")


def parse_report(message):
    """(request_id, duration_s, max_memory_mb) or None."""
    m = REPORT.search(message)
    return (m.group(1), float(m.group(2)) / 1000.0, int(m.group(3))) if m else None


def classify(message):
    """The stage's own line shapes, by name only."""
    if "SETTLE_FAILED" in message:
        return "settle_failed"
    if "TRANSACTION_SKIPPED" in message:
        return "transaction_skipped"
    if "OWED_TRANSACTION" in message:
        return "owed_transaction"
    if re.search(r"(^|\s)OWED:", message):
        return "owed"
    if re.search(r"\btransaction rows=\d+", message):
        return "transaction_rows"
    if re.search(r"(^|\s)HOLD \d{4}-\d{2}-\d{2}", message):
        return "hold"
    if "Task timed out" in message:
        return "timeout"
    if "Traceback" in message or "AccessDenied" in message:
        return "error"
    return None


def verdict(invocations, counts):
    if not invocations:
        return "NO FIRE FOUND"
    bad = [i for i in invocations if i["duration_s"] >= LIMIT_S or i["max_memory_mb"] >= PEAK_LIMIT_MB]
    if counts.get("timeout") or bad:
        return "OVER THE LIMIT (a timeout, or an invocation at or over %d s or %d MB): the rollback is the CTO's word" % (LIMIT_S, PEAK_LIMIT_MB)
    if counts.get("settle_failed") or counts.get("transaction_skipped"):
        return "READ THE LINES (a SETTLE_FAILED or TRANSACTION_SKIPPED line is present; neither stops the returns, each is named)"
    return "PASS (no timeout; every duration under %d s; every peak under %d MB; no settle or transaction failure line)" % (LIMIT_S, PEAK_LIMIT_MB)


def aws_json(args):
    r = subprocess.run([AWS] + args + ["--output", "json"], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise SystemExit("aws read failed: " + (r.stderr or r.stdout)[-200:])
    return json.loads(r.stdout or "{}")


def log_events(day):
    start = dt.datetime.strptime(day + " " + START_HHMM, "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(minutes=WINDOW_MIN)
    out, token = [], None
    while True:
        cmd = ["logs", "filter-log-events", "--log-group-name", LG, "--start-time", str(int(start.timestamp() * 1000)), "--end-time", str(int(end.timestamp() * 1000))]
        if token:
            cmd += ["--next-token", token]
        d = aws_json(cmd)
        out += d.get("events", [])
        token = d.get("nextToken")
        if not token:
            return out, start, end


def written_in_window(prefix, start, end):
    """({day: [new, overwrite]}, keys_listed): the version rows under prefix written in [start, end]; overwrite when the key has an older version."""
    versions, token = {}, None
    while True:
        cmd = ["s3api", "list-object-versions", "--bucket", BUCKET, "--prefix", prefix, "--max-items", "1000"]
        if token:
            cmd += ["--starting-token", token]
        d = aws_json(cmd)
        for v in d.get("Versions", []):
            versions.setdefault(v["Key"], []).append(dt.datetime.strptime(v["LastModified"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc))
        token = d.get("NextToken")
        if not token:
            break
    by_day = {}
    for key, times in versions.items():
        m = DAY_KEY.search(key)
        inwin = [t for t in times if start <= t <= end]
        if not m or not inwin:
            continue
        older = [t for t in times if t < start]
        cell = by_day.setdefault(m.group(1), [0, 0])
        cell[1 if older else 0] += 1
    return by_day, len(versions)


def main(argv):
    if len(argv) > 1:
        day = argv[1]
    else:
        d = dt.datetime.now(dt.timezone.utc).date()
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
        day = d.isoformat()
    ev, start, end = log_events(day)
    invocations, counts, lines = [], {}, []
    for e in ev:
        msg = e.get("message", "").strip()
        rp = parse_report(msg)
        if rp:
            t = dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc).strftime("%H:%M:%SZ")
            invocations.append({"at": t, "request_id": rp[0][:8], "duration_s": rp[1], "max_memory_mb": rp[2]})
            continue
        k = classify(msg)
        if k:
            counts[k] = counts.get(k, 0) + 1
            if k in ("owed", "owed_transaction"):
                lines.append(msg[:200])
    print("fire day %s, log events scanned: %d (%sZ to %s), invocations (REPORT lines): %d" % (day, len(ev), START_HHMM, end.strftime("%H:%MZ"), len(invocations)))
    for i in sorted(invocations, key=lambda x: x["at"]):
        print("  %s  request %s  duration %.1f s  peak %d MB" % (i["at"], i["request_id"], i["duration_s"], i["max_memory_mb"]))
    for ln in lines:
        print("  " + ln)
    print("  stage lines: transaction rows= %d, TRANSACTION_SKIPPED %d, SETTLE_FAILED %d, HOLD %d, timeouts %d, other error-class lines %d"
          % (counts.get("transaction_rows", 0), counts.get("transaction_skipped", 0), counts.get("settle_failed", 0), counts.get("hold", 0), counts.get("timeout", 0), counts.get("error", 0)))
    for label, prefix in (("returns", RETURNS), ("transaction", TX)):
        by_day, listed = written_in_window(prefix, start, end)
        new = sum(c[0] for c in by_day.values())
        over = sum(c[1] for c in by_day.values())
        print("  %s prefix (%d keys listed): written in the window: %d new key(s), %d overwrite(s) of a landed key, over %d day(s): %s"
              % (label, listed, new, over, len(by_day), ", ".join("%s(+%d/~%d)" % (d, c[0], c[1]) for d, c in sorted(by_day.items()))[:400] or "none"))
    print("VERDICT: " + verdict(invocations, counts))
    return 0


def selftest():
    bad = 0
    p = parse_report("REPORT RequestId: abcd1234-ef Duration: 298214.13 ms Billed Duration: 298215 ms Memory Size: 1024 MB Max Memory Used: 455 MB")
    if p != ("abcd1234-ef", 298.21413, 455):
        bad += 1
        print("SELFTEST FAIL parse: %r" % (p,))
    if parse_report("START RequestId: x") is not None:
        bad += 1
        print("SELFTEST FAIL parse non-report")
    cases = [("OWED: newest landed 2026-10-16, today 2026-10-20, days ['2026-10-19']", "owed"), ("OWED_TRANSACTION: newest writable 2026-09-29, days ['2026-09-29']", "owed_transaction"),
             ("  2026-09-29 transaction rows=8512 LANDED", "transaction_rows"), ("  TRANSACTION_SKIPPED 2026-09-30 window incomplete", "transaction_skipped"),
             ("SETTLE_FAILED 2026-10-01 ValueError: x", "settle_failed"), ("HOLD 2026-10-19: fact_allocations partition absent", "hold"),
             ("Task timed out after 900.00 seconds", "timeout"), ("botocore AccessDenied", "error"), ("ordinary line", None)]
    for m, want in cases:
        if classify(m) != want:
            bad += 1
            print("SELFTEST FAIL classify %r -> %r (want %r)" % (m[:30], classify(m), want))
    ok = [{"duration_s": 300.0, "max_memory_mb": 500}]
    for inv, cnt, want in ((ok, {}, "PASS"), ([{"duration_s": 800.0, "max_memory_mb": 500}], {}, "OVER"), (ok, {"timeout": 1}, "OVER"), ([{"duration_s": 100.0, "max_memory_mb": 900}], {}, "OVER"),
                           (ok, {"settle_failed": 1}, "READ"), (ok, {"transaction_skipped": 2}, "READ"), ([], {}, "NO FIRE FOUND")):
        if not verdict(inv, cnt).startswith(want):
            bad += 1
            print("SELFTEST FAIL verdict %r %r" % (cnt, want))
    if DAY_KEY.search("irpt/cottonwood/gold/account_return_daily/date=2026-10-16/data.parquet").group(1) != "2026-10-16":
        bad += 1
        print("SELFTEST FAIL day key")
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % (2 + len(cases) + 7 + 1)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if len(sys.argv) == 2 and sys.argv[1] == "--selftest" else main(sys.argv))
