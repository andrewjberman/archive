"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY probe of the Cottonwood fact_transactions window rule (CTO msg 10588).

  python <this file> <business_day> [<business_day> ...]        run from the repository root; GET requests only; counts only

For each business day D given: read the Trade Date and TransactionID columns of the partitions D through D+14 trading days (those that exist), keep the rows whose business_date (the
producer's own rule) is D, and print: the partitions read, the raw row count, the distinct TransactionID count, the rows with a null/blank TransactionID, the rows per partition, and the
number of partitions in which the average TransactionID appears. No account id, figure, symbol or TransactionID value is printed.
"""
import datetime as dt
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
import account_transaction as atx  # noqa: E402
import trading_calendar as tc  # noqa: E402


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cbd = load("cbd", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")
at = load("account_transaction_cottonwood", "data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py")
PREFIX = cbd.SILVER_ROOT + "fact_transactions/"
WINDOW = 14
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def read_partition(day):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=cbd.BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                raw = s3.get_object(Bucket=cbd.BUCKET, Key=o["Key"])["Body"].read()
                tables.append(pq.read_table(io.BytesIO(raw), columns=["Trade Date", "TransactionID"]))
    if not tables:
        return None
    return pa.concat_tables(tables, promote_options="default")


def window_days(day, existing):
    """The partition days D through D+WINDOW trading days that exist."""
    start = dt.date.fromisoformat(day)
    span = [str(x)[:10] for x in tc.trading_days_between(start, start + dt.timedelta(days=40))][:WINDOW + 1]
    return [p for p in span if p in existing]


def main(days):
    existing = set(ard.partition_days(s3, cbd.BUCKET, PREFIX))
    bd_cache = {}
    for d in days:
        parts = window_days(d, existing)
        raw = 0
        ids = Counter()
        null_ids = 0
        per_part = {}
        for p in parts:
            tbl = read_partition(p)
            if tbl is None:
                continue
            n = 0
            for tv, tid in zip(tbl.column("Trade Date").to_pylist(), tbl.column("TransactionID").to_pylist()):
                dd = at._day_of(tv)
                if dd is None:
                    continue
                k = dd.isoformat()
                if k not in bd_cache:
                    bd_cache[k] = str(atx.business_date_with_claim(dd, window=at.PERFORMANCE_DAY_WINDOW)[0])[:10]
                if bd_cache[k] != d:
                    continue
                n += 1
                raw += 1
                if tid is None or not str(tid).strip():
                    null_ids += 1
                else:
                    ids[str(tid)] += 1
            per_part[p] = n
        distinct = len(ids)
        avg = (sum(ids.values()) / distinct) if distinct else 0
        print("business day %s: partitions read %d (of window %d), raw rows %d, distinct TransactionID %d, null/blank id rows %d, mean partitions per id %.2f"
              % (d, len(parts), WINDOW + 1, raw, distinct, null_ids, avg))
        print("  rows per partition (lag order): %s" % [per_part[p] for p in parts])


if __name__ == "__main__":
    main(sys.argv[1:])
