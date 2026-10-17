"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY completeness curve and key census of the Cottonwood fact_transactions window rule (CTO msg 10588).

  python <this file>        run from the repository root; GET requests only; counts and ratios only (no account id, figure, symbol or TransactionID value is printed)

One pass over every silver partition. For each business day D (the producer's own business_date rule) whose full window D..D+14 trading days is available (D+14 trading days is not after the
newest partition), it reports how complete the day is at lag k: the share of the day's final distinct TransactionIDs (union over lags 0..14) already seen at lags <= k. It also censuses
the key: (partition, TransactionID) pairs holding more than one row and whether those rows are identical or distinct lines, and TransactionIDs whose row content differs between partitions.
"""
import hashlib
import importlib.util
import io
import statistics
import sys
from collections import defaultdict
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
                tables.append(pq.read_table(io.BytesIO(raw)))
    return pa.concat_tables(tables, promote_options="default") if tables else None


def rowhash(values):
    return hashlib.sha1("\x1f".join("" if v is None else str(v) for v in values).encode("utf-8", "replace")).hexdigest()[:12]


def main():
    days = ard.partition_days(s3, cbd.BUCKET, PREFIX)
    index = {d: i for i, d in enumerate(days)}
    bd_cache = {}
    # per business day: {partition_day: {txn_id: [rowhash,...]}}
    seen = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for p in days:
        tbl = read_partition(p)
        if tbl is None:
            continue
        cols = tbl.column_names
        trade_i, id_i = cols.index("Trade Date"), cols.index("TransactionID")
        data = [tbl.column(c).to_pylist() for c in cols]
        for r in range(tbl.num_rows):
            dd = at._day_of(data[trade_i][r])
            if dd is None:
                continue
            k = dd.isoformat()
            if k not in bd_cache:
                bd_cache[k] = str(atx.business_date_with_claim(dd, window=at.PERFORMANCE_DAY_WINDOW)[0])[:10]
            tid = data[id_i][r]
            if tid is None or not str(tid).strip():
                continue
            seen[bd_cache[k]][p][str(tid)].append(rowhash([data[c][r] for c in range(len(cols))]))
    newest = days[-1]
    # trading-day lag of a partition from a business day, over the available partition list
    curves = defaultdict(list)
    complete_days = 0
    multi_pairs = multi_distinct = ids_changed = ids_total = late_ids = 0
    for b, per_part in seen.items():
        start = __import__("datetime").date.fromisoformat(b)
        span = [str(x)[:10] for x in tc.trading_days_between(start, start + __import__("datetime").timedelta(days=45))][:WINDOW + 1]
        full = len(span) == WINDOW + 1 and span[-1] <= newest and all(s in index for s in span)
        by_lag = {span.index(p): v for p, v in per_part.items() if p in span}
        for ids in per_part.values():
            for tid, hs in ids.items():
                if len(hs) > 1:
                    multi_pairs += 1
                    if len(set(hs)) > 1:
                        multi_distinct += 1
        allids = defaultdict(set)
        for lag, ids in by_lag.items():
            for tid, hs in ids.items():
                allids[tid].update(hs)
        ids_total += len(allids)
        ids_changed += sum(1 for hs in allids.values() if len(hs) > 1)
        if not full:
            continue
        complete_days += 1
        final = set(allids)
        acc = set()
        for k in range(WINDOW + 1):
            acc |= set(by_lag.get(k, {}))
            curves[k].append(len(acc) / len(final) if final else 1.0)
        late_ids += len(final - set().union(*[set(by_lag.get(k, {})) for k in range(10)]))
    print("partitions scanned: %d (newest %s); business days seen: %d; with a full window D..D+14: %d" % (len(days), newest, len(seen), complete_days))
    print("completeness at lag k (share of the day's final distinct TransactionIDs seen by lag k), over %d full-window days:" % complete_days)
    for k in range(WINDOW + 1):
        v = curves[k]
        if v:
            print("  lag %2d: min %.4f  median %.4f" % (k, min(v), statistics.median(v)))
    print("TransactionIDs first seen AFTER lag 9 (full-window days): %d" % late_ids)
    print("(partition, TransactionID) pairs holding more than one row: %d, of which the rows are DISTINCT lines: %d" % (multi_pairs, multi_distinct))
    print("TransactionIDs (all days) %d; with more than one distinct row content across partitions or lines: %d" % (ids_total, ids_changed))


if __name__ == "__main__":
    main()
