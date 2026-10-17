"""Read-only: how big are the landed gold external flows against the account's value, and how are those account-days graded (counts and ratios only)."""
import collections
import io
import sys

import boto3
import pyarrow.parquet as pq

DAY = sys.argv[1]
s3 = boto3.client("s3")
B, P = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/"
key = [o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix=P + "date=%s/" % DAY).get("Contents", []) if o["Key"].endswith(".parquet")][0]
t = pq.read_table(io.BytesIO(s3.get_object(Bucket=B, Key=key)["Body"].read()))
print("columns", [c for c in t.column_names])
rows = t.to_pylist()
fl = [r for r in rows if abs(r["external_flow"] or 0) > 1e-9]
ratios = sorted(abs(r["external_flow"]) / r["market_value_eod"] for r in fl if r["market_value_eod"])
print(DAY, "flow accounts", len(fl), "quality", dict(collections.Counter(r["day_quality"] for r in fl)))
print("|flow| / market value: min %.3f median %.3f max %.3f" % (ratios[0], ratios[len(ratios) // 2], ratios[-1]), "| share above 1.0:", sum(1 for x in ratios if x > 1.0), "of", len(ratios))
noflow = [r for r in rows if abs(r["external_flow"] or 0) <= 1e-9]
print("no-flow accounts", len(noflow), "quality", dict(collections.Counter(r["day_quality"] for r in noflow)))
