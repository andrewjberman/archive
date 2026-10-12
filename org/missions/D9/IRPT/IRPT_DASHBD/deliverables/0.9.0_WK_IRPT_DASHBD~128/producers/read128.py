"""TO-DB-b-159 reader (~128): read-only S3 LIST and GET of the ONE firm's served daily account-return gold partitions, into a private
copy outside the repo. Client-keyed output stays private; this script holds no account id, amount or return literal.
Bucket and key shape as ~108 read90.py (GOLD_BUCKET, GOLD_PREFIX, date=<d>/data.parquet) and the same boto3 client build.
Usage: python -I read128.py
"""
import io
import pickle
from concurrent.futures import ThreadPoolExecutor

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~128/"
GOLD_BUCKET = "opal-data-49financial"
GOLD_PREFIX = "irpt/49financial/gold/account_return_daily/"


def main():
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=GOLD_BUCKET, Prefix=GOLD_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date="):
                dates.append(seg[5:])
    dates.sort()
    print("partitions listed", len(dates), "first", dates[0], "last", dates[-1])
    meta = {}

    def one(d):
        r = s3.get_object(Bucket=GOLD_BUCKET, Key="%sdate=%s/data.parquet" % (GOLD_PREFIX, d))
        body = r["Body"].read()
        t = pq.read_table(io.BytesIO(body))
        meta[d] = {"last_modified_utc": r["LastModified"].isoformat(), "bytes": len(body)}
        return d, t.to_pylist(), t.schema.names

    rows, names = [], None
    with ThreadPoolExecutor(12) as ex:
        for d, rs, nm in ex.map(one, dates):
            rows += rs
            names = names or nm
    pickle.dump({"rows": rows, "columns": names, "dates": dates, "meta": meta}, open(OUT + "gold_copy.pkl", "wb"))
    print("rows", len(rows), "columns", names)
    print("newest partition last_modified_utc", max(m["last_modified_utc"] for m in meta.values()))
    print("s3 writes 0")


if __name__ == "__main__":
    main()
