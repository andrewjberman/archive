#!/usr/bin/env python3
"""BP-b-3 census diagnostics: reads the extract and the downloaded sources (outside the checkout), prints counts only.
Used to state the CENSUS.md shape figures. Asset names are printed only where they carry the mapping gap (asset names
are not client data). No client_name, account_name or raw account id is read or printed.
Run from the worktree root:  python -I <this file> > <deliverable>/census_diagnostics.txt
"""
import json

import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r2-7-data"
EXT = f"{DATA}/lot_extract.csv"
CANON = f"{DATA}/canonical_prices.parquet"
LOOKUP = f"{DATA}/ticker_lookup.json"
CASH_RE = r"\bCASH\b|MONEY MARKET|\bMM\b|FDIC|SWEEP"


def main():
    ex = pd.read_csv(EXT, dtype=str, keep_default_na=False)
    print(f"EXTRACT rows={len(ex)} objects_with_lots={ex.object_key.nunique()}")
    print("EXTRACT price_class", ex.price_class.value_counts().to_dict())

    un = ex[ex.price_class != "NOT_UNTICKERED"].copy()
    print(f"UNTICKERED lots={len(un)} distinct_names={un.asset_name.nunique()} objects={un.object_key.nunique()}")

    cp = pd.read_parquet(CANON, columns=["asset_name", "ticker"])
    cn = set(cp.asset_name.dropna().unique())
    tk = cp.ticker.fillna("").astype(str).str.strip().str.upper()
    tk_names = set(cp.loc[(tk != "") & (tk != "UNKNOWN"), "asset_name"].dropna().unique())
    with open(LOOKUP, "r", encoding="utf-8") as fh:
        lk = json.load(fh)
    lk_names = {r["asset_name"]: r["ticker"] for r in lk
                if r.get("asset_name") and str(r.get("ticker", "")).strip().upper() not in ("", "UNKNOWN")}
    un_names = set(un.asset_name)
    print(f"NAMES untickered_in_canonical={len(un_names & cn)} untickered_in_canonical_with_ticker={len(un_names & tk_names)} "
          f"untickered_in_ticker_lookup={len(un_names & set(lk_names))} untickered_absent_from_canonical={len(un_names - cn)}")
    for n in sorted(un_names & set(lk_names)):
        print(f"LISTED asset={n} lookup_ticker={lk_names[n]} lots={int((un.asset_name == n).sum())}")

    cash = un.asset_name.str.upper().str.contains(CASH_RE, regex=True)
    off = un.price_class == "PRICED_OFF_NO_CANONICAL"
    print(f"CASH_HEURISTIC cash_like_lots={int(cash.sum())} cash_like_off={int((off & cash).sum())} "
          f"noncash_lots={int((~cash).sum())} noncash_off={int((off & ~cash).sum())}")

    off_rows = ex[ex.price_class == "PRICED_OFF_NO_CANONICAL"]
    print(f"OFF lots={len(off_rows)} by_entity_class={off_rows.entity_class.value_counts().to_dict()}")

    e = ex.copy()
    for c in ["quantity", "market_value", "current_price"]:
        e[c] = pd.to_numeric(e[c], errors="coerce")
    e = e[e.quantity.notna() & e.market_value.notna() & e.current_price.notna()].copy()
    e["qp"] = e.quantity * e.current_price
    tol = np.maximum(0.01, 1e-6 * e.market_value.abs())
    e["brk"] = (e.market_value - e.qp).abs() > tol
    b = e[e.brk].copy()
    print(f"MV_IDENTITY checked={len(e)} broken={len(b)} broken_by_class={b.price_class.value_counts().to_dict()}")
    print(f"MV_IDENTITY broken_with_market_value_zero={int((b.market_value == 0).sum())}")
    ratio = (b.qp / b.market_value.replace(0, np.nan)).dropna()
    print("MV_IDENTITY ratio_qp_over_mv_quantiles_05_25_50_75_95", [round(float(x), 4) for x in ratio.quantile([0.05, 0.25, 0.5, 0.75, 0.95])])

    dd = ex.drop_duplicates("object_key")[["object_key", "data_as_of"]]
    print(f"AS_OF_LOTS distinct_dates={dd.data_as_of.nunique()} min={dd.data_as_of.min()} max={dd.data_as_of.max()}")


if __name__ == "__main__":
    main()
