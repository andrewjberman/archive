"""IB-er-191 AC1 -- the 49F engine's served twr_daily carries no OK day with r_net <= -1 (NEW-01 class, rows S177/S181).

Usage: python e19_ac1_no_impossible_day.py [s3 root, default the registry's served root]
Reads every twr_daily partition from 2026-01-01 (read-only) and counts OK rows with r_net <= -1.0.
Measured at the cut (2026-09-28): 26 such rows across 22 accounts, including the NEW-01 account's 2026-04-16
(bmv 13,360.59, emv 0.0, cf_net 0.0). A holdings-based daily return (Andrew-direct call 3) cannot reach -1 while any
position keeps a price. Pass: 0 such rows, and the NEW-01 account's 2026-04-16 row is not OK at -1.0.
"""
import io
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3
import pandas as pd

BUCKET, ROOT = "opal-data-49financial", "gold/advi"
root = sys.argv[1] if len(sys.argv) > 1 else ROOT
prefix = root.rstrip("/") + "/canonical/twr_daily/"
NEW01 = "0049615236"
s3 = boto3.client("s3")


def days():
    out, kw = [], dict(Bucket=BUCKET, Prefix=prefix, Delimiter="/")
    while True:
        r = s3.list_objects_v2(**kw)
        out += [c["Prefix"][len(prefix) + 5:-1] for c in r.get("CommonPrefixes", [])]
        if not r.get("IsTruncated"):
            return sorted(d for d in out if d >= "2026-01-01")
        kw["ContinuationToken"] = r["NextContinuationToken"]


def read(day):
    raw = s3.get_object(Bucket=BUCKET, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()
    f = pd.read_parquet(io.BytesIO(raw), columns=["account_id", "status", "r_net"])
    return f[(f["status"] == "OK") & f["r_net"].notna() & (f["r_net"] <= -1.0)].assign(day=day)


ds = days()
with ThreadPoolExecutor(16) as pool:
    bad = pd.concat(list(pool.map(read, ds)))
new01 = bad[(bad["account_id"] == NEW01) & (bad["day"] == "2026-04-16")]
print("partitions read: %d (%s..%s) | OK rows with r_net <= -1: %d across %d accounts | NEW-01 04-16 among them: %s"
      % (len(ds), ds[0], ds[-1], len(bad), bad["account_id"].nunique(), bool(len(new01))))
ok = len(bad) == 0 and len(new01) == 0
if ok:
    print("E19-AC1 PASS")
else:
    print("E19-AC1 FAIL")
sys.exit(0 if ok else 1)
