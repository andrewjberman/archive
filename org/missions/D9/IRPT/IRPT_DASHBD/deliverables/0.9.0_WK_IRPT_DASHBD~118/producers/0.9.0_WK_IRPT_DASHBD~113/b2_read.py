"""~113 step 7: re-read 49 Financial's silver_legacy/transactions (same bucket/prefix ~108 read, read-only GETs) keeping the OBJECT partition of each row for the
18 segments' accounts, so the k copies of a day's rows can be located. Private output. Usage: python -I b2_read.py"""
import io
import pickle
from concurrent.futures import ThreadPoolExecutor

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

BUCKET = "opal-data-assets"
PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
want = {d["a"].lstrip("0") for d in R["days50"]}
print("accounts", len(want))
s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
tops = []
for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
    for cp in p.get("CommonPrefixes", []):
        tops.append(cp["Prefix"])
cols = ["return_date", "action", "transaction_type", "transaction_sub_type", "external_flow", "account_number", "market_value",
        "transaction_fee", "income", "account_fee", "trade_date", "settle_date"]
nobj = [0]
allcols = [set()]


def one(pref):
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix=pref)
    out = []
    for o in r.get("Contents", []):
        if not o["Key"].endswith(".parquet"):
            continue
        t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
        allcols[0] |= set(t.schema.names)
        have = [c for c in cols if c in t.schema.names]
        extra = [c for c in t.schema.names if c not in cols]
        for i, r2 in enumerate(t.to_pylist()):
            if str(r2.get("account_number")).strip().lstrip("0") in want:
                row = {c: r2.get(c) for c in have}
                row["_part"] = pref.rstrip("/").rsplit("=", 1)[1]
                row["_pos"] = i
                row["_extra"] = {c: r2.get(c) for c in extra}
                out.append(row)
        nobj[0] += 1
    return out


rows = []
with ThreadPoolExecutor(24) as ex:
    for out in ex.map(one, tops):
        rows += out
print("objects", nobj[0], "rows kept", len(rows))
print("all columns", sorted(allcols[0]))
pickle.dump({"rows": rows, "prefix": BUCKET + "/" + PREFIX, "objects": nobj[0]}, open(OUT + "b2_rows.pkl", "wb"))
