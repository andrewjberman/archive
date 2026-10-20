"""Read-only re-measure of the 49F dim_account_xref coverage (CRO~Y brief item 2, method of probe.py). Prints counts only, no account id."""
import sys

import boto3
import pyarrow.fs as pafs
import pyarrow.parquet as pq

A, B = "opal-data-assets", "opal-data-bd"
s3 = boto3.client("s3")
fs = pafs.S3FileSystem(region="us-east-1")


def newest(bucket, prefix):
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        keys += [(o["Key"], o["LastModified"]) for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]
    import re
    dated = [k for k in keys if re.search(r"\d{4}-\d{2}-\d{2}", k[0])]
    dated.sort(key=lambda x: re.search(r"\d{4}-\d{2}-\d{2}", x[0]).group(0))
    return dated[-1], len(dated)


def read(bucket, key, cols):
    with fs.open_input_file("%s/%s" % (bucket, key)) as f:
        return pq.read_table(f, columns=cols).to_pylist()


(xk, xm), xn = newest(A, "blackdiamond/49f/silver/dim_account_xref/")
(uk, um), un_n = newest(B, "silver/unrealized/")
print("xref newest key:", xk, "objects", xn, "modified", xm.isoformat())
print("unrealized newest key:", uk, "objects", un_n, "modified", um.isoformat())
xr = read(A, xk, ["bd_account_id"])
xids = {str(r["bd_account_id"]) for r in xr}
un = read(B, uk, ["account_id"])
live = {str(r["account_id"]) for r in un if str(r["account_id"]).startswith("z08")}
print("xref rows %d, distinct bd_account_id %d" % (len(xr), len(xids)))
print("live unrealized rows %d; z08 distinct accounts %d" % (len(un), len(live)))
print("z08 accounts present in the xref: %d; absent: %d (before, brief 2026-09-28: present 5670, absent 2362 of 8032)" % (len(live & xids), len(live - xids)))
sys.exit(0)
