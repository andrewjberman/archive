"""~115 step 1: re-read 49 Financial's silver_legacy/transactions (same bucket/prefix ~108/~113 read; read-only GETs) for the accounts of ALL 51
contested segments, keeping the transaction id and portfolio group. Private output. Prints counts only. Usage: python -I c1_read.py"""
import io
import pickle
from concurrent.futures import ThreadPoolExecutor

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~115/"
BUCKET = "opal-data-assets"
PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
rows90 = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
want = {r["a"].lstrip("0") for r in rows90 if r["idx"] in M51}
print("segments", sum(1 for r in rows90 if r["idx"] in M51), "accounts", len(want))
s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
tops = []
for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
    tops += [cp["Prefix"] for cp in p.get("CommonPrefixes", [])]
NEED = ["account_number", "return_date", "external_flow", "market_value", "transaction_id", "portfolio_group", "transaction_type",
        "transaction_sub_type", "action", "account_fee", "transaction_fee"]
nobj = [0]
nmissingcol = [0]


def one(pref):
    out = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=pref):
        for o in pg.get("Contents", []):
            if not o["Key"].endswith(".parquet"):
                continue
            t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
            have = [c for c in NEED if c in t.schema.names]
            if "transaction_id" not in have:
                nmissingcol[0] += 1
            part = pref.rstrip("/").rsplit("=", 1)[-1]
            for r in t.select(have).to_pylist():
                if str(r.get("account_number")).strip().lstrip("0") in want:
                    r["_part"] = part
                    out.append(r)
            nobj[0] += 1
    return out


rows = []
with ThreadPoolExecutor(24) as ex:
    for out in ex.map(one, tops):
        rows += out
print("date prefixes", len(tops), "objects read", nobj[0], "objects without a transaction_id column", nmissingcol[0], "rows kept", len(rows))
pickle.dump({"rows": rows, "objects": nobj[0], "prefixes": len(tops), "bucket_prefix": BUCKET + "/" + PREFIX}, open(OUT + "c1_rows.pkl", "wb"))
