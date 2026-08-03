"""ST interval-return comparison for the W1/W4 content gate.

Replicates yang-model-portfolio-benchmarks' exact methodology (period windows,
compound_returns, calculate_volatility, INCEPTION 2024-04-30), then:
  CONTROL: computed from 0727 pkl @ 2026-07-27 must reproduce the SERVED 07-27 JSON.
  TARGET:  computed from the corrected 0731 pkl @ 2026-07-31, compared interval-by-interval.
ASCII-only.
"""
import json
import pickle
import sys
from datetime import timedelta

import numpy as np
import pandas as pd

OUT = r"C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents\OCIO Models\Dashboard\202511 Model Portfolio Exposure\output"
SCRATCH = r"C:\Users\OPALBL~1\AppData\Local\Temp\claude\C--Users-Opal-Bloomberg-Desktop-ajb-workspace\d6886795-b5fb-491b-bec0-9948fe43d03e\scratchpad"
INCEPTION = pd.to_datetime("2024-04-30")
PERIODS = ["1D", "WTD", "MTD", "1M", "QTD", "1Q", "YTD", "1Y", "TTW", "Since Inception"]


def series_from_pkl(path, index_name):
    with open(path, "rb") as f:
        d = pickle.load(f)
    rd = d["return_daily"]
    s = rd[rd["index_name"] == index_name].copy()
    s["date"] = pd.to_datetime(s["date"])
    return s.sort_values("date").set_index("date")["return"].astype(float)


def compound(returns_pct):
    r = returns_pct.dropna().values / 100
    if len(r) == 0:
        return None
    return round(((1 + r).prod() - 1) * 100, 2)


def vol(returns_pct, min_points=5):
    r = returns_pct.dropna().values / 100
    if len(r) < min_points:
        return None
    return round(np.std(r, ddof=1) * np.sqrt(252) * 100, 2)


def period_return(series, period, end_date):
    series = series[series.index <= end_date]
    if len(series) == 0:
        return None, None
    if period == "1D":
        pdta = series.tail(1)
        ret = round(float(pdta.iloc[-1]), 2) if len(pdta) else None
        return ret, vol(series.tail(20))
    if period == "WTD":
        monday = end_date - timedelta(days=end_date.weekday())
        pdta = series[series.index >= monday]
    elif period == "MTD":
        pdta = series[series.index >= end_date.replace(day=1)]
    elif period == "1M":
        pdta = series[(series.index > end_date - timedelta(days=30)) & (series.index <= end_date)]
    elif period == "QTD":
        qm = ((end_date.month - 1) // 3) * 3 + 1
        pdta = series[series.index >= end_date.replace(month=qm, day=1)]
    elif period == "1Q":
        pdta = series[(series.index > end_date - timedelta(days=91)) & (series.index <= end_date)]
    elif period == "YTD":
        pdta = series[series.index >= end_date.replace(month=1, day=1)]
    elif period == "1Y":
        pdta = series[(series.index > end_date - timedelta(days=365)) & (series.index <= end_date)]
    elif period == "TTW":
        pdta = series.tail(10)
    elif period == "Since Inception":
        pdta = series[series.index >= INCEPTION]
    else:
        return None, None
    ret = compound(pdta)
    v = vol(pdta)
    if period == "Since Inception" and ret is not None:
        days = (end_date - INCEPTION).days
        if days > 0:
            ret = round(((1 + ret / 100) ** (365 / days) - 1) * 100, 2)
    return ret, v


def main():
    with open(SCRATCH + r"\mpb_current.json") as f:
        served_0727 = json.load(f)
    st_served = [m for m in served_0727["models"] if m["code"] == "ST"][0]["returns"]
    assert served_0727["data_as_of"] == "2026-07-27"

    # CONTROL: replicate served 07-27 from the 0727 pkl
    s_model_27 = series_from_pkl(OUT + r"\data 20260727 v1.pkl", "Short Term")
    end27 = pd.to_datetime("2026-07-27")
    print("CONTROL -- my replication (0727 pkl @ 07-27) vs SERVED 07-27 JSON, ST model:")
    print(f"{'period':16} {'mine':>9} {'served':>9} {'match':>6}")
    all_match = True
    for p in PERIODS:
        mine, _ = period_return(s_model_27, p, end27)
        srv = st_served.get(p, {}).get("model")
        ok = (mine is None and srv is None) or (mine is not None and srv is not None and abs(mine - srv) < 0.005)
        all_match &= ok
        print(f"{p:16} {str(mine):>9} {str(srv):>9} {'OK' if ok else '<<< MISMATCH'}")
    print("CONTROL VERDICT:", "FAITHFUL REPLICATION" if all_match else "METHODOLOGY MISMATCH -- do not trust target numbers")

    # TARGET: corrected 0731 pkl @ 07-31
    src = SCRATCH + r"\data 20260731 v1 DEDUPED.pkl"
    s_model_31 = series_from_pkl(src, "Short Term")
    s_bmk_31 = series_from_pkl(src, "Short Term Benchmark")
    end31 = pd.to_datetime("2026-07-31")
    print()
    print("TARGET -- corrected 0731 pkl @ 07-31 vs served 07-27, ST MODEL (ret / vol):")
    print(f"{'period':16} {'corrected_0731':>16} {'served_0727':>14} {'delta':>8}")
    for p in PERIODS:
        r31, v31 = period_return(s_model_31, p, end31)
        srv = st_served.get(p, {}).get("model")
        srvv = st_served.get(p, {}).get("model_volatility")
        delta = None if (r31 is None or srv is None) else round(r31 - srv, 2)
        print(f"{p:16} {str(r31):>9}/{str(v31):>6} {str(srv):>9}/{str(srvv):>4} {str(delta):>8}")
    print()
    print("TARGET -- ST INDEX BENCHMARK (context):")
    print(f"{'period':16} {'corrected_0731':>16} {'served_0727':>14}")
    for p in PERIODS:
        r31, v31 = period_return(s_bmk_31, p, end31)
        srv = st_served.get(p, {}).get("index_benchmark")
        print(f"{p:16} {str(r31):>9}/{str(v31):>6} {str(srv):>14}")
    # the four extra trading days 07-28..07-31, for the delta narrative
    tail = s_model_31[(s_model_31.index > end27) & (s_model_31.index <= end31)]
    print()
    print("new trading days in 0731 beyond 07-27 (ST model daily returns %):")
    for dt_, r in tail.items():
        print(f"  {dt_.date()}  {r:+.4f}")
    print(f"  compounded: {compound(tail):+.2f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
