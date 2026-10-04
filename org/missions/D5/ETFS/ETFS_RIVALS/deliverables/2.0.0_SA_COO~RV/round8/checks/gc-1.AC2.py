"""RIV-gc-1 AC2 (PRD v0.14, Andrew smoke S7: "the AI analysis is focused around the last 30 days ... the last 30 trading
days"): the AI fact pack's "last 30 days" trades are the last 30 TRADING days, not 30 calendar days. Today `fact_pack` keeps
G5 trades whose window_end is within `R30_DAYS` = 30 calendar days before the day (`ai_accounts.py` ~:133).

Interface (prescribed): `ai_accounts.fact_pack(fund_id, day, g5, g6, contribution, trend)` keeps a trade whose window_end
lies after the 31st NYSE trading day before `day` (i.e. within the last 30 trading days ending on `day`).
Fixture: day 2026-10-01; fund IDVZ; three trades: window_end 2026-08-26 (25 trading days back, 36 calendar days),
2026-09-25 (in both), 2026-07-30 (more than 30 trading days back).
  - (a) the 2026-08-26 trade is a T-fact (inside 30 trading days, outside 30 calendar days);
  - (b) control: the 2026-09-25 trade is a T-fact;
  - (c) control: the 2026-07-30 trade is NOT a T-fact.
FAIL at base: (a) FAILS (the 30-calendar-day cut drops it); (b) and (c) PASS."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-01"


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd

    from lib import trading_calendar as tc
    from rivalfunds import ai_accounts as aa

    import datetime as dt
    back = tc.trading_days_between(dt.date(2026, 6, 1), dt.date.fromisoformat(DAY))
    print("trading days 2026-08-26..10-01:", sum(1 for d in back if d >= dt.date(2026, 8, 26)),
          "| 2026-07-30..10-01:", sum(1 for d in back if d >= dt.date(2026, 7, 30)))
    g5 = pd.DataFrame([
        {"fund_id": "IDVZ", "security_key": "AAA_US_Equity", "security_id": "AAA", "action": "add", "window_end": "2026-08-26",
         "est_notional_base": 1500000.0, "dataset_revision": "fx"},
        {"fund_id": "IDVZ", "security_key": "BBB_US_Equity", "security_id": "BBB", "action": "trim", "window_end": "2026-09-25",
         "est_notional_base": -900000.0, "dataset_revision": "fx"},
        {"fund_id": "IDVZ", "security_key": "CCC_US_Equity", "security_id": "CCC", "action": "add", "window_end": "2026-07-30",
         "est_notional_base": 700000.0, "dataset_revision": "fx"},
    ])
    empty = pd.DataFrame()
    facts = aa.fact_pack("IDVZ", DAY, g5, empty, empty, empty)
    keys = [f["cited_row"]["key"] for f in facts if f["id"].startswith("T")]
    print("T-facts:", keys)
    v.check(any("AAA_US_Equity" in k for k in keys), "(a) a trade 25 trading days back (36 calendar days) is a T-fact")
    v.check(any("BBB_US_Equity" in k for k in keys), "(b) control: a trade 4 trading days back is a T-fact")
    v.check(not any("CCC_US_Equity" in k for k in keys), "(c) control: a trade more than 30 trading days back is not a T-fact")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
