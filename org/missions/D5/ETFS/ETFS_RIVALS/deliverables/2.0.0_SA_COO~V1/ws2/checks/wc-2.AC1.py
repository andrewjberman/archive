"""WC-2 AC1 -- the audit window's money-market exclusion names the line it leaves out (security name and amount) in a block of
its own, not the element immediately before the trade table; the main page header has no Period row, while the ranking panels'
period switch (and the rf-period radios it checks) stay. Pure: render functions over in-memory dicts, no S3, no vendor.

Server side: render._trades(fund, wmax) renders an audit fund's windows; render._controls(ctx, funds, opening) returns the
header (radios, controls); render._component_switch() is a panel's own period switch (the control).
ASSUMED CARRIER (arm a2 only): the window dict carries today only the COUNT `cash_equiv` (built in publish_page, outside
wc-2's bounds). This check also passes the excluded line as `cash_equiv_lines` = [{security_key, name, est_notional}]; the
cell does not name that field, so the issuer states it (or amends this arm) before the cut.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/wc-2.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

from rivalfunds import render  # noqa: E402

fails = []
MMF = "JPMorgan US Government Money Market"


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def trade():
    side = {"date": "2026-10-05", "key": "8035_JP", "quantity": 205000.0, "market_value": 4.1e7, "weight": 0.02, "held": True,
            "file": {"source": "bloomberg", "capture_origin": "x", "bronze_uri": "s3://b/k.json", "sha256": "ab" * 32}}
    return {"action": "trim", "name": "Tokyo Electron", "security_key": "8035_JP", "security_key_kind": "security_id",
            "counterpart_security_key": None, "shares_before": 210000.0, "shares_after": 205000.0,
            "discretionary_shares": -5000.0, "est_price": 200.0, "est_notional": -1.0e6, "weight_before": 0.021,
            "weight_after": 0.02, "confidence": "CLEAN", "key_resolution": "RESOLVED", "key_resolved": True,
            "window_widened": False, "flow_adjusted": False, "income_funded": False, "window_start": "2026-10-05",
            "window_end": "2026-10-06", "window_trading_days": 1, "flow_factor": 1.0,
            "trace": {"prior": side, "later": dict(side, date="2026-10-06")}}


win = {"window_start": "2026-10-05", "window_end": "2026-10-06", "trades": [trade()], "recon": None, "no_move": 0,
       "cash_equiv": 1,
       "cash_equiv_lines": [{"security_key": "JTSXX_US_Equity", "name": MMF, "est_notional": 2.1e6}]}  # ASSUMED carrier
fund = {"fund": "CGIC", "windows": [win], "truncated": 0, "excluded": {"cash": 1, "ca": 0, "income": 0, "income_funded": 0}}

# (a1) the exclusion block is not the element immediately before the trade table
try:
    html = render._trades(fund, 0.05)
except Exception as e:  # noqa: BLE001
    html = f"ERROR {type(e).__name__}: {e}"
t = html.find("<table")
hit = [m.start() for m in re.finditer(r"money-market|data-cash-equiv", html)]
before = [i for i in hit if 0 <= t and i < t]
if t < 0 or not hit:
    ok, why = False, f"table at {t}, exclusion hits {hit}"
elif not before:
    ok, why = True, "exclusion sits after the trade table"
else:
    gap = html[before[-1]:t]
    close = re.search(r"</[a-z0-9]+>", gap)
    tail = gap[close.end():] if close else gap
    ok = bool(re.search(r"<(?!/)(?!table)[a-z]", tail))
    why = f"between the exclusion's close and <table: {tail[:160]!r}"
print(f"     (a) rendered window: {html[:900]!r}")
check("a1", ok, why)

# (a2) it names the excluded line and its amount
amounts = ("2.1m", "2,100,000", "2.10m")
check("a2", MMF in html and any(a in html for a in amounts),
      f"names {MMF!r}: {MMF in html}; amount {[a for a in amounts if a in html]}")

# (b) the header has no Period row; the radios and a panel's own period switch stay (control)
funds = [{"fund": "CGIC", "group": "Global", "role": "home"}, {"fund": "RIV1", "group": "Global", "role": "peer"}]
a1 = [{"fund_id": f["fund"], "period": p, "n_days_period": n, "period_start": s, "period_end": "2026-10-06"}
      for f in funds for p, n, s in (("R30", 21, "2026-09-08"), ("R90", 63, "2026-07-08"), ("R365", 252, "2025-10-06"))]
ctx = {"day": "2026-10-06", "a1": {"holding_contribution": a1}}
try:
    radios, controls = render._controls(ctx, funds, "CGIC")
except Exception as e:  # noqa: BLE001
    radios, controls = "", f"ERROR {type(e).__name__}: {e}"
print(f"     (b) header controls: {controls[:900]!r}")
period_row = [s for s in ('class="rf-periods"', ">Period<", "data-period-dates", 'for="rf-period-') if s in controls]
check("b", not period_row and "rf-picker" in controls, f"header Period-row markers present: {period_row}")
sw = render._component_switch()
check("b-control", all(f'id="rf-period-{p}"' in radios for p in render.PERIODS)
      and all(f'for="rf-period-{p}"' in sw for p in render.PERIODS) and "30d" in sw and "365d" in sw,
      f"radios {re.findall(r'id=.(rf-period-R[0-9]+)', radios)}; panel switch labels {re.findall(r'for=.(rf-period-R[0-9]+)', sw)}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
