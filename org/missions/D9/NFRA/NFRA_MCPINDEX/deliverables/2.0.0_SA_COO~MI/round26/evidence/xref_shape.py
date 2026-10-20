"""Shape of the xref gap (counts and patterns only; no account id is printed)."""
import re
from collections import Counter

import pyarrow.fs as pafs
import pyarrow.parquet as pq

A, B = "opal-data-assets", "opal-data-bd"
fs = pafs.S3FileSystem(region="us-east-1")


def read_all(bucket, key):
    with fs.open_input_file("%s/%s" % (bucket, key)) as f:
        return pq.read_table(f)


xt = read_all(A, "blackdiamond/49f/silver/dim_account_xref/date=2026-10-19/data.parquet")
print("xref columns:", xt.schema.names)
ut = read_all(B, "silver/unrealized/2026-10-16.parquet")
print("unrealized columns:", ut.schema.names[:14])
xids = {str(v) for v in xt.column("bd_account_id").to_pylist()}
live = {str(v) for v in ut.column("account_id").to_pylist() if str(v).startswith("z08")}
absent = live - xids


def shape(s):
    return re.sub(r"[0-9]", "9", re.sub(r"[A-Za-z]", "a", s))


print("shape of present ids :", Counter(shape(s) for s in (live & xids)).most_common(4))
print("shape of absent ids  :", Counter(shape(s) for s in absent).most_common(4))
print("shape of xref ids    :", Counter(shape(s) for s in xids).most_common(4))
# does an absent id appear in any other xref column?
hit = Counter()
for name in xt.schema.names:
    vals = {str(v) for v in xt.column(name).to_pylist()}
    n = len(absent & vals)
    if n:
        hit[name] = n
print("absent ids found in other xref columns:", dict(hit))
# unrealized rows per absent vs present account
cnt = Counter()
accts = ut.column("account_id").to_pylist()
for a in accts:
    a = str(a)
    if a in absent:
        cnt["rows_absent"] += 1
    elif a in live:
        cnt["rows_present"] += 1
print("unrealized rows for absent accounts %d, for present accounts %d" % (cnt["rows_absent"], cnt["rows_present"]))
