"""IB-er-191 AC2 -- every twr_daily partition carries its value columns (row W61-S2).

Usage: python e19_ac2_value_columns.py [s3 root, default the registry's served root]
Measured at the cut (2026-09-28): date=2024-07-08 and date=2025-01-09 lack bmv/emv/cf_net while their neighbours
carry them, all schema_version 1.2; the adapter's schema guard then refuses every full-history (Since-inception) read.
Arm A: both named partitions carry bmv, emv and r_net. Arm B (control): a neighbour, date=2025-01-10, still does.
"""
import io
import sys

import boto3
import pyarrow.parquet as pq

BUCKET, ROOT = "opal-data-49financial", "gold/advi"
root = sys.argv[1] if len(sys.argv) > 1 else ROOT
prefix = root.rstrip("/") + "/canonical/twr_daily/"
NEED = ("bmv", "emv", "r_net")
s3 = boto3.client("s3")
ok = True
for day in ("2024-07-08", "2025-01-09", "2025-01-10"):
    raw = s3.get_object(Bucket=BUCKET, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()
    cols = pq.read_schema(io.BytesIO(raw)).names
    missing = [c for c in NEED if c not in cols]
    print("%s missing %s" % (day, missing))
    ok = ok and not missing
if ok:
    print("E19-AC2 PASS")
else:
    print("E19-AC2 FAIL")
sys.exit(0 if ok else 1)
