#!/usr/bin/env python3
"""BP-c-7 named-source check: gold canonical holdings snapshot (the HLOT2 re-open price, B_01 lines 1168-1334).

Source: gold/canonical/holdings/2026-10-09.parquet (the snapshot for the 2026-10-09 data_as_of, read from
C:/dev/wk-bdprce-r3-19-data/holdings_20261009.parquet). B_01.holdings_lots.py:1169 keys it by snapshot date; the
re-open lot takes the holdings row's `price` (B_01.holdings_lots.py:1288-1334).

Binding: asset_name (exact, a name key in the source itself) + account (sha12 of the BD account id equals the lot's
account_ref) + exact price. Bond percent-of-par is also tested (served = price/100 or served = price x 100).
Negative control: served price shifted by +0.37. Positive control: 300 holdings rows replayed as served prices.
Scope: only triples with data_as_of 2026-10-09 (the snapshot in hand); other dates are reported as not read.
Output: C:/dev/wk-bdprce-r3-19-data/classified/named_holdings.json (no raw account id written; sha12 only).
Run from the worktree root:  python -I <this file>
"""
import hashlib
import json
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r3-19-data"
R2 = "C:/dev/wk-bdprce-r2-7-data"
SNAP_FILE = f"{DATA}/holdings_20261009.parquet"
SNAP_KEY = "gold/canonical/holdings/2026-10-09.parquet"
SNAP_DATE = "2026-10-09"
TOL = 1e-6


def sha12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def close(a, b):
    return np.abs(a - b) <= TOL * np.maximum(1.0, np.abs(b))


def main():
    h = pd.read_parquet(SNAP_FILE, columns=["account_id", "asset_name", "price", "source"])
    h = h[h["price"].notna() & (h["price"] > 0)].copy()
    h["ref"] = h["account_id"].astype(str).str.strip().map(sha12)
    h["name"] = h["asset_name"].astype(str)
    print(f"OK: snapshot={SNAP_KEY} priced rows={len(h)} distinct refs={h['ref'].nunique()}")

    cls = pd.read_csv(f"{DATA}/classified/lots_classified.csv", dtype=str, keep_default_na=False)
    unexpl = cls[(cls["class"] == "UNEXPLAINED") & (cls["served_price"].str.lower() != "nan")]
    unexpl = unexpl[unexpl["data_as_of"] == SNAP_DATE]
    not_read = cls[(cls["class"] == "UNEXPLAINED") & (cls["data_as_of"] != SNAP_DATE)]
    print(f"OK: unexplained priced triples at {SNAP_DATE} lots={len(unexpl)}; "
          f"unexplained lots at other as-of dates (not read here)={len(not_read)}")

    # account refs present in the extract, to keep the join to the lot population
    refs_all = set(cls["account_ref"])
    h = h[h["ref"].isin(refs_all)].copy()
    print(f"OK: holdings rows whose account_ref is in the extract={len(h)}")

    by_name = {k: g[["ref", "price", "source"]].to_numpy() for k, g in h.groupby("name")}

    def match(name, refs, served, conv=("eq",)):
        arr = by_name.get(name)
        if arr is None:
            return []
        out = []
        for ref, price, source in arr:
            if ref not in refs:
                continue
            ok = False
            if "eq" in conv and close(served, price):
                ok = True
            if "x100" in conv and close(served, price * 100.0):
                ok = True
            if "div100" in conv and close(served, price / 100.0):
                ok = True
            if ok:
                out.append((ref, float(price), source))
        return out

    tri = unexpl.groupby(["asset_name", "served_price"])["account_ref"].apply(lambda s: set(s)).reset_index()
    tested = 0
    matched = {}
    ctrl = 0
    for r in tri.itertuples(index=False):
        p = float(r.served_price)
        tested += 1
        hits = match(r.asset_name, set(r.account_ref), p, ("eq", "x100", "div100"))
        if hits:
            matched[(r.asset_name, r.served_price)] = hits
        if match(r.asset_name, set(r.account_ref), p + 0.37, ("eq", "x100", "div100")):
            ctrl += 1

    # positive control: replay 300 holdings rows as served prices
    sample = h.sample(n=min(300, len(h)), random_state=20261014)
    pc = sum(1 for s in sample.itertuples(index=False)
             if match(s.name, {s.ref}, float(s.price), ("eq",)))

    src = Counter(v[0][2] for v in matched.values())
    print(f"OK: positive control recall={pc} of {len(sample)}")
    print(f"HOLDINGS NAME+ACCOUNT+PRICE: triples tested={tested} matched={len(matched)} "
          f"negative-control(+0.37) matched={ctrl}")
    print("source label of first hit per matched triple", dict(src))
    out = {
        "source": SNAP_KEY, "data_as_of_scope": SNAP_DATE, "triples_tested": tested,
        "triples_matched": len(matched), "control_matched": ctrl,
        "positive_control_recall": f"{pc} of {len(sample)}",
        "matches": [
            {"asset_name": k[0], "served_price": k[1], "data_as_of": SNAP_DATE, "n_hits": len(v),
             "first_hit": {"account_ref": v[0][0], "holdings_price": v[0][1], "source_label": str(v[0][2])}}
            for k, v in sorted(matched.items())
        ],
    }
    os.makedirs(f"{DATA}/classified", exist_ok=True)
    json.dump(out, open(f"{DATA}/classified/named_holdings.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
