#!/usr/bin/env python3
"""BP-c-7 named-source check: Schwab RPS closing price (B_01 repricing path), account-level, with a negative control.

Source: schwab/silver/rps/date=20260723/data.parquet (the newest RPS partition listed; no partition covers 2026-10-09,
see surprise row ADVI_BDPRCE-D1-W19-S2). Mapping: gold/dimensions/schwab_bd_account_mapping.parquet, read the way
B_01.holdings_lots.py:581-589 reads it (last pair wins). The lot carries only sha12(BD account id) (account_ref), so the
join is account + price: a lot is a candidate when some RPS row for one of its accounts carries closing_price equal to
the served price (equity) or to the served price x 100 (bond, percent of par, B_01.holdings_lots.py:2223-2225).

Negative control: the same test with every served price shifted by +0.37. Matches beyond the control rate are the signal.
Positive control: 300 RPS rows are re-played as synthetic served prices; recall must be 300 of 300.
Output: C:/dev/wk-bdprce-r3-19-data/classified/named_rps.json (raw account ids are NOT written; sha12 only).
Run from the worktree root:  python -I <this file>
"""
import hashlib
import json
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r3-19-data"
R2 = "C:/dev/wk-bdprce-r2-7-data"
RPS_FILE = f"{DATA}/rps_20260723.parquet"
RPS_KEY = "schwab/silver/rps/date=20260723/data.parquet"
MAP_FILE = f"{DATA}/schwab_bd_mapping.parquet"
TOL = 1e-6


def sha12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def main():
    m = pd.read_parquet(MAP_FILE)
    cols = list(m.columns)
    bd_col = next((c for c in cols if "bd" in c.lower() and "account" in c.lower()), cols[0])
    sw_col = next((c for c in cols if "schwab" in c.lower()), cols[1])
    sw2bd = {str(sw).strip(): str(bd).strip() for bd, sw in zip(m[bd_col], m[sw_col])}
    print(f"OK: mapping pairs={len(sw2bd)} (bd={bd_col}, schwab={sw_col})")

    rps = pd.read_parquet(RPS_FILE, columns=["account_id", "ticker", "closing_price"])
    rps = rps[rps["closing_price"].notna() & (rps["closing_price"] > 0)].copy()
    rps["bd"] = rps["account_id"].astype(str).str.strip().map(sw2bd)
    rps = rps[rps["bd"].notna()].copy()
    rps["ref"] = rps["bd"].map(lambda b: sha12(b))
    print(f"OK: RPS priced rows={len(rps)} rows mapped to a BD account={len(rps)} "
          f"distinct BD accounts={rps['ref'].nunique()} partition={RPS_KEY}")

    # lots, per triple: the account refs that hold it
    lots = pd.read_csv(f"{R2}/lot_extract.csv", dtype=str, keep_default_na=False)
    lots = lots[lots["price_class"] == "PRICED_OFF_NO_CANONICAL"].copy()
    lots["p"] = pd.to_numeric(lots["current_price"], errors="coerce")
    # only triples the canonical and daily passes left UNEXPLAINED (lots_classified.csv, written by bp_c7_classify.py)
    cls = pd.read_csv(f"{DATA}/classified/lots_classified.csv", dtype=str, keep_default_na=False)
    unexpl = cls[cls["class"] == "UNEXPLAINED"]
    unexpl_keys = set(zip(unexpl["asset_name"], unexpl["served_price"], unexpl["data_as_of"]))
    in_unexpl = [k in unexpl_keys for k in zip(lots["asset_name"], lots["current_price"], lots["data_as_of"])]
    lots = lots[in_unexpl].copy()
    print(f"OK: unexplained lots entering RPS check={len(lots)} triples={len(unexpl_keys)}")
    tri_refs = lots.groupby(["asset_name", "current_price", "data_as_of"])["account_ref"].apply(lambda s: set(s))
    tri_p = lots.groupby(["asset_name", "current_price", "data_as_of"])["p"].first()

    # index RPS by ref
    by_ref = {k: g[["ticker", "closing_price"]].to_numpy() for k, g in rps.groupby("ref")}

    def hits(refs, price):
        out = []
        for r in refs:
            arr = by_ref.get(r)
            if arr is None:
                continue
            for tk, cp in arr:
                if abs(cp - price) <= TOL * max(1.0, abs(price)):
                    out.append((r, "equity", tk, cp))
                elif abs(cp - price * 100.0) <= TOL * max(1.0, abs(price * 100.0)):
                    out.append((r, "bond_pct_par", tk, cp))
        return out

    # positive control: replay 300 RPS rows as served prices
    sample = rps.sample(n=300, random_state=20261014)
    pc_ok = 0
    for r in sample.itertuples(index=False):
        if hits({r.ref}, float(r.closing_price)):
            pc_ok += 1
    print(f"OK: positive control recall={pc_ok} of 300")

    matched, control_matched = {}, 0
    n_tri = 0
    n_lots_nan = 0
    for key, refs in tri_refs.items():
        p = tri_p.loc[key]
        if np.isnan(p):
            n_lots_nan += len(lots[(lots.asset_name == key[0]) & (lots.current_price == key[1]) & (lots.data_as_of == key[2])])
            continue
        n_tri += 1
        h = hits(refs, p)
        if h:
            matched[key] = h
        if hits(refs, p + 0.37):
            control_matched += 1
    print(f"OK: priced triples tested={n_tri} (NaN-price lots excluded={n_lots_nan})")
    print(f"RPS ACCOUNT+PRICE: triples matched={len(matched)} of {n_tri}; "
          f"negative-control (shifted +0.37) matched={control_matched} of {n_tri}")
    kinds = Counter(h[0][1] for h in matched.values())
    print("match kinds (first hit per triple)", dict(kinds))
    out = {
        "source": RPS_KEY, "mapping": "gold/dimensions/schwab_bd_account_mapping.parquet",
        "triples_tested": n_tri, "triples_matched": len(matched), "control_matched": control_matched,
        "positive_control_recall": f"{pc_ok} of 300",
        "matches": [
            {"asset_name": k[0], "served_price": k[1], "data_as_of": k[2], "n_hits": len(v),
             "first_hit": {"account_ref": v[0][0], "kind": v[0][1], "ticker": str(v[0][2]), "closing_price": float(v[0][3])}}
            for k, v in sorted(matched.items())
        ],
    }
    import os
    os.makedirs(f"{DATA}/classified", exist_ok=True)
    json.dump(out, open(f"{DATA}/classified/named_rps.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
