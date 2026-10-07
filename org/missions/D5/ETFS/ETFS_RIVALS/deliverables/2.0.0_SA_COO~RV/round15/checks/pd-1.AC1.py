"""RIV-pd-1 AC1 (PRD v0.18 FWD-23; ADDENDUM F.2, F.6; Andrew-direct calendar days @69c7f24b44): the two gold tables' periods are
30 / 90 / 365 CALENDAR days back from the as-of day, and MTD / QTD / YTD keep computing.

Measured today: `gold_holding_contribution.PERIODS = ("MTD","QTD","YTD","R30")` with R30 = the 30th NYSE trading day ending on the
day (`period_start`, :120-128); `gold_buying_trend.PERIODS = ("YTD","R30","MTD","QTD")`, R30 likewise (`_period_starts`, :123-136).
Neither knows R90 or R365 (`period_start("R90", ..)` raises ValueError; `_period_starts(..)` has no such key).

Interface (prescribed, verbatim): both modules' `PERIODS` gain `R90` and `R365` and keep `MTD`, `QTD`, `YTD`.
`gold_holding_contribution.period_start(p, day)` and `gold_buying_trend._period_starts(day)[p]` return, for `R30` / `R90` / `R365`,
`date(day) - 30 / 90 / 365` calendar days (`day` here is the as-of the stage already passes). `earliest_start` follows.
Fixture: none (pure date arithmetic); day 2026-10-06 -> R30 2026-09-06, R90 2026-07-08, R365 2025-10-06.
  - (a) `gold_holding_contribution.period_start(p, "2026-10-06")` is 2026-09-06 / 2026-07-08 / 2025-10-06 for R30 / R90 / R365;
  - (b) `gold_buying_trend._period_starts("2026-10-06")[p]` is the same three dates;
  - (c) both `PERIODS` tuples hold R30, R90 and R365 AND still MTD, QTD, YTD; `earliest_start("2026-10-06")` is 2025-10-06;
  - (d) control: both `PERIODS` hold MTD, QTD, YTD and R30, and their MTD / QTD / YTD starts for 2026-10-06 are 2026-10-01 /
        2026-10-01 / 2026-01-01 in both modules (unchanged by this cell).
FAIL at base: (a), (b), (c) FAIL (R30 is the 30th trading day, 2026-08-25; R90 and R365 do not exist); (d) PASSES."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-06"
WANT = {"R30": dt.date(2026, 9, 6), "R90": dt.date(2026, 7, 8), "R365": dt.date(2025, 10, 6)}
KEPT = {"MTD": dt.date(2026, 10, 1), "QTD": dt.date(2026, 10, 1), "YTD": dt.date(2026, 1, 1)}


def _try(fn):
    """The call's value, or a string naming why it has none (a missing period must fail its arm, never the file)."""
    try:
        return fn()
    except Exception as e:  # noqa: BLE001 -- the absence is the measured value
        return f"{type(e).__name__}: {e}"


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc

    got_hc = {p: _try(lambda p=p: hc.period_start(p, DAY)) for p in WANT}
    print("holding_contribution.period_start:", {p: str(x) for p, x in got_hc.items()}, "| want:", {p: str(x) for p, x in WANT.items()})
    v.check(got_hc == WANT, "(a) holding_contribution: R30 / R90 / R365 start 30 / 90 / 365 calendar days before the day")

    starts = _try(lambda: bt._period_starts(DAY))
    got_bt = {p: (starts.get(p) if isinstance(starts, dict) else starts) for p in WANT}
    print("buying_trend._period_starts:", {p: str(x) for p, x in got_bt.items()})
    v.check(got_bt == WANT, "(b) buying_trend: R30 / R90 / R365 start 30 / 90 / 365 calendar days before the day")

    need = {"R30", "R90", "R365", "MTD", "QTD", "YTD"}
    earliest = _try(lambda: hc.earliest_start(DAY))
    print("PERIODS: holding_contribution", hc.PERIODS, "| buying_trend", bt.PERIODS, "| earliest_start:", earliest)
    v.check(set(hc.PERIODS) >= need and set(bt.PERIODS) >= need and earliest == WANT["R365"],
            "(c) both PERIODS hold R30, R90, R365 and MTD, QTD, YTD; earliest_start is the R365 start")

    kept_hc = {p: _try(lambda p=p: hc.period_start(p, DAY)) for p in KEPT}
    kept_bt = {p: (starts.get(p) if isinstance(starts, dict) else starts) for p in KEPT}
    print("MTD/QTD/YTD starts: holding_contribution", {p: str(x) for p, x in kept_hc.items()},
          "| buying_trend", {p: str(x) for p, x in kept_bt.items()})
    old = {"MTD", "QTD", "YTD", "R30"}
    v.check(set(hc.PERIODS) >= old and set(bt.PERIODS) >= old and kept_hc == KEPT and kept_bt == KEPT,
            "(d) control: MTD, QTD, YTD are still periods of both tables, with unchanged starts")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
