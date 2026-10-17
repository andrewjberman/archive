"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY census of Cottonwood fact_transactions rows whose Trade Date is not a trading day (the rows the producer rolls forward and stamps business_date_claim `inferred`).

  python <this file>        run from the repository root; GET requests only; counts and dates only (no account id, figure or symbol is read into the output)

Only the `Trade Date` column of each partition is read. A row is "rolled" when its Trade Date is not a trading day in lib/trading_calendar.py. The output is the denominator
(partitions and rows scanned), the number of rolled rows, and the partitions and distinct trade dates that hold them.
"""
import importlib.util
import io
import sys
from collections import Counter
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402
import trading_calendar as tc  # noqa: E402


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cbd = load("cbd", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")
at = load("account_transaction_cottonwood", "data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py")
PREFIX = cbd.SILVER_ROOT + "fact_transactions/"
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def main():
    days = ard.partition_days(s3, cbd.BUCKET, PREFIX)
    rows = 0
    unreadable = 0
    rolled_dates = Counter()
    rolled_parts = Counter()
    trading_cache = {}
    for day in days:
        tables = []
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=cbd.BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    raw = s3.get_object(Bucket=cbd.BUCKET, Key=o["Key"])["Body"].read()
                    tables.append(pq.read_table(io.BytesIO(raw), columns=["Trade Date"]))
        if not tables:
            continue
        col = pa.concat_tables(tables, promote_options="default").column("Trade Date").to_pylist()
        rows += len(col)
        for v in col:
            dd = at._day_of(v)  # the producer's own reader of a Trade Date cell (MM/DD/YYYY or ISO); None when unreadable
            if dd is None:
                unreadable += 1
                continue
            d = dd.isoformat() if hasattr(dd, "isoformat") else str(dd)[:10]
            if d not in trading_cache:
                trading_cache[d] = bool(tc.is_trading_day(d))
            if not trading_cache[d]:
                rolled_dates[d] += 1
                rolled_parts[day] += 1
    print("partitions scanned: %d, rows scanned: %d, Trade Date cells the producer cannot read: %d" % (len(days), rows, unreadable))
    print("rolled rows (Trade Date not a trading day): %d in %d partition(s) over %d distinct trade date(s)" % (sum(rolled_dates.values()), len(rolled_parts), len(rolled_dates)))
    for d, n in sorted(rolled_dates.items())[:40]:
        print("  trade date %s: %d row(s)" % (d, n))


if __name__ == "__main__":
    main()
