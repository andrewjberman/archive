"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE census of 49 Financial's `business_date` against the CTO's round-131 rule (msg 9342
ruling 3): the first NYSE trading day on or after the trade date.

  python <this file> <out.json> [n_partitions]        default every partition (0)

Over every partition of the 49 Financial `fact_trn` table it counts the rows; the rows whose trade_date is unreadable; the rows where business_date
equals the first trading day on or after trade_date; the rows where it differs, split by whether business_date equals the raw trade_date (the source
does not roll) or is some other day; and the rows whose trade_date falls on a non-trading day. Counts only: no account id, amount, symbol or
identifier is kept or written. GET requests only. Run from the repository root with the box's AWS credentials; needs boto3, pandas and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import random
import sys
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
import account_return_daily as ard  # noqa: E402
import trading_calendar as tc  # noqa: E402

s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))
WINDOW = 14


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def first_on_or_after(d, cache):
    if d in cache:
        return cache[d]
    x = d
    out = None
    for _ in range(WINDOW):
        if tc.is_trading_day(x):
            out = x
            break
        x += dt.timedelta(days=1)
    cache[d] = out
    return out


def main(out_path, n_partitions):
    at = load("account_transaction", "data/assets/scripts/gold/irpt_reporting/account_transaction.py")
    src = json.load(open(ROOT / "data/assets/scripts/gold/irpt_reporting/sources.json", encoding="utf-8"))["schwab_08335338"]
    bucket, prefix = src["bucket"], src["transactions_prefix"]
    days = ard.partition_days(s3, bucket, prefix)
    picked = days if not n_partitions or n_partitions >= len(days) else sorted(random.Random(132).sample(days, n_partitions))
    c = {"rows": 0, "trade_date_unreadable": 0, "business_date_unreadable": 0, "equal_to_rule": 0, "differs_equals_raw_trade_date": 0,
         "differs_other": 0, "trade_date_on_non_trading_day": 0, "no_trading_day_in_window": 0}
    cache = {}
    for day in picked:
        tables = []
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    tables.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()),
                                                columns=["business_date", "trade_date"]))
        if not tables:
            continue
        df = pa.concat_tables(tables, promote_options="default").to_pandas()
        counts = df.groupby(["business_date", "trade_date"], dropna=False).size()
        for (b_raw, t_raw), n in counts.items():
            c["rows"] += int(n)
            t = at._day_or_none(t_raw)
            b = at._day_or_none(b_raw)
            if t is None:
                c["trade_date_unreadable"] += int(n)
                continue
            if b is None:
                c["business_date_unreadable"] += int(n)
                continue
            want = first_on_or_after(t, cache)
            if want is None:
                c["no_trading_day_in_window"] += int(n)
                continue
            if t != want:
                c["trade_date_on_non_trading_day"] += int(n)
            if b == want:
                c["equal_to_rule"] += int(n)
            elif b == t:
                c["differs_equals_raw_trade_date"] += int(n)
            else:
                c["differs_other"] += int(n)
        print("read", day, flush=True)
    out = {"firm": "49financial", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "table": "fact_trn",
           "partitions_in_table": len(days), "partitions_read": len(picked), "counts": c, "calendar": tc.calendar_source(),
           "reader": "values-free: counts of rows by how business_date compares with the first trading day on or after trade_date; no value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(c)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0)
