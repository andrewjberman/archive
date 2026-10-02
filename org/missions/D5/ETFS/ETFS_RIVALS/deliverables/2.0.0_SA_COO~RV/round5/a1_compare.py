"""Compare the A1 frames produced at two pins over the same inputs (a1_at_pin.py output dirs)."""
import json
import sys

import pandas as pd

a_dir, b_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
KEYS = {"holding_contribution": ["fund_id", "period", "axis", "bucket"], "buying_trend": ["fund_id", "axis", "lean", "rank"],
        "input_census": ["date", "input_kind", "subject", "fund_id"]}
SKIP = {"produced_at", "revision", "dataset_revision"}
res = {}
for t, k in KEYS.items():
    a = pd.read_pickle(f"{a_dir}/{t}.pkl")
    b = pd.read_pickle(f"{b_dir}/{t}.pkl")
    m = a.merge(b, on=k, how="outer", suffixes=("_a", "_b"), indicator=True)
    cols = sorted((set(a.columns) & set(b.columns)) - set(k) - SKIP)
    changed = {}
    for c in cols:
        x, y = m[f"{c}_a"], m[f"{c}_b"]
        same = (x.astype(str) == y.astype(str)) | (x.isna() & y.isna())
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            same = same | ((x - y).abs() <= 1e-9 * pd.concat([x.abs(), y.abs()], axis=1).max(axis=1).clip(lower=1.0))
        n = int((~same & (m["_merge"] == "both")).sum())
        if n:
            changed[c] = n
    res[t] = {"rows_a": len(a), "rows_b": len(b), "unmatched": int((m["_merge"] != "both").sum()),
              "columns_added": sorted(set(b.columns) - set(a.columns)), "columns_removed": sorted(set(a.columns) - set(b.columns)),
              "values_compared": int((m["_merge"] == "both").sum()) * len(cols), "values_changed": changed}
print(json.dumps(res, indent=1))
json.dump(res, open(out, "w"), indent=1)
