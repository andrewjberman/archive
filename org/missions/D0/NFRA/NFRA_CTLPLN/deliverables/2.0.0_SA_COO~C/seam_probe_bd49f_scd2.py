"""Issuer seam probe for CT-cl-1 (read-only): fold the stored 49F dim (date=2026-09-28)
against a 'today' frame carrying the same rows with flat_fee as int64, using the converter file
given as argv[1]. Prints CHANGED=<n> of <open accounts>, plus a control with one real change.
ASCII only. No writes to S3.
"""
import importlib.util
import io
import sys

import boto3
import pandas as pd

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("conv_under_test", path)
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)

s3 = boto3.client("s3", region_name="us-east-1")
key = bd.PFX + "/silver/" + bd.DIM_TABLE + "/date=2026-09-28/data.parquet"
prev = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bd.MONOLITH, Key=key)["Body"].read()))
cur = prev[prev["is_current"]].copy()
print("PREV rows", len(prev), "open", len(cur), "flat_fee dtype", prev["flat_fee"].dtype)

tod = cur.copy()
ff = tod["flat_fee"]
integral = bool(ff.notna().all() and (ff == ff.round()).all())
print("flat_fee all non-null and integral:", integral)
if integral:
    tod["flat_fee"] = ff.astype("int64")
print("TODAY flat_fee dtype", tod["flat_fee"].dtype)


def changed(out_rows, n_open):
    return int((~out_rows["is_current"]).sum() - int((~prev["is_current"]).sum())), n_open


out = bd.scd2_fold(prev, tod, "2026-10-19")
newly_closed = int((~out["is_current"]).sum()) - int((~prev["is_current"]).sum())
print("FOLD same-rows: newly_closed=%d of %d open; total rows %d (prev %d)"
      % (newly_closed, len(cur), len(out), len(prev)))

ctl = tod.copy()
i = ctl.index[0]
base = ctl.at[i, "flat_fee"]
ctl["flat_fee"] = ctl["flat_fee"].astype("float64")
ctl.at[i, "flat_fee"] = float(base) + 25.0
if integral:
    ctl["flat_fee"] = ctl["flat_fee"].map(lambda v: v)  # keep float; int vs float is the fix under test
out2 = bd.scd2_fold(prev, ctl, "2026-10-19")
newly2 = int((~out2["is_current"]).sum()) - int((~prev["is_current"]).sum())
print("CONTROL one real flat_fee change: newly_closed=%d (fixed file must read 1; unfixed reads all)" % newly2)
