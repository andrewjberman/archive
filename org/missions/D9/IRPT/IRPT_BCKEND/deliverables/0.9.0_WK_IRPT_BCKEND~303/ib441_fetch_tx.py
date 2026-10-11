#!/usr/bin/env python3
"""IB-pr-441: read the silver transactions table (beside the holdings table), every date partition, rows de-duplicated on TransactionID.  Read only.
No account column is read.  Writes a pickle (outside the repo) of the de-duplicated rows reduced to the columns below.

    python -I ib441_fetch_tx.py <out.pkl>
"""
import io
import pickle
import sys
from collections import Counter
from pathlib import Path
import boto3
import pyarrow.parquet as pq
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ib441_fetch_s3 as f  # noqa: E402

COLS = ["TransactionID", "Transaction Type", "Transaction Sub Type", "Trade Date", "Settle Date", "Price", "CUSIP", "Ticker", "Symbol", "SEC Asset Type", "Share Class Type"]


def main():
    out = sys.argv[1]
    sp, _ = f.declared()
    prefix = sp.rstrip("/").rsplit("/", 1)[0] + "/fact_transactions/"
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))
    parts, tok = [], None
    while True:
        kw = dict(Bucket=f.BUCKET, Prefix=prefix, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        parts += [p["Prefix"] for p in r.get("CommonPrefixes", [])]
        tok = r.get("NextContinuationToken")
        if not tok:
            break
    seen, rows, absent, objs = {}, 0, Counter(), 0
    for p in parts:
        for o in s3.list_objects_v2(Bucket=f.BUCKET, Prefix=p).get("Contents", []):
            if not o["Key"].endswith(".parquet"):
                continue
            b = io.BytesIO(s3.get_object(Bucket=f.BUCKET, Key=o["Key"])["Body"].read())
            have = set(pq.read_schema(b).names)
            for c in COLS:
                if c not in have:
                    absent[c] += 1
            t = pq.read_table(b, columns=[c for c in COLS if c in have]).to_pydict()
            n = len(t["TransactionID"])
            rows += n
            objs += 1
            for i in range(n):
                k = t["TransactionID"][i]
                if k not in seen:
                    seen[k] = {c: (t[c][i] if c in t else None) for c in COLS}
    pickle.dump({"rows": list(seen.values()), "partitions": sorted(p.rstrip("/").split("date=")[1] for p in parts), "objects": objs, "rows_read": rows,
                 "absent_cols": dict(absent)}, open(out, "wb"))
    print("partitions", len(parts), "objects", objs, "rows", rows, "distinct ids", len(seen), "absent", dict(absent))


if __name__ == "__main__":
    main()
