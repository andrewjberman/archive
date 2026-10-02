"""IRPT_DASHBD TO-DB-b-11 -- MEASURE the reporting gold producer (the producer's own functions, in the order the handler's
compute() calls them) over the whole holdings population for ONE day. Reads only: nothing is uploaded or written to disk; the
frame stays in memory and its parquet size is taken from a BytesIO.

SCALED: the laptop link moved ~35-200 KB/s when this was run, so the account-count-independent inception scan
(first_data_dates, a narrow read of every balance partition) is timed on SAMPLE_PARTS partitions, not all 563.

Usage: python p2_producer_measure_r5.py <repo_root> <YYYY-MM-DD> [max_accounts, 0 = all] [SAMPLE_PARTS]
"""
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
day = sys.argv[2]
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 0
sample_parts = int(sys.argv[4]) if len(sys.argv) > 4 else 3

spec = importlib.util.spec_from_file_location("rg_handler", root / "infra/aws/lambda/investor-reporting/reporting-gold/handler.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
ard = h.ard
s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
firm = ard.firm_scope(src)

uri = ard.opal_naming.address("irpt", firm, "gold", ard.HOLDINGS_TABLE, "date=" + day)
bucket, key = ard._split(uri)
base = key.rsplit("/date=", 1)[0] + "/"
population = sorted(set(ard.read_partition(s3, bucket, base, day, columns=["account_id"])["account_id"].astype(str)))
print("population: s3://%s/%sdate=%s accounts=%d" % (bucket, base, day, len(population)))
accts = population[:cap] if cap else population

stages = {}


def stage(name, t):
    stages[name] = round(time.time() - t, 3)
    print("STAGE %s %.3fs" % (name, stages[name]), flush=True)


thresholds = h.load_thresholds()
t0 = time.time()
table, keycols = ard.load_classification(src)
t = time.time()
trn_days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])
stage("list_trn_days", t)

real_days = ard.partition_days
all_bal = real_days(s3, src["bucket"], src["balance_prefix"])
ard.partition_days = lambda s3_, b, p: all_bal[-sample_parts:] if p == src["balance_prefix"] else real_days(s3_, b, p)
t = time.time()
first_data = ard.first_data_dates(s3, src, day, accounts=accts, workers=12)
stage("first_data_dates_sample_%d_of_%d" % (sample_parts, len(all_bal)), t)
ard.partition_days = real_days

t = time.time()
bal_days = ard.partition_days(s3, src["bucket"], src["balance_prefix"])
stage("list_bal_days", t)
flows = ard.FlowCache(s3, src, table, keycols, accts)
t = time.time()
value_cache, holdings_cache = ard.prefetch(s3, src, firm, [day], trn_days, accounts=accts, flows=flows, workers=12)
stage("prefetch", t)
t = time.time()
rows, notes, first_seen = ard.compute_range(
    s3, src, firm, [day], trn_days, accounts=accts, thresholds=thresholds, flows=flows,
    value_cache=value_cache, holdings_cache=holdings_cache, first_data=first_data, bal_days=bal_days)
stage("compute_range", t)
seconds = time.time() - t0

frame = pd.DataFrame(rows)
frame = frame.drop(columns=[c for c in frame.columns if c.startswith("_")])
ard._check_enums(frame)
buf = io.BytesIO()
pq.write_table(pa.Table.from_pandas(frame[ard.COLUMNS], schema=ard.ARROW_SCHEMA, preserve_index=False), buf)
print(json.dumps({"day": day, "accounts_in": len(accts), "accounts_out": int(frame["account_id"].nunique()) if len(frame) else 0,
                  "rows": int(len(frame)), "seconds": round(seconds, 1), "stages": stages,
                  "gold_partition_bytes": buf.tell()}), flush=True)
