"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY reader of the 49 Financial reporting-gold function's scheduled fire (ledger leg L7; the CTO's msg 10141 and round-138 ruling 2a).

  python <this file> [YYYY-MM-DD]      default: the newest weekday on or before today (UTC); run from the repository root; GET requests only

For the fire day it prints, for EVERY invocation of `irpt-49f-reporting-gold-lambda` between 11:30Z and 12:45Z: the REPORT line's start, duration and Max Memory Used (the DENOMINATOR is the number of
invocations printed), the log lines `transaction rows=` and `TRANSACTION_SKIPPED` counted (day and counts only), any `Task timed out` / `Traceback` / `AccessDenied` line counted, and the verdict:
PASS when no invocation timed out, every duration is under 720 s and every peak is under 80 percent of 8,192 MB (6,553 MB). A roll-back is the CTO's word and the applier's act: this tool decides nothing.
No client value is read: only REPORT lines and the stage's own line shapes are matched, and only counts are printed.
"""
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
AWS = str(ROOT / ".tools" / "aws.cmd")
LG = "/aws/lambda/irpt-49f-reporting-gold-lambda"
LIMIT_S = 720.0
PEAK_LIMIT_MB = 6553
REPORT = re.compile(r"REPORT RequestId: (\S+)\s+Duration: ([\d.]+) ms.*?Max Memory Used: (\d+) MB")


def parse_report(message):
    """(request_id, duration_s, max_memory_mb) or None."""
    m = REPORT.search(message)
    return (m.group(1), float(m.group(2)) / 1000.0, int(m.group(3))) if m else None


def classify(message):
    """The stage's own line shapes, by name only."""
    if "TRANSACTION_SKIPPED" in message:
        return "transaction_skipped"
    if re.search(r"\btransaction rows=\d+", message):
        return "transaction_rows"
    if "Task timed out" in message:
        return "timeout"
    if "FILLED_CATCHUP_LIST_FAILED" in message:
        return "filled_catchup_denied"
    if "Traceback" in message or "AccessDenied" in message:
        return "error"
    return None


def verdict(invocations, counts):
    if not invocations:
        return "NO FIRE FOUND"
    bad = [i for i in invocations if i["duration_s"] >= LIMIT_S or i["max_memory_mb"] >= PEAK_LIMIT_MB]
    if counts.get("timeout") or bad:
        return "OVER THE LIMIT (a timeout, or an invocation at or over %d s or %d MB): the rollback is the CTO's word" % (LIMIT_S, PEAK_LIMIT_MB)
    return "PASS (no timeout; every duration under %d s; every peak under %d MB)" % (LIMIT_S, PEAK_LIMIT_MB)


def events(day):
    start = dt.datetime.strptime(day + " 11:30", "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(minutes=75)
    out, token = [], None
    while True:
        cmd = [AWS, "logs", "filter-log-events", "--log-group-name", LG, "--start-time", str(int(start.timestamp() * 1000)), "--end-time", str(int(end.timestamp() * 1000)), "--output", "json"]
        if token:
            cmd += ["--next-token", token]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            raise SystemExit("logs read failed: " + (r.stderr or r.stdout)[-200:])
        d = json.loads(r.stdout or "{}")
        out += d.get("events", [])
        token = d.get("nextToken")
        if not token:
            return out


def main(argv):
    if len(argv) > 1:
        day = argv[1]
    else:
        d = dt.datetime.now(dt.timezone.utc).date()
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
        day = d.isoformat()
    ev = events(day)
    invocations, counts = [], {}
    for e in ev:
        msg = e.get("message", "")
        rp = parse_report(msg)
        if rp:
            t = dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc).strftime("%H:%M:%SZ")
            invocations.append({"at": t, "request_id": rp[0][:8], "duration_s": rp[1], "max_memory_mb": rp[2]})
            continue
        k = classify(msg)
        if k:
            counts[k] = counts.get(k, 0) + 1
    print("fire day %s, log events scanned: %d (11:30Z to 12:45Z), invocations (REPORT lines): %d" % (day, len(ev), len(invocations)))
    for i in sorted(invocations, key=lambda x: x["at"]):
        print("  %s  request %s  duration %.1f s  peak %d MB" % (i["at"], i["request_id"], i["duration_s"], i["max_memory_mb"]))
    if invocations:
        print("  total duration over %d invocations: %.1f s; longest %.1f s; highest peak %d MB" % (len(invocations), sum(i["duration_s"] for i in invocations),
                                                                                                  max(i["duration_s"] for i in invocations), max(i["max_memory_mb"] for i in invocations)))
    print("  stage lines: transaction rows= %d, TRANSACTION_SKIPPED %d, timeouts %d, other error-class lines %d" % (counts.get("transaction_rows", 0), counts.get("transaction_skipped", 0), counts.get("timeout", 0), counts.get("error", 0)))
    print("  pre-existing, NOT the transaction stage (row IRPT_DASHBD-D2-S135): FILLED_CATCHUP_LIST_FAILED lines %d" % counts.get("filled_catchup_denied", 0))
    print("VERDICT: " + verdict(invocations, counts))
    return 0


def selftest():
    bad = 0
    msgs = [("REPORT RequestId: abcd1234-ef Duration: 298214.13 ms Billed Duration: 298215 ms Memory Size: 8192 MB Max Memory Used: 1455 MB", ("abcd1234-ef", 298.21413, 1455)),
            ("START RequestId: x", None)]
    for m, want in msgs:
        got = parse_report(m)
        if got != want:
            bad += 1
            print("SELFTEST FAIL parse %r: got %r want %r" % (m[:30], got, want))
    for m, want in (("2026-10-16 transaction rows=8512 LANDED", "transaction_rows"), ("TRANSACTION_SKIPPED 2026-10-16 ValueError: x", "transaction_skipped"),
                    ("Task timed out after 900.00 seconds", "timeout"), ("botocore AccessDenied", "error"), ("FILLED_CATCHUP_LIST_FAILED AccessDenied: x", "filled_catchup_denied"), ("ordinary line", None)):
        if classify(m) != want:
            bad += 1
            print("SELFTEST FAIL classify %r" % m)
    ok = [{"duration_s": 300.0, "max_memory_mb": 1500}]
    if not verdict(ok, {}).startswith("PASS"):
        bad += 1
        print("SELFTEST FAIL verdict pass")
    if not verdict([{"duration_s": 800.0, "max_memory_mb": 1500}], {}).startswith("OVER"):
        bad += 1
        print("SELFTEST FAIL verdict over duration")
    if not verdict(ok, {"timeout": 1}).startswith("OVER"):
        bad += 1
        print("SELFTEST FAIL verdict timeout")
    if not verdict([{"duration_s": 100.0, "max_memory_mb": 7000}], {}).startswith("OVER"):
        bad += 1
        print("SELFTEST FAIL verdict memory")
    if verdict([], {}) != "NO FIRE FOUND":
        bad += 1
        print("SELFTEST FAIL verdict empty")
    print("selftest %s" % ("FAIL" if bad else "PASS (12 arms)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if len(sys.argv) == 2 and sys.argv[1] == "--selftest" else main(sys.argv))
