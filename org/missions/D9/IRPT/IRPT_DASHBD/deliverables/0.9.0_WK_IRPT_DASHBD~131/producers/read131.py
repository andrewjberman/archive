"""~131: read-only S3 reads of 49 Financial's transactions (copy and original), rows of the 49 accounts, into a private pickle.
Usage: python -I read131.py copy|orig"""
import datetime as dt
import io
import os
import pickle
import sys
from concurrent.futures import ThreadPoolExecutor
import boto3
import pyarrow.parquet as pq
from botocore.config import Config
PRIV = os.environ["IRPT_PRIV_ROOT"].rstrip("/") + "/0.9.0_WK_IRPT_DASHBD~131/"
OUTD = os.environ["IRPT_RERUN_DIR"].rstrip("/") + "/"
which = sys.argv[1]
days = pickle.load(open(PRIV + "days234.pkl", "rb"))
want = {x["a"].strip().lstrip("0") for x in days}
lo = (dt.date.fromisoformat(min(x["d"] for x in days)) - dt.timedelta(days=100)).isoformat()
COLS = ["transaction_id", "return_date", "trade_date", "transaction_type", "transaction_sub_type", "external_flow", "account_number",
        "market_value", "asset_id", "asset_name", "asset_display_name", "units"]
s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
if which == "copy":
    B, P = "opal-data-assets", "blackdiamond/49financial/silver_legacy/transactions/"
    keys = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
        for o in p.get("Contents", []):
            if o["Key"].endswith(".parquet"):
                day = o["Key"].split("date=")[1][:10]
                if day >= lo:
                    keys.append((day, o["Key"]))
else:
    B, P = "opal-data-bd", "silver/transactions/"
    keys = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
        for o in p.get("Contents", []):
            if o["Key"].endswith(".parquet"):
                day = o["Key"].rsplit("/", 1)[1][:10]
                if day >= lo:
                    keys.append((day, o["Key"]))
keys.sort()
print(which, "files from", lo, ":", len(keys))
errs = []

def one(dk):
    day, k = dk
    try:
        t = pq.read_table(io.BytesIO(s3.get_object(Bucket=B, Key=k)["Body"].read()))
    except Exception as e:
        errs.append((day, repr(e)[:200]))
        return day, [], 0, None
    have = [c for c in COLS if c in t.schema.names]
    rws = [r for r in t.select(have).to_pylist() if str(r.get("account_number")).strip().lstrip("0") in want]
    return day, rws, t.num_rows, [c for c in COLS if c not in t.schema.names]

out, nonempty, missing = [], [], set()
with ThreadPoolExecutor(24) as ex:
    for day, rws, n, miss in ex.map(one, keys):
        for r in rws:
            r["_file_day"] = day
        out += rws
        if n:
            nonempty.append(day)
        if miss:
            missing.update(miss)
print("rows kept", len(out), "files with rows", len(nonempty), "newest nonempty file", max(nonempty), "missing cols", missing, "errors", len(errs), errs[:3])
pickle.dump({"rows": out, "newest_nonempty": max(nonempty), "nfiles": len(keys), "errs": errs, "lo": lo}, open(OUTD + "txn_%s.pkl" % which, "wb"))
