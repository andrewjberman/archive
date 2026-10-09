"""WD-1 AC1 -- gold_trade_schedule.infer_trades(canonical, actions=None): a holding whose share count did not move is never a
trade whatever the flow factor; a candidate add/trim below TRADE_TOLERANCE_BPS (20 bps of the later report's total market
value) is not a page trade (dropped, or kept with action `below_tolerance` / an equivalent flag), while entries and exits stay
trades whatever their size; a later report that re-publishes the earlier one yields no trade. Pure: frames only, no S3, no vendor.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/wd-1.AC1.py
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

D0, D1 = "2026-10-01", "2026-10-02"
TRADE_ACTIONS = ("entry", "add", "trim", "exit")
SHOW = ["security_key", "action", "shares_before", "shares_after", "discretionary_shares", "est_notional", "flow_factor"]
fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def canon(date, book, fund, actual=None):
    """book: {bbg id: (quantity, price)} -> canonical_shape (G1) rows for one report date, with one USD cash line.
    `actual` = the payload's own report date (Bloomberg rows keep it in extra_attributes.bloomberg.source_report_date)."""
    day = dt.date.fromisoformat(date)
    ea = json.dumps({"bloomberg": {"source_report_date": actual or date, "requested_date": date}}, sort_keys=True)
    base = {"fund_ticker": fund, "fund_id": fund, "report_date": day, "dataset_revision": f"r-{date}", "extra_attributes": ea}
    out = [{**base, "position_type": "cash", "is_cash_line": True, "security_id": None, "raw_identifier": "USD Curncy",
            "security_bloomberg": "USD Curncy", "resolution_status": "UNRESOLVED", "quantity": 1000.0, "market_value": 0.0,
            "weight": 0.0}]
    for k, (q, p) in book.items():
        out.append({**base, "position_type": "long", "is_cash_line": False, "security_id": k.replace(" ", "_"),
                    "raw_identifier": k, "security_bloomberg": k, "resolution_status": "RESOLVED",
                    "quantity": float(q), "market_value": float(q) * p, "weight": 0.01})
    return out


def run(rows):
    try:
        return g.infer_trades(pd.DataFrame(rows), None), None
    except Exception as e:  # noqa: BLE001 -- a raised error is a FAIL with its text, never a crash
        return None, f"{type(e).__name__}: {e}"


def flagged(r) -> bool:
    """An equivalent flag the readers skip: a truthy column whose name says tolerance."""
    return any("tolerance" in str(c).lower() and bool(v) and not (isinstance(v, float) and v != v) for c, v in r.items()
               if c != "action")


def is_trade(r) -> bool:
    return str(r.get("action")) in TRADE_ACTIONS and not flagged(r)


def show(df, err):
    if err:
        return err
    if df is None or len(df) == 0:
        return "rows: []"
    cols = SHOW + [c for c in df.columns if "tolerance" in str(c).lower()]
    return "rows: " + "; ".join(str({c: (round(v, 2) if isinstance(v, float) else v) for c, v in r.items() if c in cols})
                                for r in df.to_dict("records"))


def rows_of(df, sec):
    return [] if df is None else [r for r in df.to_dict("records") if str(r["security_key"]).startswith(sec)]


# (a) fund flows scale the book by 0.97; S9 keeps exactly 10,000 shares. Its flow residual (300 sh x $10 = $3,000, ~31 bps of
#     the later book) clears the tolerance, so only the unchanged-count rule can remove it. Today: an `add` row (expected FAIL).
BOOK = {f"S{i} XX Equity": (10000, 10.0) for i in range(10)}
later = {k: ((q * 0.97 if not k.startswith("S9") else q), p) for k, (q, p) in BOOK.items()}
df, err = run(canon(D0, BOOK, "FLOW") + canon(D1, later, "FLOW"))
print(f"     (a) {show(df, err)}")
s9 = rows_of(df, "S9")
check("a", err is None and not any(str(r["action"]) in ("add", "trim") for r in s9) and not any(is_trade(r) for r in s9),
      f"unchanged 10,000 -> 10,000 under flow factor 0.97: S9 rows {[(r['action'], r['discretionary_shares']) for r in s9]}"
      + (f" ({err})" if err else ""))

# (b) no flow (f = 1). Later book total ~$989,500, so 20 bps ~ $1,979.
#     S7 trims 100 sh x $10 = $1,000 (~10 bps): NOT a page trade.  S8 trims 1,000 sh x $10 = $10,000 (~101 bps): a trade.
#     NEW entry 50 sh x $10 = $500 (~5 bps): a trade.  TINY full exit 40 sh x $10 = $400: a trade.
B0 = dict(BOOK, **{"TINY XX Equity": (40, 10.0)})
B1 = dict(BOOK, **{"S7 XX Equity": (9900, 10.0), "S8 XX Equity": (9000, 10.0), "NEW XX Equity": (50, 10.0)})
df, err = run(canon(D0, B0, "TOLR") + canon(D1, B1, "TOLR"))
print(f"     (b) {show(df, err)}")
tot = sum(q * p for q, p in B1.values())
s7, s8, new, tiny = rows_of(df, "S7"), rows_of(df, "S8"), rows_of(df, "NEW"), rows_of(df, "TINY")
check("b", err is None and not any(is_trade(r) for r in s7),
      f"sub-tolerance trim ${100 * 10.0:,.0f} = {1000 / tot * 1e4:.1f} bps of ${tot:,.0f}: S7 rows "
      f"{[(r['action'], r['est_notional']) for r in s7]} (want none, or below_tolerance / flagged)")
check("b-control", err is None and len([r for r in s8 if is_trade(r) and r["action"] == "trim"]) == 1
      and len([r for r in new if is_trade(r) and r["action"] == "entry"]) == 1
      and len([r for r in tiny if is_trade(r) and r["action"] == "exit"]) == 1,
      f"above-tolerance trim S8 {[(r['action'], r['est_notional']) for r in s8]}; small entry NEW "
      f"{[(r['action'], r['est_notional']) for r in new]}; small exit TINY {[(r['action'], r['est_notional']) for r in tiny]}")

# (c) the later report re-publishes the earlier one: same holdings, same actual report date (D0), delivered under D1.
df, err = run(canon(D0, BOOK, "REPT") + canon(D1, BOOK, "REPT", actual=D0))
print(f"     (c) {show(df, err)}")
n = 0 if df is None else sum(1 for r in df.to_dict("records") if is_trade(r))
check("c", err is None and n == 0, f"re-published report (actual date {D0} under {D1}): {n} trade row(s), want 0")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
