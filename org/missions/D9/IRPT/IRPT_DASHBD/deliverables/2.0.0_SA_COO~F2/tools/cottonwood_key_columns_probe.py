"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY probe of WHICH columns make a Cottonwood fact_transactions TransactionID's rows differ (CTO msg 10588 / 10592: dedup on transaction_id).

  python <this file> <business_day> [<business_day> ...]        run from the repository root; GET requests only; counts and COLUMN NAMES only

For each business day D: read all columns of the partitions D..D+14 trading days, keep the rows whose business_date (the producer's rule) is D, and report
  (a) ACROSS partitions: for each TransactionID seen in two or more partitions with ONE line per partition, the columns whose value differs between partitions (count of ids per column);
  (b) WITHIN a partition: for each (partition, TransactionID) holding more than one row, the columns whose value differs between those rows (count of pairs per column), and how many pairs
      remain distinct when the columns found varying in (a) are ignored.
No value is printed.
"""
import datetime as dt
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
WINDOW = 14
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def read_partition(day):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=cbd.BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                tables.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=cbd.BUCKET, Key=o["Key"])["Body"].read())))
    return pa.concat_tables(tables, promote_options="default") if tables else None


def main(days):
    existing = set(ard.partition_days(s3, cbd.BUCKET, PREFIX))
    bd_cache = {}
    across = Counter()
    across_ids = 0
    within = Counter()
    within_pairs = 0
    within_still_distinct = 0
    vary_cols = set()
    pending = []
    for d in days:
        start = dt.date.fromisoformat(d)
        span = [str(x)[:10] for x in tc.trading_days_between(start, start + dt.timedelta(days=40))][:WINDOW + 1]
        per_id = defaultdict(dict)  # id -> {partition: [row dict, ...]}
        for p in [x for x in span if x in existing]:
            tbl = read_partition(p)
            if tbl is None:
                continue
            cols = tbl.column_names
            data = {c: tbl.column(c).to_pylist() for c in cols}
            for r in range(tbl.num_rows):
                dd = at._day_of(data["Trade Date"][r])
                if dd is None:
                    continue
                k = dd.isoformat()
                if k not in bd_cache:
                    bd_cache[k] = str(atx.business_date_with_claim(dd, window=at.PERFORMANCE_DAY_WINDOW)[0])[:10]
                if bd_cache[k] != d:
                    continue
                tid = data["TransactionID"][r]
                if tid is None:
                    continue
                per_id[str(tid)].setdefault(p, []).append({c: data[c][r] for c in cols})
        for tid, parts in per_id.items():
            single = [rows[0] for rows in parts.values() if len(rows) == 1]
            if len(single) >= 2:
                across_ids += 1
                for c in single[0]:
                    if len({str(s.get(c)) for s in single}) > 1:
                        across[c] += 1
            for rows in parts.values():
                if len(rows) > 1:
                    pending.append(rows)
    vary_cols = {c for c, n in across.items() if n > 0}
    for rows in pending:
        within_pairs += 1
        for c in rows[0]:
            if len({str(r.get(c)) for r in rows}) > 1:
                within[c] += 1
        sig = {tuple(str(r.get(c)) for c in sorted(rows[0]) if c not in vary_cols) for r in rows}
        if len(sig) > 1:
            within_still_distinct += 1
    print("business days: %s; ids seen in 2+ partitions with one line each: %d" % (",".join(days), across_ids))
    print("ACROSS partitions, columns that differ (ids): %s" % dict(sorted(across.items(), key=lambda kv: -kv[1])))
    print("WITHIN a partition, (partition, id) pairs holding more than one row: %d; columns that differ (pairs): %s" % (within_pairs, dict(sorted(within.items(), key=lambda kv: -kv[1]))))
    print("pairs still distinct after ignoring the columns that vary across partitions: %d of %d" % (within_still_distinct, within_pairs))


if __name__ == "__main__":
    main(sys.argv[1:])
