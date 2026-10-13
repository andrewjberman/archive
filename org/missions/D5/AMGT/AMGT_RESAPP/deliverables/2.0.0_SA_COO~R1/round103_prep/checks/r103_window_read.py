"""AMGT_RESAPP round-103 PREP -- the overlay's handler time over a DECLARED WINDOW, from the function's own log lines (`AMGT-bj-3`).

  PYTHONPATH=<repo root> python r103_window_read.py --window "<label>,<start UTC ISO>,<end UTC ISO>" [--window "<label>,<start>,<end>" ...] [--slow-ms 4000]
  PYTHONPATH=<repo root> python r103_window_read.py --auto-split <start UTC ISO> [--slow-ms 4000]
      reads the function's `LastModified` (the last apply) and declares TWO windows: `before` = <start> .. LastModified and `after` = LastModified .. now.

READ-ONLY: Logs Insights over `/aws/lambda/opal-amgt-scoped-api`, per window: (1) the overlay requests, one per `AMGT_PHASE route=overlay phase=read_security_overlay ms=<n>` line (the round-102
phase lines; a window that starts before 2026-10-13T16:17:06Z, the apply that carried them, has none and says so); (2) the function's REPORT lines (invocations, those with an Init Duration).
Prints, per window, ONE line: the window's label, its start and end in UTC, the trading days the window touches (`lib.trading_calendar`, the basis), the overlay count (the DENOMINATOR),
the median and 95th percentile of the overlay's `read_security_overlay` milliseconds, the maximum, how many are over `--slow-ms` (default 4000: the first overlay on a container) and what
share they are, the function's REPORT count and how many carry an Init Duration. A query that does not reach `Complete` is `NOT READ`, never a zero. The overlay's handler time is the
`read_security_overlay` phase plus about 3 ms outside it (round 102: 20,338 of 20,566 ms was identity 223 + read_security_overlay 20,338 + serialize 2 + 3).
Verdict `R103 WINDOW READ: <n> window(s) read, <m> not read`. Exit 0 when every window was read. Writes nothing.
"""
import datetime as dt
import sys
import time

import boto3

LG = "/aws/lambda/opal-amgt-scoped-api"


def parse_window(text):
    label, start, end = [x.strip() for x in text.split(",")]
    s = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    e = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return label, s, e


def query(cw, text, start, end):
    qid = cw.start_query(logGroupName=LG, startTime=int(start.timestamp()), endTime=int(end.timestamp()), queryString=text, limit=1000)["queryId"]
    out = {}
    for _ in range(120):
        time.sleep(2)
        out = cw.get_query_results(queryId=qid)
        if out["status"] in ("Complete", "Failed", "Cancelled", "Timeout"):
            break
    rows = [{c["field"]: c["value"] for c in row if c["field"] != "@ptr"} for row in out.get("results", [])]
    return out.get("status"), rows


def trading_days(start, end):
    try:
        import lib.trading_calendar as tc

        days = []
        d = start.date()
        while d <= end.date():
            if tc.is_trading_day(d):
                days.append(d.isoformat())
            d += dt.timedelta(days=1)
        return days
    except Exception as err:  # noqa: BLE001
        return ["calendar unavailable (%s)" % type(err).__name__]


def main(argv):
    windows = [parse_window(argv[i + 1]) for i, a in enumerate(argv) if a == "--window"]
    if "--auto-split" in argv:
        first = dt.datetime.strptime(argv[argv.index("--auto-split") + 1], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")
        applied = dt.datetime.strptime(cfg["LastModified"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
        print("function CodeSha256 %s | LastModified %s" % (cfg.get("CodeSha256"), cfg["LastModified"]))
        windows = [("before", first, applied), ("after", applied, dt.datetime.now(dt.timezone.utc).replace(microsecond=0))]
    slow = int(argv[argv.index("--slow-ms") + 1]) if "--slow-ms" in argv else 4000
    if not windows:
        print(__doc__)
        return 2
    cw = boto3.client("logs", region_name="us-east-1")
    read = 0
    unread = 0
    for label, start, end in windows:
        days = trading_days(start, end)
        q1 = ('filter @message like /AMGT_PHASE route=overlay phase=read_security_overlay/ | parse @message /ms=(?<ms>[0-9]+)/ '
              '| stats count(*) as n, pct(ms, 50) as p50, pct(ms, 95) as p95, max(ms) as mx, sum(ms > %d) as slow' % slow)
        q2 = 'filter @type = "REPORT" | stats count(*) as n, sum(@initDuration > 0) as init'
        s1, r1 = query(cw, q1, start, end)
        s2, r2 = query(cw, q2, start, end)
        head = "WINDOW %s | %s .. %s UTC | trading days %s" % (label, start.strftime("%Y-%m-%dT%H:%MZ"), end.strftime("%Y-%m-%dT%H:%MZ"), days)
        if s1 != "Complete" or s2 != "Complete":
            unread += 1
            print("%s | NOT READ (overlay query %s, report query %s)" % (head, s1, s2))
            continue
        read += 1
        o = r1[0] if r1 else {}
        r = r2[0] if r2 else {}
        n = int(float(o.get("n", 0) or 0))
        rn = int(float(r.get("n", 0) or 0))
        rin = int(float(r.get("init", 0) or 0))
        if n == 0:
            print("%s | overlays 0 (the denominator is zero: no overlay phase line in this window) | REPORT %d, with Init %d" % (head, rn, rin))
            continue
        slow_n = int(float(o.get("slow", 0) or 0))
        print("%s | overlays %d | median %.0f ms | p95 %.0f ms | max %.0f ms | over %d ms: %d (%.1f percent) | REPORT %d, with Init %d" % (
            head, n, float(o.get("p50", 0)), float(o.get("p95", 0)), float(o.get("mx", 0)), slow, slow_n, 100.0 * slow_n / n, rn, rin))
    print("R103 WINDOW READ: %d window(s) read, %d not read" % (read, unread))
    return 0 if unread == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
