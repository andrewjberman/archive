"""Read-only DRY derivation of every landed Cottonwood gold day from the claim floor with the CURRENT adapter (the late-posting reader of DB-b-333), compared with the landed gold day
(IRPT_DASHBD round 150, issuer 2.0.0_SA_COO~D2). It mirrors `run_day` without a write: presence_hold, derive over the previous trading day to the day with the floor day, keep the day's rows.
Per day it prints COUNTS only: rows new/old, NOT_MEASURABLE rows new/old, the sum of absolute external flows new/old, and the largest |external_flow| over market value new/old.
No account id, name or value row is printed or kept. Usage: python -I <this file> --out <json path> [--floor 2026-07-10]
"""
import datetime
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
sys.path.insert(0, str(ROOT / "lib"))
import boto3  # noqa: E402
import cottonwood_bd_account_return_daily as cbd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import trading_calendar as tc  # noqa: E402

FLOOR_DAY = "2026-07-10"


def stats(rows_flow_mv_quality):
    n, nm, tot, worst = 0, 0, 0.0, 0.0
    for flow, mv, quality in rows_flow_mv_quality:
        n += 1
        nm += 1 if quality == "NOT_MEASURABLE" else 0
        if flow:
            tot += abs(flow)
            if mv:
                worst = max(worst, abs(flow) / abs(mv))
    return {"rows": n, "not_measurable": nm, "abs_flow_sum": round(tot, 2), "max_flow_over_value": round(worst, 4)}


def landed(s3):
    bucket, prefix = cbd.gold_prefix()
    out, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        for cp in page.get("CommonPrefixes", []):
            tail = cp["Prefix"][len(prefix):].strip("/")
            if tail.startswith("date=") and tail[len("date="):] >= FLOOR_DAY:
                out.append(tail[len("date="):])
        if not page.get("IsTruncated"):
            return sorted(out)
        token = page["NextContinuationToken"]


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    reader = cbd.CottonwoodBlackDiamondSilverReader(s3)
    bucket, prefix = cbd.gold_prefix()
    days = landed(s3)
    out = {"claim": "measured", "floor": FLOOR_DAY, "denominator": {"landed_days": len(days)}, "days": {}}
    for day in days:
        row = {}
        old = pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read())).to_pydict()
        row["old"] = stats(zip(old["external_flow"], old["market_value_eod"], old["day_quality"]))
        hold = cbd.presence_hold(reader, day)
        if hold is not None:
            row["held"] = hold[:80]
            out["days"][day] = row
            continue
        prev = tc.prev_trading_day(datetime.date.fromisoformat(day)).isoformat()
        rows, _summary = cbd.derive(reader, cbd.accounts_in_partition(reader, day), prev, day, floor_day=FLOOR_DAY)
        rows = [r for r in rows if r["business_date"] == day]
        row["new"] = stats((r["external_flow"], r["market_value_eod"], r["day_quality"]) for r in rows)
        out["days"][day] = row
        print(day, row["old"]["rows"], row["new"]["rows"], row["old"]["abs_flow_sum"], row["new"]["abs_flow_sum"], flush=True)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("done", len(out["days"]))


if __name__ == "__main__":
    main()
