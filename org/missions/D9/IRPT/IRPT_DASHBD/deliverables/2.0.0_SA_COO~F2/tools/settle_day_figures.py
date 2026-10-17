"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY settle-day figures the CTO's REVISION 2 condition asks Act 3(b) to print.

  python <this file> <day> [<day> ...]        run from the repository root of the release tree; GET requests only; counts and ratios only

For each day, the figures of the day the settle step would derive: the run_day derivation (the adapter's derive over the previous trading day to the day, keeping business_date == day), through
the real silver reader and the handler's FLOOR_DAY, WITHOUT any write. Prints, per day: the derived row count (equal to run_day's `rows`), the NOT_MEASURABLE share (rows whose return_basis
is NOT_MEASURABLE), and the flow-account count (rows whose external_flow is non-null and non-zero). With the landed partition present it also prints the landed row count, so a changed row
count is visible. No account id, figure or value is printed.
"""
import importlib.util
import io
import sys
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path.cwd()
HANDLER = ROOT / "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
sys.path.insert(0, str(HANDLER.parent))
spec = importlib.util.spec_from_file_location("handler", str(HANDLER))
h = importlib.util.module_from_spec(spec)
sys.modules["handler"] = h
spec.loader.exec_module(h)
cbd = h.cbd
tc = h.tc


def figures(reader, day):
    prev = tc.prev_trading_day(__import__("datetime").date.fromisoformat(day)).isoformat()
    rows, _summary = cbd.derive(reader, cbd.accounts_in_partition(reader, day), prev, day, floor_day=h.FLOOR_DAY)
    rows = [r for r in rows if r["business_date"] == day]
    n = len(rows)
    nm = sum(1 for r in rows if r.get("return_basis") == "NOT_MEASURABLE")
    flow = sum(1 for r in rows if r.get("external_flow") not in (None, 0, 0.0))
    return n, nm, flow


def landed_rows(s3, day):
    bucket, prefix = cbd.gold_prefix()
    key = "%sdate=%s/data.parquet" % (prefix, day)
    try:
        body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    except Exception:  # noqa: BLE001
        return None
    return pq.read_table(io.BytesIO(body)).num_rows


def main(days):
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    reader = cbd.CottonwoodBlackDiamondSilverReader()
    for day in days:
        n, nm, flow = figures(reader, day)
        landed = landed_rows(s3, day)
        share = (100.0 * nm / n) if n else 0.0
        print("settle day %s: derived rows %d, NOT_MEASURABLE %d (%.1f percent), flow accounts %d, landed rows %s"
              % (day, n, nm, share, flow, landed if landed is not None else "none"))


if __name__ == "__main__":
    main(sys.argv[1:])
