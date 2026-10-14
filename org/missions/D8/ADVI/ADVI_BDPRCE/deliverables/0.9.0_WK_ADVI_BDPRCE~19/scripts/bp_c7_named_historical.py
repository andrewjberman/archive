#!/usr/bin/env python3
"""BP-c-7 value-only check against silver/historical_prices.parquet, 2026-10-09, with a shifted-price control.

Local copy: C:/dev/wk-bdprce-r2-7-data/historical_prices.parquet (the round-2 read; columns date, ticker, close,
fetch_date, source). The table carries NO asset_name, and the 1,859 lots carry no ticker (ticker_served is blank
for every one), so a close can be matched to a lot by VALUE only. A value-only match is not a trace and is never
classed; this check reports how many unexplained priced triples coincide with some close, against a shifted control.
Output: C:/dev/wk-bdprce-r3-19-data/classified/named_historical.json
Run from the worktree root:  python -I <this file>
"""
import json
import os
import sys

import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r3-19-data"
HIST = "C:/dev/wk-bdprce-r2-7-data/historical_prices.parquet"
SNAP_DATE = "2026-10-09"
TOL = 1e-6


def main():
    h = pd.read_parquet(HIST, columns=["date", "ticker", "close"])
    h = h[h["date"].astype(str).str[:10] == SNAP_DATE]
    closes = h["close"].dropna().to_numpy(dtype=float)
    cls = pd.read_csv(f"{DATA}/classified/lots_classified.csv", dtype=str, keep_default_na=False)
    u = cls[(cls["class"] == "UNEXPLAINED") & (cls["served_price"].str.lower() != "nan")
            & (cls["data_as_of"] == SNAP_DATE)]
    tri = u[["asset_name", "served_price"]].drop_duplicates()

    def hit(p):
        return bool(np.any(np.abs(closes - p) <= TOL * np.maximum(1.0, abs(p))))

    real = sum(hit(float(p)) for p in tri["served_price"])
    ctrl = sum(hit(float(p) + 0.37) for p in tri["served_price"])
    out = {"source": "silver/historical_prices.parquet (round-2 local copy)", "scope": SNAP_DATE,
           "historical_rows_on_scope_date": int(len(closes)), "triples_tested": int(len(tri)),
           "value_only_matches": int(real), "shift_control_matches": int(ctrl), "bindable_by_name": False,
           "note": "value-only; the table has no asset_name and the lots carry no ticker; not classed"}
    os.makedirs(f"{DATA}/classified", exist_ok=True)
    json.dump(out, open(f"{DATA}/classified/named_historical.json", "w"), indent=1)
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
