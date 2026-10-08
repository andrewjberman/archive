"""ETFS_RIVALS round 25 (RIV-rg-1) -- the before and after of every fund's tables, for the never-widen pair (CTO ruling msg
31428, term 2): the rankings and the 30d / 90d / 365d tables per fund, each moved figure named.

    python before_after_tables.py <code root> <page day> <real-run out dir> <out json>

BEFORE: the newest served object of gold holding_contribution and gold buying_trend at date=<page day> on S3 (read-only).
AFTER: the same two tables as the real run of the new code wrote them under <real-run out dir>/layer (local).
Rows are matched on (fund_id, period, axis, bucket). A figure "moves" when a compared column differs (numbers beyond 1e-12 absolute and 1e-9 relative: the control run of
unchanged code differs by ~1e-16 relative in summed dollars).
Meta columns (revision, produced_at, input_manifest, producer_version) are not compared."""
import collections
import glob
import io
import json
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, RUN, OUT = sys.argv[2], sys.argv[3].rstrip("/\\"), sys.argv[4]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import homes, revision, sinks  # noqa: E402

META = {"revision", "produced_at", "input_manifest", "producer_version"}
KEY = ["fund_id", "period", "axis", "bucket"]
PAGE_PERIODS = ("R30", "R90", "R365")
s = sinks.S3Sink()
rec = {"day": DAY, "tables": {}}


def same(a, b):
    if pd.isna(a) and pd.isna(b):
        return True
    try:
        fa, fb = float(a), float(b)
        return abs(fa - fb) <= max(1e-12, 1e-9 * max(abs(fa), abs(fb)))  # summation-order noise is ~1e-16 relative
    except (TypeError, ValueError):
        return str(a) == str(b)


def norm(v):
    if pd.isna(v):
        return None
    if isinstance(v, (bool, str)):
        return v
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


for table in ("holding_contribution", "buying_trend"):
    pre = homes.address("rivalfunds", "etfs", "gold", table, "date=" + DAY)
    bu = revision.newest([u for u in s.list(pre) if u.endswith(".parquet")])
    before = pd.read_parquet(io.BytesIO(s.get(bu)))
    local = sorted(glob.glob(RUN + "/layer/opal-data-etfs/rivalfunds/etfs/gold/" + table + "/date=" + DAY + "/*.parquet"))
    assert local, "the real run wrote no " + table
    after = pd.read_parquet(local[-1])
    key = [k for k in KEY if k in before.columns and k in after.columns]
    cols = [c for c in before.columns if c in after.columns and c not in META and c not in key]
    b = before.set_index(key)
    a = after.set_index(key)
    assert b.index.is_unique and a.index.is_unique, table + ": key not unique"
    only_b, only_a = b.index.difference(a.index), a.index.difference(b.index)
    both = b.index.intersection(a.index)
    moved = []
    per_col = collections.Counter()
    for k in both:
        rb, ra = b.loc[k], a.loc[k]
        d = {c: [rb[c], ra[c]] for c in cols if not same(rb[c], ra[c])}
        if d:
            for c in d:
                per_col[c] += 1
            moved.append({"key": [str(x) for x in (k if isinstance(k, tuple) else (k,))],
                          "name": str(ra.get("security_name", "")), "moved": {c: [norm(v[0]), norm(v[1])] for c, v in d.items()}})
    page = [m for m in moved if "period" not in key or m["key"][key.index("period")] in PAGE_PERIODS]
    by_fund = collections.Counter(m["key"][0] for m in page)
    by_period = collections.Counter(m["key"][key.index("period")] for m in moved) if "period" in key else {}
    rec["tables"][table] = {"before": bu, "after": local[-1], "rows_before": len(before), "rows_after": len(after), "key": key,
                            "compared_columns": cols, "rows_only_before": [list(map(str, k)) for k in only_b][:200],
                            "rows_only_after": [list(map(str, k)) for k in only_a][:200], "n_only_before": len(only_b), "n_only_after": len(only_a),
                            "rows_in_both": len(both), "rows_moved": len(moved), "rows_moved_on_page_periods": len(page),
                            "moved_by_column": dict(per_col), "moved_by_period": dict(by_period), "moved_by_fund_page_periods": dict(by_fund),
                            "moved": moved}
    print(f"{table}: rows {len(before)} -> {len(after)} | only before {len(only_b)} | only after {len(only_a)} | in both {len(both)} | "
          f"moved {len(moved)} (page periods {len(page)})")
    print("   by column:", dict(per_col))
    print("   by period:", dict(by_period))
    print("   by fund (30d / 90d / 365d):", dict(sorted(by_fund.items())))
    if table == "holding_contribution":
        big = sorted((m for m in page if "contribution" in m["moved"]), key=lambda m: -abs((m["moved"]["contribution"][1] or 0) - (m["moved"]["contribution"][0] or 0)))
        print("   largest contribution moves on the page periods (percentage points):")
        for m in big[:15]:
            c = m["moved"]["contribution"]
            rk = m["moved"].get("rank_best") or m["moved"].get("rank_worst")
            print(f"     {m['key'][0]} {m['key'][1]} {m['key'][3]:<22} {(c[0] or 0) * 100:+.3f} -> {(c[1] or 0) * 100:+.3f}  rank {rk}  {m['name'][:30]}")
        top = [m for m in page if any(c in m["moved"] for c in ("rank_best", "rank_worst"))
               and (min(x for x in (m["moved"].get("rank_best", [99, 99]) + m["moved"].get("rank_worst", [99, 99])) if x is not None) <= 10)]
        print(f"   rows of the page periods whose rank moves into or out of a top or bottom 10: {len(top)}")
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
