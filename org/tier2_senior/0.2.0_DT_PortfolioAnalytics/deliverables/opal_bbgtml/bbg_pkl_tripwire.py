"""OPAL_BBGTML leg-2 tripwire -- light cleanliness/expected-shape checks on the two
daily Bloomberg PKLs BEFORE anything ships to the /data-refresh channel.

A TRIPWIRE, not a parser (Andrew, 2026-07-15): the scripts and the BBG shape are
stable, so this only trips on the failure modes worth stopping an upload for:
  - file missing / not a pickle / not the expected dict
  - top-level keys drifted
  - duplicated (date, index) rows
  - as-of date not the expected business day (stale or mis-dated run)
  - a frame that shrank below the pinned floor (truncated pull) or exploded

Runs LOCALLY on the terminal machine (pre-send). The m365 gateway never unpickles
(unpickling is code execution; the gateway also carries no pandas by design) --
gateway-side checks are structural only (filename/date/size).

Pins measured from the 2026-07-10 vintage (data 8.5MB / model 17.1MB).
Update PINS deliberately when Yang changes the notebooks -- a pin edit is a
declaration that the shape change is intended.

Usage:
    python bbg_pkl_tripwire.py <output_dir> [--date YYYYMMDD] [--allow-stale N]

Exit 0 = PASS (safe to send). Exit 1 = FAIL (do not send; read the reasons).
No non-ASCII in output (CLAUDE.md code-quality rule).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pickle
import sys

import pandas as pd

# ---------------------------------------------------------------------------
# Pins (2026-07-10 vintage). floor = measured * 0.98 rounded down; ceil = x1.5.
# Daily history grows, so floors only ratchet UP over time.
# ---------------------------------------------------------------------------
DATA_KEYS = {"return_daily", "return_monthly", "price_monthly", "asset_correlations"}
CORR_WINDOWS = {"1M", "2M", "3M", "6M", "1Y"}
MODEL_KEYS = {
    "holdings", "benchmark_holdings", "etf_returns", "etf_characteristics",
    "factor_spreads", "model_returns", "benchmark_returns", "factor_spread",
    "model_correlations", "factor_correlations", "combined", "regression", "summary",
}
# 2026-08-04 rename mirror (LTC->LT / LTA->ULT, MSTR route-out 225204Z; sitez twin fixed live
# under the /terminal-upload fire authorization -- keep both twins in lockstep on any edit).
REGRESSION_MODELS = {"UST", "ST", "INT", "LT", "ULT"}
# Yang's index_name values for the five models (spelling pinned AS-IS from the data).
# Post-rename source spellings per DS live workbook check @89a3cca5ed: 'Long Term' /
# 'Ultra Long Term' (unhyphenated; the 'Agressive' typo retired with the source series).
# LAYER NOTE (MSTR 230727Z + artifact adjudication 232036Z): THREE distinct name layers
# exist and only this one is validated here -- (1) pkl index_name, unhyphenated, pinned
# above; (2) served JSON display strings, currently 'Ultra-Short Term'/'Ultra-Long Term'
# (DIVERGENT from canon, producer fix at DS next-seam); (3) rendered display, DE typing
# canon @02b7f351 ('Ultra Short-Term'/'Ultra Long-Term', hyphen joins Term) via the FE
# displayModelName() render-boundary resolver. A validator comparing any two layers'
# strings byte-wise will manufacture a false mismatch; compare within a layer only.
MODEL_INDEX_NAMES = {
    "Ultra Short Term", "Short Term", "Intermediate Term",
    "Long Term", "Ultra Long Term",
}
ROW_PINS = {  # frame -> (floor, ceiling)
    ("data", "return_daily"):   (107000, 165000),
    ("data", "return_monthly"): (28400, 43500),
    ("data", "price_monthly"):  (29500, 45300),
    ("model", "etf_returns"):   (75000, 115000),
    ("model", "model_returns"): (6700, 10400),
    ("model", "holdings"):      (1400, 2300),
}
SUMMARY_SHAPE = (25, 10)  # 5 models x 5 windows, 10 stat columns


def expected_asof(run_date: dt.date, allow_stale: int = 0) -> set:
    """The notebooks pin date_end = run day - 1 business day. allow_stale N widens
    the acceptable set by N further business days (US market holidays -- BDay does
    not know the exchange calendar, so the day after a holiday needs --allow-stale 1)."""
    out = set()
    anchor = pd.Timestamp(run_date)
    for back in range(1, 2 + allow_stale):
        out.add((anchor - pd.tseries.offsets.BDay(back)).date())
    return out


def _fail(reasons: list, msg: str) -> None:
    reasons.append(msg)
    print("FAIL: " + msg)


def _ok(msg: str) -> None:
    print("OK:   " + msg)


def _check_dupes(df: pd.DataFrame, subset: list, label: str, reasons: list) -> None:
    if not set(subset).issubset(df.columns):
        return  # columns drifted -> the key/column checks already flag structure
    n = int(df.duplicated(subset=subset).sum())
    if n:
        _fail(reasons, f"{label}: {n} duplicated {subset} rows")
    else:
        _ok(f"{label}: no duplicate {subset} rows")


def _check_rows(kind: str, name: str, df: pd.DataFrame, reasons: list) -> None:
    pin = ROW_PINS.get((kind, name))
    if not pin:
        return
    lo, hi = pin
    if not (lo <= len(df) <= hi):
        _fail(reasons, f"{kind}.{name}: {len(df)} rows outside pinned band [{lo}, {hi}]")
    else:
        _ok(f"{kind}.{name}: {len(df)} rows within band [{lo}, {hi}]")


def check_data_pkl(path: str, asof_ok: set, reasons: list) -> None:
    with open(path, "rb") as f:
        d = pickle.load(f)
    if not isinstance(d, dict) or set(d.keys()) != DATA_KEYS:
        _fail(reasons, f"data pkl keys drifted: {sorted(d.keys()) if isinstance(d, dict) else type(d).__name__}")
        return
    _ok("data pkl: top-level keys exact")
    if set(d["asset_correlations"].keys()) != CORR_WINDOWS:
        _fail(reasons, f"asset_correlations windows drifted: {sorted(d['asset_correlations'].keys())}")
    for name in ("return_daily", "return_monthly", "price_monthly"):
        df = d[name]
        _check_rows("data", name, df, reasons)
        _check_dupes(df, ["date", "index_name"], f"data.{name}", reasons)
    rd = d["return_daily"]
    missing = MODEL_INDEX_NAMES - set(rd["index_name"].unique())
    if missing:
        _fail(reasons, f"model tickers missing from return_daily: {sorted(missing)}")
    else:
        _ok("data.return_daily: all 5 model portfolios present")
    maxd = pd.to_datetime(rd["date"]).max().date()
    if maxd not in asof_ok:
        _fail(reasons, f"data as-of {maxd} not in expected {sorted(str(x) for x in asof_ok)} "
                       "(if yesterday was a US market holiday, rerun with --allow-stale 1)")
    else:
        _ok(f"data as-of {maxd} matches expected business day")


def check_model_pkl(path: str, asof_ok: set, reasons: list) -> None:
    with open(path, "rb") as f:
        d = pickle.load(f)
    if not isinstance(d, dict) or set(d.keys()) != MODEL_KEYS:
        _fail(reasons, f"model pkl keys drifted: {sorted(d.keys()) if isinstance(d, dict) else type(d).__name__}")
        return
    _ok("model pkl: top-level keys exact (13)")
    if set(d["regression"].keys()) != REGRESSION_MODELS:
        _fail(reasons, f"regression models drifted: {sorted(d['regression'].keys())}")
    else:
        _ok("model.regression: UST/ST/INT/LTC/LTA present")
    if tuple(d["summary"].shape) != SUMMARY_SHAPE:
        _fail(reasons, f"model.summary shape {d['summary'].shape} != pinned {SUMMARY_SHAPE}")
    else:
        _ok(f"model.summary: shape {SUMMARY_SHAPE} exact")
    for name in ("etf_returns", "model_returns", "holdings"):
        _check_rows("model", name, d[name], reasons)
    er = d["etf_returns"]
    if {"date", "ticker"}.issubset(er.columns):
        _check_dupes(er, ["date", "ticker"], "model.etf_returns", reasons)
    date_col = "date" if "date" in er.columns else None
    if date_col:
        maxd = pd.to_datetime(er[date_col]).max().date()
        if maxd not in asof_ok:
            _fail(reasons, f"model as-of {maxd} not in expected {sorted(str(x) for x in asof_ok)} "
                           "(if yesterday was a US market holiday, rerun with --allow-stale 1)")
        else:
            _ok(f"model as-of {maxd} matches expected business day")


def main() -> int:
    ap = argparse.ArgumentParser(description="OPAL_BBGTML PKL tripwire")
    ap.add_argument("output_dir", help="the project output/ directory holding the PKLs")
    ap.add_argument("--date", default=None, help="vintage YYYYMMDD (default: the notebooks' "
                                                 "own rule, run day - 1 business day)")
    ap.add_argument("--allow-stale", type=int, default=0,
                    help="accept an as-of up to N business days older (US holiday runs)")
    args = ap.parse_args()

    today = dt.date.today()
    if args.date:
        stamp = args.date
        vintage = dt.datetime.strptime(stamp, "%Y%m%d").date()
        asof_ok = {vintage} | expected_asof(today, args.allow_stale)
    else:
        stamp = (pd.Timestamp(today) - pd.tseries.offsets.BDay(1)).strftime("%Y%m%d")
        asof_ok = expected_asof(today, args.allow_stale)

    data_path = os.path.join(args.output_dir, f"data {stamp} v1.pkl")
    model_path = os.path.join(args.output_dir, f"model {stamp} v1.pkl")

    print(f"TRIPWIRE: vintage {stamp}")
    reasons: list = []
    for label, path, fn in (("data", data_path, check_data_pkl),
                            ("model", model_path, check_model_pkl)):
        if not os.path.exists(path):
            _fail(reasons, f"{label} pkl missing: {path}")
            continue
        size_mb = os.path.getsize(path) / 1e6
        if size_mb < 1:
            _fail(reasons, f"{label} pkl suspiciously small: {size_mb:.1f} MB")
        try:
            fn(path, asof_ok, reasons)
        except Exception as e:  # unreadable pickle, pandas mismatch, etc.
            _fail(reasons, f"{label} pkl unreadable: {type(e).__name__}: {e}")

    print()
    if reasons:
        print(f"RESULT: FAIL ({len(reasons)} issue(s)) -- DO NOT SEND. Fix or rerun the pull first.")
        return 1
    print("RESULT: PASS -- both PKLs safe to send (/bbg-send).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
