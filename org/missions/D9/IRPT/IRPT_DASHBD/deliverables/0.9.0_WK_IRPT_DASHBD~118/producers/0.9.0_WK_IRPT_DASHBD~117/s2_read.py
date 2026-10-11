"""~117 step 2: read 49 Financial's silver_legacy/transactions (read-only GETs, same bucket/prefix as ~108/~115) for the accounts of all 90
segments, keeping the transaction id. Private output. Counts only. Usage: python -I s2_read.py"""
import io
import pickle
from concurrent.futures import ThreadPoolExecutor

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~117/"
BUCKET = "opal-data-assets"
PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
rows90 = pickle.load(open(P + "table90.pkl", "rb"))
want = {r["a"].lstrip("0") for r in rows90}
print("segments", len(rows90), "accounts", len(want))
s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
tops = []
for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
    tops += [cp["Prefix"] for cp in p.get("CommonPrefixes", [])]
NEED = ["account_number", "return_date", "external_flow", "market_value", "transaction_id", "portfolio_group"]
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
            for r in t.select(have).to_pylist():
                if str(r.get("account_number")).strip().lstrip("0") in want:
                    out.append(r)
            nobj[0] += 1
    return out


rows = []
with ThreadPoolExecutor(24) as ex:
    for out in ex.map(one, tops):
        rows += out
print("date prefixes", len(tops), "objects read", nobj[0], "objects without a transaction_id column", nmissingcol[0], "rows kept", len(rows))
pickle.dump({"rows": rows, "objects": nobj[0], "prefixes": len(tops)}, open(OUT + "s2_rows.pkl", "wb"))
