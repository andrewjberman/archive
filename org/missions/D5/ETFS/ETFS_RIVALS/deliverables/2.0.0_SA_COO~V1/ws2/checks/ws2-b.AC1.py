"""WS2-b AC1 -- rivalfunds.dramatic_move: detect() finds a stored close past 3x or under 1/3 of the security's prior stored
close with no split or merger on file; lookup() turns a web search result into ONE corporate-action row (claim INFERRED,
source_url), or None. The search is injected: this check makes no network call and writes nothing.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/ws2-b.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

import pandas as pd  # noqa: E402

fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


try:
    from rivalfunds import dramatic_move as dm
except Exception as e:  # noqa: BLE001 -- the module is absent at the base: the expected FAIL
    print(f"FAIL (import) rivalfunds.dramatic_move: {type(e).__name__}: {e}")
    print("AC1 RESULT: FAIL 1 (import)")
    sys.exit(0)

G4 = pd.DataFrame([{"security_id": "TKOMY_US_Equity", "date": d, "px_close": p, "currency": "USD"} for d, p in
                   [("2026-10-05", 49.59), ("2026-10-06", 50.5), ("2026-10-07", 3.33)]] +
                  [{"security_id": "AAA_US_Equity", "date": d, "px_close": p, "currency": "USD"} for d, p in
                   [("2026-10-06", 10.0), ("2026-10-07", 19.0)]])
NO_ACTIONS = pd.DataFrame([], columns=["security_id", "event_type", "ratio", "ex_date", "claim"])
STORED = pd.DataFrame([{"security_id": "TKOMY US Equity", "event_type": "split", "ratio": 15.0, "ex_date": "2026-10-07",
                        "claim": "MEASURED"}])

# (a) the 93% drop with no action on file is one candidate; a 1.9x move is not
c = dm.detect(G4, NO_ACTIONS)
check("a", len(c) == 1 and c[0].get("security_id") == "TKOMY_US_Equity" and str(c[0].get("date"))[:10] == "2026-10-07"
      and abs(float(c[0].get("prior_close")) - 50.5) < 1e-9 and abs(float(c[0].get("close")) - 3.33) < 1e-9,
      f"candidates {c}")

# (b) control: the same move with a stored split on file is not a candidate
check("b", dm.detect(G4, STORED) == [], f"candidates with a stored split {dm.detect(G4, STORED)}")

# (c) lookup: a search result naming the ratio becomes one row in the stored shape, claim INFERRED, with its URL
calls = []


def found(q):
    calls.append(q)
    return [{"title": "Tokio Marine to conduct stock split", "url": "https://example.test/tokio-split",
             "snippet": "Tokio Marine Holdings will carry out a 15-for-1 stock split effective October 7, 2026."}]


row = dm.lookup(c[0] if c else {"security_id": "TKOMY_US_Equity", "date": "2026-10-07", "prior_close": 50.5,
                                 "close": 3.33, "security_name": "Tokio Marine Holdings Inc"}, search=found)
check("c", isinstance(row, dict) and row.get("event_type") == "split" and float(row.get("ratio")) == 15.0
      and str(row.get("ex_date"))[:10] == "2026-10-07" and row.get("claim") == "INFERRED"
      and row.get("source_url") == "https://example.test/tokio-split" and row.get("security_id") == "TKOMY US Equity"
      and len(calls) >= 1 and "Tokio Marine" in calls[0],
      f"row {row}; queries {calls}")

# (d) control: nothing found -> None, never a guessed ratio
none = dm.lookup({"security_id": "TKOMY_US_Equity", "date": "2026-10-07", "prior_close": 50.5, "close": 3.33,
                  "security_name": "Tokio Marine Holdings Inc"}, search=lambda q: [])
check("d", none is None, f"no result -> {none!r}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
