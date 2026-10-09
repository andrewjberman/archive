"""RIV-we-2 AC1 -- a trade window is dated by its reports' AS-OF dates (the canonical rows' source_report_date, RIV-we-1),
never by the delivery days: window_start / window_end are the as-of dates; the delivery days ride along as
window_start_delivered / window_end_delivered. A fund whose as-of equals its delivery day is unchanged (control).
Pure: canonical fixtures, no S3. CTO ruling ADDENDUM 2/3 (@9f0a957c00): "the CGIC trade windows move a trading day earlier".

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/we-2.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import datetime as dt
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

import pandas as pd  # noqa: E402

from rivalfunds import gold_trade_schedule as g  # noqa: E402

fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def canon(date, book, fund, actual):
    day = dt.date.fromisoformat(date)
    ea = json.dumps({"bloomberg": {"source_report_date": actual, "delivered_on": date, "requested_date": date}}, sort_keys=True)
    base = {"fund_ticker": fund, "fund_id": fund, "report_date": day, "dataset_revision": f"r-{fund}-{date}", "extra_attributes": ea}
    out = [{**base, "position_type": "cash", "is_cash_line": True, "security_id": None, "raw_identifier": "USD Curncy",
            "security_bloomberg": "USD Curncy", "resolution_status": "UNRESOLVED", "quantity": 1000.0, "market_value": 0.0,
            "weight": 0.0}]
    for k, (q, p) in book.items():
        out.append({**base, "position_type": "long", "is_cash_line": False, "security_id": k.replace(" ", "_"),
                    "raw_identifier": k, "security_bloomberg": k, "resolution_status": "RESOLVED",
                    "quantity": float(q), "market_value": float(q) * p, "weight": 0.01})
    return out


B0 = {"AAA US Equity": (100000, 10.0), "BBB US Equity": (50000, 20.0)}
B1 = {"AAA US Equity": (100000, 10.0), "BBB US Equity": (80000, 20.0)}   # BBB +30,000 sh ($600k, a clear trade)
# LAG: delivered 10-02 (as-of 09-30) and 10-05 (as-of 10-02); CTRL: as-of equals delivery
rows = (canon("2026-10-02", B0, "LAG", "2026-09-30") + canon("2026-10-05", B1, "LAG", "2026-10-02")
        + canon("2026-10-02", B0, "CTRL", "2026-10-02") + canon("2026-10-05", B1, "CTRL", "2026-10-05"))
try:
    df = g.infer_trades(pd.DataFrame(rows), None)
    err = None
except Exception as e:  # noqa: BLE001
    df, err = None, f"{type(e).__name__}: {e}"


def win(fund):
    if df is None:
        return err
    r = df[(df["fund_ticker"].astype(str) == fund) & (df["security_key"].astype(str).str.startswith("BBB"))]
    if not len(r):
        return "no BBB row"
    x = r.iloc[0].to_dict()
    return {k: str(x.get(k))[:10] for k in ("window_start", "window_end", "window_start_delivered", "window_end_delivered")}


lag, ctrl = win("LAG"), win("CTRL")
check("a", isinstance(lag, dict) and lag["window_start"] == "2026-09-30" and lag["window_end"] == "2026-10-02",
      f"lagging fund: the window reads its as-of dates -> {lag}")
check("b", isinstance(lag, dict) and lag["window_start_delivered"] == "2026-10-02" and lag["window_end_delivered"] == "2026-10-05",
      f"lagging fund: the delivery days ride along -> {lag}")
check("c", isinstance(ctrl, dict) and ctrl["window_start"] == "2026-10-02" and ctrl["window_end"] == "2026-10-05",
      f"control fund (as-of = delivery): unchanged -> {ctrl}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
