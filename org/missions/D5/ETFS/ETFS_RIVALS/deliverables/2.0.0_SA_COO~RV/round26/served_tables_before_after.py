"""ETFS_RIVALS round 26 deploy -- the three A1 tables of the page day, the object the republish wrote against the object
served before it, row for row (COO half: one moved row is a rollback; CTO half C2).

    python served_tables_before_after.py <code root> <page day> <out json>

Read-only on S3. For holding_contribution, buying_trend and input_census at date=<page day>: lists the objects, takes
the newest and the one before it by `revision.newest`, and compares them on every column except the ones that name the
build (revision, produced_at, input_manifest, producer_version). Numbers within 1e-12 absolute or 1e-9 relative are equal
(summation order). Rows are matched on a key when one is unique, else compared as sorted multisets."""
import io
import json
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, OUT = sys.argv[2], sys.argv[3]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import homes, revision, sinks  # noqa: E402

META = {"revision", "produced_at", "input_manifest", "producer_version"}
KEYS = (("fund_id", "period", "axis", "bucket"), ("fund_id", "kind", "security_id", "date"), ("fund_id", "kind", "key"))
s = sinks.S3Sink()
rec = {"day": DAY, "tables": {}}


def same(a, b):
    if pd.isna(a) and pd.isna(b):
        return True
    try:
        fa, fb = float(a), float(b)
        return abs(fa - fb) <= max(1e-12, 1e-9 * max(abs(fa), abs(fb)))
    except (TypeError, ValueError):
        return str(a) == str(b)


worst = 0
for table in ("holding_contribution", "buying_trend", "input_census"):
    pre = homes.address("rivalfunds", "etfs", "gold", table, "date=" + DAY)
    us = [u for u in s.list(pre) if u.endswith(".parquet")]
    new = revision.newest(us)
    old = revision.newest([u for u in us if u != new])
    a, b = pd.read_parquet(io.BytesIO(s.get(old))), pd.read_parquet(io.BytesIO(s.get(new)))
    cols = [c for c in a.columns if c in b.columns and c not in META]
    key = next((k for k in KEYS if all(c in a.columns and c in b.columns for c in k) and not a.duplicated(list(k)).any()
                and not b.duplicated(list(k)).any()), None)
    r = {"objects": len(us), "before": old.rsplit("/", 1)[-1], "after": new.rsplit("/", 1)[-1], "rows_before": len(a), "rows_after": len(b),
         "columns_compared": len(cols), "columns_only_before": sorted(set(a.columns) - set(b.columns)),
         "columns_only_after": sorted(set(b.columns) - set(a.columns)), "key": list(key) if key else None}
    if key:
        ai, bi = a.set_index(list(key)), b.set_index(list(key))
        both = ai.index.intersection(bi.index)
        moved = {}
        for c in [c for c in cols if c not in key]:
            n = sum(1 for x, y in zip(ai.loc[both, c], bi.loc[both, c]) if not same(x, y))
            if n:
                moved[c] = n
        rows_moved = sum(1 for k in both if any(not same(ai.loc[k, c], bi.loc[k, c]) for c in moved)) if moved else 0
        r.update({"only_before": int(len(ai.index.difference(bi.index))), "only_after": int(len(bi.index.difference(ai.index))),
                  "rows_in_both": int(len(both)), "moved_by_column": moved, "rows_moved": int(rows_moved)})
        bad = r["only_before"] + r["only_after"] + r["rows_moved"]
    else:
        sa = a[cols].astype(str).sort_values(cols).reset_index(drop=True)
        sb = b[cols].astype(str).sort_values(cols).reset_index(drop=True)
        eq = len(sa) == len(sb) and bool((sa.values == sb.values).all())
        r.update({"equal_as_sorted_rows": bool(eq)})
        bad = 0 if eq else max(len(a), len(b))
    worst += bad
    rec["tables"][table] = r
    print(table, json.dumps(r)[:520])
rec["rows_moved_or_unmatched_total"] = worst
print("TOTAL rows moved or unmatched across the three tables:", worst)
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1)
