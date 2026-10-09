"""RIV-wh-1 (CTO ruling ADDENDUM 5 @ceab50de56) -- no '$0.0 million', no zero-notional fact, no bare identifier in a fact.

    python wh1_small_notional_and_unnamed_check.py      (run from the repository root)

Builds `ai_accounts.fact_pack` on a one-fund fixture of five trade rows inside the 30-day window:
  SMALL  42,000         -> its fact shows the notional in thousands, never '$0.0 million'
  ZERO   0              -> no fact at all
  EDGE   60,000         -> still in millions (negative arm: $0.05 million or more reads in millions)
  CUSIP  key 037833100, no name anywhere -> no fact text carries '037833100' (named, or left out)
  NAMED  5,000,000 Alpha Co -> unchanged (control)
Exit 0 = PASS, 1 = FAIL.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "data", "etfs", "scripts"))
from rivalfunds import ai_accounts  # noqa: E402

DAY = "2026-10-08"
rows = [("SML_US", "buy", 42_000.0), ("ZRO_US", "sell", 0.0), ("EDG_US", "buy", 60_000.0),
        ("037833100", "buy", 8_117_367.23), ("AAA_US", "buy", 5_000_000.0)]
g5 = pd.DataFrame([{"fund_id": "TST", "security_key": k, "action": a, "window_end": "2026-10-06", "est_notional_base": v}
                   for k, a, v in rows])
empty = pd.DataFrame(columns=["fund_id"])
names = {"SML_US": "Small Co", "ZRO_US": "Zero Co", "EDG_US": "Edge Co", "AAA_US": "Alpha Co"}
facts = ai_accounts.fact_pack("TST", DAY, g5, empty, empty, empty, names=names)
trades = [f["text"] for f in facts if str(f.get("id", "")).startswith("T")]
for t in trades:
    print("trade fact:", t)
fails = []
small = [t for t in trades if "Small Co" in t]
if not small or "$0.0 million" in small[0] or "thousand" not in small[0]:
    fails.append("SMALL: a $42,000 notional is not shown in thousands")
if any("Zero Co" in t for t in trades):
    fails.append("ZERO: a zero notional is offered as a fact")
edge = [t for t in trades if "Edge Co" in t]
if not edge or "million" not in edge[0]:
    fails.append("EDGE (negative arm): $0.06 million no longer reads in millions")
if any("037833100" in t for t in trades):
    fails.append("CUSIP: a fact carries the bare identifier 037833100")
if not any("Alpha Co" in t and "$5.0 million" in t for t in trades):
    fails.append("NAMED (control): the named $5.0 million buy changed")
if any("$0.0 million" in t for t in trades):
    fails.append("a fact still shows '$0.0 million'")
for f in fails:
    print("FAIL:", f)
print(f"WH1 RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
