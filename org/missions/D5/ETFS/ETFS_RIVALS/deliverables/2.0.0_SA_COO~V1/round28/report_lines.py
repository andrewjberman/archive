"""Print the REPORT lines (and any timeout / unhandled error) of the five rivalfunds Lambdas in a UTC window.

    python report_lines.py <start ISO, e.g. 2026-10-09T10:55> <end ISO>

For ledger etfs-rivalfunds-r27 L2 and the aw-1 apply's condition (b) (read independently of the applier). Read-only: one
CloudWatch Logs filter per function. A function with no REPORT line in the window prints `NO REPORT LINE`, never silence.
"""
import datetime as dt
import sys

FUNCS = ["etfs-rivalfunds-daily-lambda", "etfs-rivalfunds-fetch-holdings-lambda", "rivalfunds-build-silver-lambda",
         "rivalfunds-build-canonical-shape-lambda", "rivalfunds-publish-page-lambda"]
LIMIT_MS = 720_000


def ms(iso):
    return int(dt.datetime.fromisoformat(iso).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)


def events(fn, pattern, start, end):
    """All matching messages of one log group in the window (paginated), or (None, error)."""
    import boto3
    try:
        logs = boto3.client("logs", region_name="us-east-1")
        out, kw = [], {"logGroupName": f"/aws/lambda/{fn}", "startTime": start, "endTime": end, "filterPattern": pattern}
        while True:
            r = logs.filter_log_events(**kw)
            out += [e["message"].strip() for e in r.get("events", [])]
            if not r.get("nextToken"):
                return out, None
            kw["nextToken"] = r["nextToken"]
    except Exception as e:  # noqa: BLE001 -- a failed read is printed as READ FAILED, never as no lines
        return None, f"{type(e).__name__}: {e}"


start, end = ms(sys.argv[1]), ms(sys.argv[2])
blocking = 0
for fn in FUNCS:
    rep, err = events(fn, "REPORT", start, end)
    bad, _ = events(fn, '?"Task timed out" ?"Status: timeout" ?"[ERROR]"', start, end)
    if err:
        print(f"{fn}: READ FAILED {err}")
        blocking += 1
        continue
    if not rep:
        print(f"{fn}: NO REPORT LINE in the window")
    for line in rep:
        dur = float(line.split("Duration: ")[1].split(" ms")[0]) if "Duration: " in line else 0.0
        flag = "  <-- OVER 720 s (BLOCKING)" if dur > LIMIT_MS else ""
        blocking += bool(flag)
        print(f"{fn}: {line}{flag}")
    for line in bad or []:
        blocking += 1
        print(f"{fn}: ERROR LINE {line[:200]}")
print(f"RESULT: {blocking} blocking finding(s) across {len(FUNCS)} functions")
