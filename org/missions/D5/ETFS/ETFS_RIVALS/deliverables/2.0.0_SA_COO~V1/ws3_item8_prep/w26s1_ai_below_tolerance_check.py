"""Row W26-S1, the ai_accounts half -- a below-tolerance row is never offered to the model as a trade. Prepared before the cut.

    python w26s1_ai_below_tolerance_check.py      (run from the repository root)

Builds `ai_accounts.fact_pack` on a fixture: one fund, three trade rows inside the 30-day window. One is a buy, one is a
`below_tolerance` row (RIV-wd-1: under Andrew's 20 bps tolerance, kept as a row, never a trade), and one is a sell.
PASS when no trade fact names below_tolerance and the buy and the sell are both present (the control arm: the filter
removes only the one row). Exit 0 = PASS, 1 = FAIL.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "data", "etfs", "scripts"))
from rivalfunds import ai_accounts  # noqa: E402

DAY = "2026-10-08"
g5 = pd.DataFrame([
    {"fund_id": "TST", "security_key": "AAA_US", "action": "buy", "window_end": "2026-10-06", "est_notional_base": 5_000_000.0},
    {"fund_id": "TST", "security_key": "BBB_US", "action": "below_tolerance", "window_end": "2026-10-06", "est_notional_base": -9_000_000.0},
    {"fund_id": "TST", "security_key": "CCC_US", "action": "sell", "window_end": "2026-10-07", "est_notional_base": -3_000_000.0},
])
empty = pd.DataFrame(columns=["fund_id"])
names = {"AAA_US": "Alpha Co", "BBB_US": "Beta Co", "CCC_US": "Gamma Co"}
facts = ai_accounts.fact_pack("TST", DAY, g5, empty, empty, empty, names=names)
trades = [f["text"] for f in facts if str(f.get("id", "")).startswith("T")]
for t in trades:
    print("trade fact:", t)
fails = []
if any("below_tolerance" in t or "Beta Co" in t for t in trades):
    fails.append("a below_tolerance row is offered as a trade")
if not any("Alpha Co" in t for t in trades) or not any("Gamma Co" in t for t in trades):
    fails.append("control: the buy or the sell is missing")
for f in fails:
    print("FAIL:", f)
print(f"W26-S1 AI RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
