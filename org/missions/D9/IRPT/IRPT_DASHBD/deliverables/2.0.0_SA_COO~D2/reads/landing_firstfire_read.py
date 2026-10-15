"""IRPT_DASHBD Cottonwood landing, the read of the FIRST SCHEDULED FIRE (issuer 2.0.0_SA_COO~D2; CTO ROUND-128 ANALYSIS ADDENDUM 1 @143709c44f, term 3): exactly one new dated partition, history
unmodified, one value-level spot read of the new day against the source. (The fourth term, the report-build function's next build loading the table, waits for that function.) READ ONLY: S3 LIST
and GET, CloudWatch Logs filter, the local re-derivation of the reference; prints COUNTS and verdict words only.

Usage: python landing_firstfire_read.py <repo_root> <apply_finished_utc> [<since_iso_utc>]
       apply_finished_utc: the enable apply's `apply_finished_utc` from the AE record (keys of days up to 2026-10-14 must not be modified after it)
       since_iso_utc: the fire's cut (default the apply time)

VERDICTS: NEW_PARTITIONS (count and dates after 2026-10-14; the ruling reads exactly one), HISTORY (3,325 history partitions and the 65 landed days unmodified since the apply), REPORT lines of the
fire (memory, duration), NON_TRADING_DAY (a partition for a non-trading day is a STOP), VALUE_SPOT_READ (the new day against a local re-derivation under a different pyarrow: rows, key set, float values
within 1e-12, and the 14.0.2 load).
"""
import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

FUNCTION = "irpt-cot-account-return-daily-lambda"
LOG_GROUP = "/aws/lambda/" + FUNCTION
GOLD_BUCKET, GOLD_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/"
LAST_CATCHUP_DAY, HISTORY_COUNT = "2026-10-14", 3325
LOADER = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/2.0.0_SA_COO~D2/venv14/Scripts/python.exe"


def main(root, apply_finished, since):
    root = Path(root)
    sys.path.insert(0, str(root))
    import boto3
    from lib import trading_calendar as tc
    s3, logs = boto3.client("s3"), boto3.client("logs", region_name="us-east-1")
    by_day, tok = {}, None
    while True:
        kw = {"Bucket": GOLD_BUCKET, "Prefix": GOLD_PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            by_day.setdefault(o["Key"][len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15], []).append((o["Key"], o["LastModified"]))
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    new_days = sorted(d for d in by_day if d > LAST_CATCHUP_DAY)
    hist = [d for d in by_day if d <= "2026-06-22"]
    touched = [k for d, items in by_day.items() if d <= LAST_CATCHUP_DAY for k, t in items if t.strftime("%Y-%m-%dT%H:%M:%SZ") >= apply_finished]
    print("NEW_PARTITIONS:", len(new_days), new_days, "(the ruling reads exactly one)")
    print("HISTORY: %d history partitions (expect %d); keys of days up to %s modified after the apply: %d" % (len(hist), HISTORY_COUNT, LAST_CATCHUP_DAY, len(touched)))
    for d in new_days:
        objs = sorted(k.rsplit("/", 1)[1] for k, _ in by_day[d])
        trading = tc.is_trading_day(dt.date.fromisoformat(d))
        print("  %s objects %s trading_day %s %s" % (d, objs, trading, "" if trading else "STOP: a partition for a non-trading day"))
    start_ms = int(dt.datetime.fromisoformat(since.replace("Z", "+00:00")).timestamp() * 1000)
    reports, tk = [], None
    for _ in range(100):
        kw = {"logGroupName": LOG_GROUP, "filterPattern": "REPORT", "startTime": start_ms}
        if tk:
            kw["nextToken"] = tk
        r = logs.filter_log_events(**kw)
        for ev in r.get("events", []):
            m = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
            if m:
                reports.append((ev["timestamp"], float(m.group(1)), int(m.group(3))))
        tk = r.get("nextToken")
        if not tk:
            break
    for ts, dur, mx in sorted(reports):
        print("  REPORT %s duration %.1f s Max Memory Used %d MB" % (dt.datetime.fromtimestamp(ts / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"), dur / 1000, mx))
    if new_days:
        spec = importlib.util.spec_from_file_location("p132", str(root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r132/p132_value.py"))
        p132 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(p132)
        for d in new_days:
            f = p132.fresh(root, LOADER, d)
            ok = f["rows_equal"] and f["key_set_equal"] and f["non_float_mismatches"] == 0 and f["max_abs_diff"] <= 1e-12 and f["loader"]["rows"] == f["landed"]["rows"]
            print("VALUE_SPOT_READ %s: landed rows %d (written by %s), reference rows %d (pyarrow %s), key set equal %s, %d float values max diff %g, non-float mismatches %d, 14.0.2 load rows %s -> %s" %
                  (d, f["landed"]["rows"], f["landed"]["created_by"], f["reference"]["rows"], f["reference"]["pyarrow_version"], f["key_set_equal"], f["values_compared"], f["max_abs_diff"],
                   f["non_float_mismatches"], f["loader"]["rows"], "PASS" if ok else "FAIL"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.argv[2])
