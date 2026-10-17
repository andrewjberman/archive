"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY census of the Cottonwood fact_transactions silver PARTITION LAG -- how far after a row's own business day the row lands.

  python <this file>        run from the repository root; GET requests only; counts and dates only (no account id, figure or symbol is read into the output)

Background (the CTO's msg 10588, dell1 msg 7612): the Cottonwood transaction pull is a 14-day period pull, so a business day's rows can sit in LATER partitions. The producer
(account_transaction_cottonwood) takes a day's frame from the ONE partition date=D and REFUSES the whole day when any row's business_date (the first trading day on or after the Trade
Date, the producer's own rule) is not D. This census measures, over every partition, only the Trade Date column and prints: the denominator (partitions and rows scanned), the rows by
LAG (trading days from the row's business_date to the partition that holds it; 0 = the row sits in its own day's partition), the partitions the current producer would REFUSE
(any row with lag != 0), and, for business days, how many distinct partitions hold their rows.
"""
import importlib.util
import io
import sys
from collections import Counter, defaultdict
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
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def trading_lag(business, partition, cache):
    """Trading days from business to partition (0 when equal; negative when the row's business day is AFTER the partition)."""
    key = (business, partition)
    if key not in cache:
        if business == partition:
            cache[key] = 0
        elif business < partition:
            cache[key] = len(tc.trading_days_between(business, partition)) - 1
        else:
            cache[key] = -(len(tc.trading_days_between(partition, business)) - 1)
    return cache[key]


def main():
    days = ard.partition_days(s3, cbd.BUCKET, PREFIX)
    rows = unreadable = 0
    by_lag = Counter()
    refused_parts = 0
    parts_per_business = defaultdict(set)
    lagcache = {}
    bdcache = {}
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
        off = 0
        for v in col:
            rows += 1
            dd = at._day_of(v)
            if dd is None:
                unreadable += 1
                continue
            d = dd.isoformat() if hasattr(dd, "isoformat") else str(dd)[:10]
            if d not in bdcache:
                try:
                    bdcache[d] = str(atx.business_date_with_claim(dd, window=at.PERFORMANCE_DAY_WINDOW)[0])[:10]
                except Exception:  # noqa: BLE001
                    bdcache[d] = None
            b = bdcache[d]
            if b is None:
                unreadable += 1
                continue
            lag = trading_lag(b, day, lagcache)
            by_lag[lag] += 1
            parts_per_business[b].add(day)
            if lag != 0:
                off += 1
        if off:
            refused_parts += 1
    print("partitions scanned: %d, rows scanned: %d, rows the producer cannot place (unreadable Trade Date or no trading day): %d" % (len(days), rows, unreadable))
    placed = sum(by_lag.values())
    print("rows placed: %d" % placed)
    for lag in sorted(by_lag):
        print("  lag %+d trading day(s): %d row(s)" % (lag, by_lag[lag]))
    print("partitions the CURRENT producer would REFUSE (any row with lag != 0): %d of %d" % (refused_parts, len(days)))
    spread = Counter(len(v) for v in parts_per_business.values())
    print("business days with rows: %d; by the number of distinct partitions holding them:" % len(parts_per_business))
    for n in sorted(spread):
        print("  %d partition(s): %d business day(s)" % (n, spread[n]))
    late = [b for b, v in parts_per_business.items() if max(v) > b]
    print("business days with at least one row in a LATER partition: %d; newest such business day: %s" % (len(late), max(late) if late else None))


if __name__ == "__main__":
    main()
