"""MDLP_VOLAUD.001 -- ETF vs INDEX benchmark volatility audit (read-only probe).

Pulls latest data.pkl + published model_portfolio_benchmarks.json; mirrors the
Lambda's get_term_returns + calculate_period_returns + calculate_volatility
methodology to produce AC1-AC5 evidence tables for the audit brief.

No artifact write. No Lambda invoke. Output is structured JSON to stdout +
optional --out tabular files for the brief.

Author: 0.4.0_DS_ClientPlatform~B
TO: MDLP_VOLAUD.001 (CTO 2026-05-19)
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
from datetime import timedelta

import boto3
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

BUCKET = "opal-data-portal-v2"
LATEST_KEY = "benchmarks/LATEST.json"
PUBLISHED_KEY = "json/benchmarks/model_portfolio_benchmarks.json"
INCEPTION_DATE = "2024-04-30"

MODEL_CODES = ["UST", "ST", "INT", "LTC", "LTA"]
PERIODS = ["1D", "WTD", "MTD", "1M", "QTD", "1Q", "YTD", "1Y", "Since Inception"]

INDEX_NAME_MAP = {
    "UST": {"model": "Ultra Short Term",
            "index_benchmark": "Ultra Short Term Benchmark",
            "etf_benchmark": "Ultra Short Term ETF"},
    "ST":  {"model": "Short Term",
            "index_benchmark": "Short Term Benchmark",
            "etf_benchmark": "Short Term ETF"},
    "INT": {"model": "Intermediate Term",
            "index_benchmark": "Intermediate Term Benchmark",
            "etf_benchmark": "Intermediate Term ETF"},
    "LTC": {"model": "Long Term Conservative",
            "index_benchmark": "Long Term Benchmark",
            "etf_benchmark": "Long Term ETF"},
    "LTA": {"model": "Long Term Agressive",
            "index_benchmark": "Long Term Benchmark",
            "etf_benchmark": "Long Term ETF"},
}


def s3():
    return boto3.client("s3", region_name="us-east-1")


def load_pickle() -> tuple[dict, str]:
    """Resolve LATEST.json -> data_pkl + load it."""
    latest = json.loads(s3().get_object(
        Bucket=BUCKET, Key=LATEST_KEY)["Body"].read())
    data_key = latest["data_pkl"]
    body = s3().get_object(Bucket=BUCKET, Key=data_key)["Body"].read()
    return pickle.loads(body), data_key


def get_term_returns(data_pkl: dict) -> pd.DataFrame:
    """Mirror Lambda lambda_function.py:333-367 exactly."""
    return_daily = data_pkl["return_daily"].copy()
    term_data = return_daily[
        return_daily["index_name"].str.contains("Term", na=False)].copy()
    term_data["date"] = pd.to_datetime(term_data["date"])
    term_data = term_data[term_data["date"].dt.weekday < 5]
    pivoted = term_data.pivot(
        index="date", columns="index_name", values="return")
    pivoted = pivoted.sort_index()
    pivoted = pivoted.loc[(pivoted.fillna(0) != 0).any(axis=1)]
    return pivoted


def calculate_volatility(returns_pct: pd.Series, min_points: int = 5
                          ) -> float | None:
    """Mirror Lambda lambda_function.py:470-477 exactly."""
    returns_decimal = returns_pct.dropna().values / 100
    if len(returns_decimal) < min_points:
        return None
    daily_std = np.std(returns_decimal, ddof=1)
    annualized = daily_std * np.sqrt(252)
    return round(annualized * 100, 2)


def period_slice(series: pd.Series, end_date, period: str) -> pd.Series:
    """Mirror Lambda lambda_function.py:370-443 -- the period-slice logic."""
    series = series[series.index <= end_date]
    inception = pd.to_datetime(INCEPTION_DATE)
    if period == "1D":
        # Vol uses tail(20), not tail(1) -- special case in Lambda
        return series.tail(20)
    elif period == "WTD":
        monday = end_date - timedelta(days=end_date.weekday())
        return series[series.index >= monday]
    elif period == "MTD":
        month_start = end_date.replace(day=1)
        return series[series.index >= month_start]
    elif period == "1M":
        start_date = end_date - timedelta(days=30)
        return series[(series.index > start_date) & (series.index <= end_date)]
    elif period == "QTD":
        quarter_month = ((end_date.month - 1) // 3) * 3 + 1
        quarter_start = end_date.replace(month=quarter_month, day=1)
        return series[series.index >= quarter_start]
    elif period == "1Q":
        start_date = end_date - timedelta(days=91)
        return series[(series.index > start_date) & (series.index <= end_date)]
    elif period == "YTD":
        year_start = end_date.replace(month=1, day=1)
        return series[series.index >= year_start]
    elif period == "1Y":
        start_date = end_date - timedelta(days=365)
        return series[(series.index > start_date) & (series.index <= end_date)]
    elif period == "Since Inception":
        return series[series.index >= inception]
    return pd.Series(dtype=float)


def structural_inspection(panel: pd.DataFrame) -> list[dict]:
    """AC1 -- per-series row count, date range, NaN count, zero-return-day
    count, max abs daily-return with date.
    """
    rows = []
    for col in panel.columns:
        s = panel[col]
        s_nonnull = s.dropna()
        if s_nonnull.empty:
            continue
        zero_count = int((s_nonnull == 0).sum())
        max_abs_idx = s_nonnull.abs().idxmax()
        max_abs_val = float(s_nonnull.loc[max_abs_idx])
        rows.append({
            "series": col,
            "row_count": int(len(s_nonnull)),
            "first_date": str(s_nonnull.index.min().date()),
            "last_date": str(s_nonnull.index.max().date()),
            "nan_count": int(s.isna().sum()),
            "zero_return_day_count": zero_count,
            "max_abs_daily_return_pct": round(max_abs_val, 4),
            "max_abs_daily_return_date": str(pd.Timestamp(max_abs_idx).date()),
        })
    return rows


def pair_window_stats(idx_series: pd.Series, etf_series: pd.Series,
                      window_name: str, slc: pd.DataFrame) -> dict:
    """AC2 -- for one (INDEX, ETF) pair over one window.

    Returns Pearson correlation, stdev ratio (ETF/INDEX), residual mean/stdev/
    max-abs (with date), residual lag-1 autocorrelation, plus n.
    """
    a = slc[idx_series].dropna()
    b = slc[etf_series].dropna()
    joint = pd.concat([a, b], axis=1, join="inner").dropna()
    joint.columns = ["idx", "etf"]
    n = len(joint)
    if n < 2:
        return {"window": window_name, "n": n,
                "corr": None, "stdev_ratio_etf_over_idx": None,
                "residual_mean_pct": None, "residual_stdev_pct": None,
                "max_abs_residual_pct": None, "max_abs_residual_date": None,
                "residual_lag1_autocorr": None,
                "idx_stdev_pct": None, "etf_stdev_pct": None}
    corr = float(joint["idx"].corr(joint["etf"]))
    idx_sd = float(joint["idx"].std(ddof=1))
    etf_sd = float(joint["etf"].std(ddof=1))
    ratio = float(etf_sd / idx_sd) if idx_sd > 0 else None
    residual = joint["etf"] - joint["idx"]
    r_mean = float(residual.mean())
    r_std = float(residual.std(ddof=1))
    abs_idx = residual.abs().idxmax()
    r_max_abs = float(residual.loc[abs_idx])
    if n >= 3:
        lag1 = float(residual.autocorr(lag=1))
    else:
        lag1 = None
    return {
        "window": window_name,
        "n": n,
        "first_date": str(joint.index.min().date()),
        "last_date": str(joint.index.max().date()),
        "corr": round(corr, 4),
        "idx_stdev_pct": round(idx_sd, 4),
        "etf_stdev_pct": round(etf_sd, 4),
        "stdev_ratio_etf_over_idx": round(ratio, 4) if ratio is not None else None,
        "residual_mean_pct": round(r_mean, 4),
        "residual_stdev_pct": round(r_std, 4),
        "max_abs_residual_pct": round(r_max_abs, 4),
        "max_abs_residual_date": str(pd.Timestamp(abs_idx).date()),
        "residual_lag1_autocorr": round(lag1, 4) if lag1 is not None else None,
    }


def reproduce_vols(panel: pd.DataFrame, end_date,
                    published: dict) -> list[dict]:
    """AC3 -- reproduce calculate_volatility for both INDEX and ETF series
    for each (model, period); cross-check vs published JSON.
    """
    pub_by_model = {m["code"]: m.get("returns", {})
                    for m in published.get("models", [])}
    rows = []
    for model in MODEL_CODES:
        idx_name = INDEX_NAME_MAP[model]["index_benchmark"]
        etf_name = INDEX_NAME_MAP[model]["etf_benchmark"]
        if idx_name not in panel.columns or etf_name not in panel.columns:
            rows.append({"model": model, "missing_series": True})
            continue
        for period in PERIODS:
            idx_slice = period_slice(panel[idx_name], end_date, period)
            etf_slice = period_slice(panel[etf_name], end_date, period)
            idx_vol = calculate_volatility(idx_slice)
            etf_vol = calculate_volatility(etf_slice)
            pub = pub_by_model.get(model, {}).get(period, {})
            pub_idx = pub.get("index_benchmark_volatility")
            pub_etf = pub.get("etf_benchmark_volatility")
            d_idx = (None if idx_vol is None or pub_idx is None
                     else round(idx_vol - pub_idx, 4))
            d_etf = (None if etf_vol is None or pub_etf is None
                     else round(etf_vol - pub_etf, 4))
            rows.append({
                "model": model,
                "period": period,
                "n_idx": int(len(idx_slice.dropna())),
                "n_etf": int(len(etf_slice.dropna())),
                "recomputed_index_vol": idx_vol,
                "published_index_vol": pub_idx,
                "diff_index_vol_abs_pct": d_idx,
                "recomputed_etf_vol": etf_vol,
                "published_etf_vol": pub_etf,
                "diff_etf_vol_abs_pct": d_etf,
            })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-json", default=None,
                    help="write the full audit dict to this JSON path")
    args = ap.parse_args()

    print("INFO: loading pickle + published JSON", flush=True)
    data_pkl, data_key = load_pickle()
    published = json.loads(
        s3().get_object(Bucket=BUCKET, Key=PUBLISHED_KEY)["Body"].read())

    print(f"INFO: data_pkl key = {data_key}", flush=True)
    print(f"INFO: published data_as_of = {published.get('data_as_of')}",
          flush=True)
    print(f"INFO: return_daily rows = {len(data_pkl['return_daily']):,}",
          flush=True)

    panel = get_term_returns(data_pkl)
    end_date = panel.index.max()
    print(f"INFO: panel after get_term_returns: rows={len(panel)}, "
          f"cols={len(panel.columns)}, end_date={end_date.date()}", flush=True)
    print(f"INFO: panel columns = {sorted(panel.columns.tolist())}",
          flush=True)

    # --- AC1: structural inspection ---
    ac1 = structural_inspection(panel)
    print("\nINFO: AC1 -- structural inspection (per series):", flush=True)
    print(pd.DataFrame(ac1).to_string(index=False), flush=True)

    # --- AC2: pair-window stats (4 distinct pairs x 3 windows) ---
    distinct_pairs = []  # (label, idx_name, etf_name)
    seen = set()
    for model in MODEL_CODES:
        idx_n = INDEX_NAME_MAP[model]["index_benchmark"]
        etf_n = INDEX_NAME_MAP[model]["etf_benchmark"]
        if (idx_n, etf_n) in seen:
            continue
        seen.add((idx_n, etf_n))
        # LTC + LTA share -> labeled "LT" for shared pair
        label = "LT" if model in ("LTC", "LTA") else model
        distinct_pairs.append((label, idx_n, etf_n))
    print("\nINFO: AC2 -- 4 distinct INDEX-vs-ETF pairs (LTC/LTA share):",
          flush=True)
    for label, idx_n, etf_n in distinct_pairs:
        print(f"  {label}: ({idx_n}) vs ({etf_n})", flush=True)

    ac2 = []
    # 1Y window: calendar-365 to mirror the Lambda's calculate_period_returns
    # 1Y branch (`end_date - 365 days`); yields ~261 weekday entries
    # post-weekend-strip rather than tail(252). CTO rider #2 (2026-05-19).
    one_year_start = end_date - timedelta(days=365)
    one_year = panel[(panel.index > one_year_start)
                     & (panel.index <= end_date)]
    ytd_mask = panel.index >= pd.Timestamp(year=end_date.year, month=1, day=1)
    ytd = panel[ytd_mask]
    si_mask = panel.index >= pd.Timestamp(INCEPTION_DATE)
    si = panel[si_mask]
    for label, idx_n, etf_n in distinct_pairs:
        for window_name, slc in (("1Y", one_year), ("YTD", ytd),
                                 ("Since Inception", si)):
            row = {"pair": label, "idx_name": idx_n, "etf_name": etf_n}
            row.update(pair_window_stats(idx_n, etf_n, window_name, slc))
            ac2.append(row)
    print("\nINFO: AC2 -- pair-window stats:", flush=True)
    ac2_df = pd.DataFrame(ac2)
    print(ac2_df.drop(columns=["idx_name", "etf_name"]).to_string(
        index=False), flush=True)

    # --- AC3: reproduce vols + cross-check ---
    ac3 = reproduce_vols(panel, end_date, published)
    ac3_df = pd.DataFrame(ac3)
    print("\nINFO: AC3 -- reproduce vols (5 models x 9 periods):", flush=True)
    print(ac3_df.to_string(index=False), flush=True)
    drift_idx = ac3_df[(ac3_df["diff_index_vol_abs_pct"].abs() > 0.01)
                       & ac3_df["diff_index_vol_abs_pct"].notna()]
    drift_etf = ac3_df[(ac3_df["diff_etf_vol_abs_pct"].abs() > 0.01)
                       & ac3_df["diff_etf_vol_abs_pct"].notna()]
    print(f"\nINFO: AC3 drift rows (|diff| > 0.01%): "
          f"INDEX={len(drift_idx)}, ETF={len(drift_etf)}", flush=True)
    if len(drift_idx):
        print("  INDEX drifts:", flush=True)
        print(drift_idx.to_string(index=False), flush=True)
    if len(drift_etf):
        print("  ETF drifts:", flush=True)
        print(drift_etf.to_string(index=False), flush=True)

    # --- AC4 + AC5: hypothesis verdict + anomaly inventory ---
    # AC4 thresholds: corr>=0.95; stdev_ratio in [1.00, 1.30]; residual_mean
    # plausible-fee-drag (<= ~14 bps/year for BIL = ~0.06bps/day, ~3bps for IVV
    # ~0.012bps/day; use 5bps/day as a generous outer bound per TO §scope).
    # AC5 classes (TO §scope): ETF<INDEX vol; ratio>1.30 in calm; corr<0.90;
    # residual drift >5bps/day in magnitude; zero-day asymmetry.
    print("\nINFO: AC4 -- microstructure hypothesis verdict per (pair, window):",
          flush=True)
    verdicts = []
    for row in ac2:
        flags = []
        if row["corr"] is not None and row["corr"] < 0.95:
            flags.append(f"corr<0.95 (corr={row['corr']:.4f})")
        if (row["stdev_ratio_etf_over_idx"] is not None
                and not (1.00 <= row["stdev_ratio_etf_over_idx"] <= 1.30)):
            flags.append(
                f"stdev ratio out of [1.00, 1.30] "
                f"(ratio={row['stdev_ratio_etf_over_idx']:.4f})")
        if (row["residual_mean_pct"] is not None
                and abs(row["residual_mean_pct"]) > 0.05):
            flags.append(
                f"|residual mean| > 5bps/day "
                f"({row['residual_mean_pct']:.4f}%)")
        verdict = "consistent-with-microstructure" if not flags else "FLAGGED"
        verdicts.append({"pair": row["pair"], "window": row["window"],
                         "verdict": verdict, "flags": "; ".join(flags)})
    verdicts_df = pd.DataFrame(verdicts)
    print(verdicts_df.to_string(index=False), flush=True)

    # AC5 anomaly inventory
    print("\nINFO: AC5 -- anomaly inventory:", flush=True)
    inventory = {
        "etf_lt_index_vol": [],
        "ratio_gt_1p30_calm": [],
        "corr_lt_0p90": [],
        "residual_drift_gt_5bps": [],
        "zero_day_asymmetry": [],
        "lambda_collapsed_period_values": [],
        "ratio_gt_1p30_full_grid": [],
    }
    # ETF < INDEX vol: across all AC3 cells
    for r in ac3:
        if (r.get("recomputed_index_vol") is not None
                and r.get("recomputed_etf_vol") is not None
                and r["recomputed_etf_vol"] < r["recomputed_index_vol"]):
            inventory["etf_lt_index_vol"].append({
                "model": r["model"], "period": r["period"],
                "idx_vol": r["recomputed_index_vol"],
                "etf_vol": r["recomputed_etf_vol"],
                "magnitude_pct": round(
                    r["recomputed_index_vol"] - r["recomputed_etf_vol"], 4),
            })
    # ratio>1.30 calm: across pair_window rows
    for r in ac2:
        if (r["stdev_ratio_etf_over_idx"] is not None
                and r["stdev_ratio_etf_over_idx"] > 1.30):
            inventory["ratio_gt_1p30_calm"].append({
                "pair": r["pair"], "window": r["window"],
                "ratio": r["stdev_ratio_etf_over_idx"]})
    # corr<0.90 across pair_window rows
    for r in ac2:
        if r["corr"] is not None and r["corr"] < 0.90:
            inventory["corr_lt_0p90"].append({
                "pair": r["pair"], "window": r["window"],
                "corr": r["corr"]})
    # residual drift > 5bps/day mean across pair_window rows
    for r in ac2:
        if (r["residual_mean_pct"] is not None
                and abs(r["residual_mean_pct"]) > 0.05):
            inventory["residual_drift_gt_5bps"].append({
                "pair": r["pair"], "window": r["window"],
                "residual_mean_pct": r["residual_mean_pct"]})
    # Full-grid ratio test (5 models x 9 periods, both PUBLISHED and recomputed)
    # AC4 thresholds applied across all 45 cells, not just 12 AC2 cells.
    pub_by_model = {m["code"]: m.get("returns", {})
                    for m in published.get("models", [])}
    for r in ac3:
        if r.get("missing_series"):
            continue
        # Use published vols to characterize what the consumer SEES
        pub_idx = r.get("published_index_vol")
        pub_etf = r.get("published_etf_vol")
        if pub_idx and pub_etf and pub_idx > 0:
            ratio = pub_etf / pub_idx
            if ratio > 1.30:
                inventory["ratio_gt_1p30_full_grid"].append({
                    "model": r["model"], "period": r["period"],
                    "published_idx_vol": pub_idx,
                    "published_etf_vol": pub_etf,
                    "ratio": round(ratio, 4),
                })

    # Lambda-collapsed-period-value anomaly: for each model, check whether
    # published 1D / WTD / MTD volatility fields collapse to one value.
    for code in MODEL_CODES:
        m_ret = pub_by_model.get(code, {})
        v1d = m_ret.get("1D", {}).get("index_benchmark_volatility")
        vwtd = m_ret.get("WTD", {}).get("index_benchmark_volatility")
        vmtd = m_ret.get("MTD", {}).get("index_benchmark_volatility")
        if v1d is not None and v1d == vwtd == vmtd:
            inventory["lambda_collapsed_period_values"].append({
                "model": code, "axis": "index_benchmark_volatility",
                "value_1d": v1d, "value_wtd": vwtd, "value_mtd": vmtd,
            })
        v1d_e = m_ret.get("1D", {}).get("etf_benchmark_volatility")
        vwtd_e = m_ret.get("WTD", {}).get("etf_benchmark_volatility")
        vmtd_e = m_ret.get("MTD", {}).get("etf_benchmark_volatility")
        if v1d_e is not None and v1d_e == vwtd_e == vmtd_e:
            inventory["lambda_collapsed_period_values"].append({
                "model": code, "axis": "etf_benchmark_volatility",
                "value_1d": v1d_e, "value_wtd": vwtd_e, "value_mtd": vmtd_e,
            })

    # zero-day asymmetry on AC1 -- compare zero_return_day_count for index vs
    # etf per pair on the full SI panel.
    ac1_by_name = {r["series"]: r for r in ac1}
    for label, idx_n, etf_n in distinct_pairs:
        idx_zeros = ac1_by_name.get(idx_n, {}).get("zero_return_day_count", 0)
        etf_zeros = ac1_by_name.get(etf_n, {}).get("zero_return_day_count", 0)
        denom = max(ac1_by_name.get(idx_n, {}).get("row_count", 1), 1)
        ratio = abs(idx_zeros - etf_zeros) / denom
        # Surface every observed asymmetry (lower the threshold to 1%, since
        # the audit's interest is "is the calendar handling defensible," not
        # "did >5% of rows differ"). Per-pair zero-day count contrast goes in
        # the inventory regardless; the brief explains the underlying mechanism.
        if ratio > 0.01:
            inventory["zero_day_asymmetry"].append({
                "pair": label,
                "idx_zero_days": idx_zeros,
                "etf_zero_days": etf_zeros,
                "row_count": denom,
                "asym_ratio": round(ratio, 4),
            })
    for cls, items in inventory.items():
        if items:
            print(f"  {cls}: {len(items)} anomaly row(s)", flush=True)
            for x in items:
                print(f"    {x}", flush=True)
        else:
            print(f"  {cls}: NONE", flush=True)

    out = {
        "data_pkl_key": data_key,
        "published_data_as_of": published.get("data_as_of"),
        "panel_rows": int(len(panel)),
        "panel_cols": sorted(panel.columns.tolist()),
        "end_date": str(end_date.date()),
        "ac1_structural": ac1,
        "ac2_pair_window": ac2,
        "ac3_reproduce_vols": ac3,
        "ac3_drift_index_count": int(len(drift_idx)),
        "ac3_drift_etf_count": int(len(drift_etf)),
        "ac3_drift_index_rows": drift_idx.to_dict(orient="records"),
        "ac3_drift_etf_rows": drift_etf.to_dict(orient="records"),
        "ac4_verdicts": verdicts,
        "ac5_inventory": inventory,
    }
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, default=str)
        print(f"\nINFO: wrote {args.out_json}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
