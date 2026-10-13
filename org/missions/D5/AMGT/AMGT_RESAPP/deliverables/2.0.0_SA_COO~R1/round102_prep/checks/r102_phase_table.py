"""AMGT_RESAPP round-102 PREP -- the overlay's PER-PHASE TABLE for ONE request on the live function, from its own log lines (`AMGT-bi-2`'s driven request, graded by its criterion AC3).

  PYTHONPATH=<repo root> python r102_phase_table.py --request-id <id> | --id-file <file holding a line 'REQUEST_ID <id>'> [--hours 48]
  python r102_phase_table.py --lines-file <text file of log lines>      (a CONTROL: the same arms over saved lines, no AWS call)

READ-ONLY: ONE Logs Insights query over `/aws/lambda/opal-amgt-scoped-api` for that request id (its START, END, REPORT and application lines). Prints the REPORT line's handler time
(`Duration`, the number the 29 s limit applies to) and `Init Duration` (a cold container has one), then one row per `AMGT_PHASE route=overlay` phase with its milliseconds and its
share of the handler time, then the arms:
  T1  the request is an overlay request: all fourteen phases are present once each (identity, model_block, axis_reads, check_face, feed, description, research_coverage, posture, peers,
      provenance, top_band, input_provenance, read_security_overlay, serialize)
  T2  the container was cold: the REPORT line carries an Init Duration
  T3  the eleven inner phases sum to `read_security_overlay` within max(5 percent, 5 ms)
  T4  identity + read_security_overlay + serialize sum to the handler time within max(5 percent, 5 ms)
  T5  the handler time is stated (a number, not absent)
Verdict `R102 PHASE TABLE: YES` (T1 to T5), `R102 PHASE TABLE: WARM` (T1, T3, T4, T5 hold and the container was warm: the split is real but it is not a COLD request), else
`R102 PHASE TABLE: NO`. Exit 0 on YES. Writes nothing. A query that does not reach `Complete` is `NO`, never an empty table.
"""
import re
import sys
import time

import boto3

LG = "/aws/lambda/opal-amgt-scoped-api"
PHASES = ["identity", "model_block", "axis_reads", "check_face", "feed", "description", "research_coverage", "posture", "peers", "provenance", "top_band",
          "input_provenance", "read_security_overlay", "serialize"]
INNER = PHASES[1:12]
PHASE_LINE = re.compile(r"AMGT_PHASE route=overlay phase=(\S+) ms=(\d+)")


def within(a, b):
    return abs(a - b) <= max(0.05 * max(a, b), 5.0)


def main(argv):
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default

    rid = opt("--request-id")
    lines_file = opt("--lines-file")
    if lines_file:
        messages = [x.rstrip("\n") for x in open(lines_file, encoding="utf-8")]
        return report(messages, "lines-file")
    if rid is None and opt("--id-file"):
        for line in open(opt("--id-file"), encoding="utf-8"):
            m = re.match(r"\s*REQUEST_ID\s+([0-9a-fA-F-]{36})\s*$", line)
            if m:
                rid = m.group(1)
                break
    if not rid:
        print("R102 PHASE TABLE: NO (no request id)")
        return 1
    hours = int(opt("--hours", "48"))
    cw = boto3.client("logs", region_name="us-east-1")
    end = int(time.time())

    def run_query(text, start, stop):
        qid = cw.start_query(logGroupName=LG, startTime=start, endTime=stop, queryString=text, limit=1000)["queryId"]
        out = {}
        for _ in range(90):
            time.sleep(2)
            out = cw.get_query_results(queryId=qid)
            if out["status"] in ("Complete", "Failed", "Cancelled", "Timeout"):
                break
        rows = [{c["field"]: c["value"] for c in row if c["field"] != "@ptr"} for row in out.get("results", [])]
        return out.get("status"), rows

    # 1. the request's own tagged lines (START, END, REPORT): they carry the request id; they give the log stream and the time bounds.
    status, tagged = run_query('filter @requestId = "%s" | fields @timestamp, @logStream, @message | sort @timestamp asc | limit 50' % rid, end - hours * 3600, end + 60)
    print("request id %s | query status %s | tagged lines %d" % (rid, status, len(tagged)))
    if status != "Complete" or not tagged:
        print("R102 PHASE TABLE: NO (the request's own lines were not found)")
        return 1
    # `print` lines carry no request id in the text log format: they are the lines of the SAME log stream between START and REPORT.
    import datetime as dt

    def ts(row):
        return dt.datetime.strptime(row["@timestamp"][:23], "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=dt.timezone.utc)

    stamps = [ts(r) for r in tagged]
    t0 = int((min(stamps) - dt.timedelta(seconds=2)).timestamp())
    t1 = int((max(stamps) + dt.timedelta(seconds=2)).timestamp())
    stream = tagged[0]["@logStream"]
    status, rows = run_query('filter @logStream = "%s" | fields @timestamp, @message | sort @timestamp asc | limit 500' % stream, t0, t1)
    print("log stream %s | window %s to %s | status %s | lines %d" % (stream[-20:], min(stamps).strftime("%H:%M:%S"), max(stamps).strftime("%H:%M:%S"), status, len(rows)))
    if status != "Complete":
        print("R102 PHASE TABLE: NO (the stream query did not complete)")
        return 1
    messages = [r.get("@message", "") for r in rows]
    return report(messages, rid)


def report(messages, rid):
    report = next((m for m in messages if m.startswith("REPORT ")), "")
    dur = re.search(r"Duration: ([0-9.]+) ms", report)
    init = re.search(r"Init Duration: ([0-9.]+) ms", report)
    handler_ms = float(dur.group(1)) if dur else None
    print("REPORT: handler %s ms | init %s" % (("%.2f" % handler_ms) if handler_ms is not None else "ABSENT", ("%s ms" % init.group(1)) if init else "none (warm container)"))
    seen = {}
    names = []
    for m in messages:
        pm = PHASE_LINE.search(m)
        if pm:
            names.append(pm.group(1))
            seen[pm.group(1)] = int(pm.group(2))
    for n in PHASES:
        if n in seen:
            share = ("%.1f%%" % (100.0 * seen[n] / handler_ms)) if handler_ms else "?"
            print("PHASE %-24s %7d ms  %s of the handler time" % (n, seen[n], share))
    t1 = sorted(names) == sorted(PHASES)
    t2 = init is not None
    t5 = handler_ms is not None
    t3 = t4 = False
    if t1:
        inner = sum(seen[n] for n in INNER)
        outer = seen["identity"] + seen["read_security_overlay"] + seen["serialize"]
        t3 = within(inner, seen["read_security_overlay"])
        print("   inner phases %d ms against read_security_overlay %d ms" % (inner, seen["read_security_overlay"]))
        if t5:
            t4 = within(outer, handler_ms)
            print("   outer phases %d ms against handler time %.2f ms (unaccounted %.2f ms)" % (outer, handler_ms, handler_ms - outer))
    for name, ok in (("T1 all fourteen phases once each", t1), ("T2 cold container", t2), ("T3 inner sum", t3), ("T4 outer sum", t4), ("T5 handler time stated", t5)):
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    if t1 and t2 and t3 and t4 and t5:
        verdict = "YES"
    elif t1 and not t2 and t3 and t4 and t5:
        verdict = "WARM"
    else:
        verdict = "NO"
    print("R102 PHASE TABLE: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
