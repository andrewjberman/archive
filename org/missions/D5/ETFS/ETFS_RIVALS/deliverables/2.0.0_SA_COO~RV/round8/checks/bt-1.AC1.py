"""RIV-bt-1 AC1 (PRD v0.14 FWD-15: the buying trend runs "over the period the page is set to", the last 30 trading days by
default): the buying-trend table carries one block of rows per period -- R30, MTD, QTD, YTD -- each with its own window.
Measured: `gold_buying_trend.build` writes the year to date only (`:157` start = 01-01; `:210` clip), and the page's period
switch never reaches the trend card.

Interface (prescribed): `gold_buying_trend.build(g5, g6, g1, day, universe_entries)` returns rows with a `period` column in
{R30, MTD, QTD, YTD}; each period's rows carry that period's `window_start` (R30: the 30th NYSE trading day ending on `day`;
MTD/QTD/YTD: the period's first trading day, clipped to the fund's first report as today), `window_end` = `day`, and
`n_trading_days` for that window; a period with no trade for the fund writes no line rows for it (as YTD does today). The YTD
rows are today's rows.
Fixture: day 2026-10-02; fund TXUE (reports 2026-01-02 and 2026-10-01); three trades: AAA add ending 2026-03-02 (YTD only),
BBB add ending 2026-09-10 (YTD, QTD, R30), CCC trim ending 2026-10-02 (every period).
  - (a) the rows carry a `period` column holding R30, MTD, QTD and YTD;
  - (b) each period's security lines are exactly its trades' securities: R30 {BBB, CCC}, MTD {CCC}, QTD {BBB, CCC}, and its
        window_start is that period's start (R30 = the 30th trading day ending 2026-10-02);
  - (c) control: the YTD security lines are {AAA, BBB, CCC} with window_start 2026-01-02, as today.
FAIL at base: (a) and (b) FAIL; (c) PASSES (rows with no `period` column are read as YTD)."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-02"


def g1():
    import pandas as pd
    rows = []
    for d in ("2026-01-02", "2026-10-01"):
        for k in ("AAA", "BBB", "CCC"):
            rows.append({"report_date": d, "fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": f"{k}_US_Equity",
                         "raw_identifier": f"{k} US Equity", "security_bloomberg": f"{k} US Equity", "security_name": f"{k} Corp",
                         "gics_sector": "Industrials", "is_cash_line": False, "position_type": "long", "quantity": 100.0,
                         "market_value": 1000.0, "weight": 0.1, "dataset_revision": "fx"})
    return pd.DataFrame(rows)


def g5():
    import pandas as pd
    t = [("AAA", "add", "2026-03-02", 1500000.0), ("BBB", "add", "2026-09-10", 900000.0), ("CCC", "trim", "2026-10-02", -400000.0)]
    return pd.DataFrame([{"fund_id": "TXUE", "security_key": f"{k}_US_Equity", "security_id": f"{k}_US_Equity", "action": a,
                          "window_end": we, "est_notional_base": n, "dataset_revision": "fx"} for k, a, we, n in t])


def run(v):
    c.setup_path()
    c.offline_guards()
    from lib import trading_calendar as tc
    from rivalfunds import gold_buying_trend as bt

    out = bt.build(g5(), None, g1(), DAY, [{"fund_id": "TXUE", "role": "rival"}])
    rows = out.to_dict("records")
    has = "period" in out.columns
    periods = sorted({str(r.get("period")) for r in rows}) if has else []
    print("columns has period:", has, "| periods:", periods)
    v.check(has and set(periods) >= {"R30", "MTD", "QTD", "YTD"}, "(a) the rows carry a period column with R30, MTD, QTD, YTD")

    def sec(p):
        sel = [r for r in rows if str(r.get("axis")) == "security" and (str(r.get("period")) == p if has else p == "YTD")]
        return {str(r["bucket"]).split("_")[0] for r in sel}, sorted({str(r.get("window_start"))[:10] for r in sel})

    r30_start = tc.trading_days_between(dt.date(2026, 7, 1), dt.date.fromisoformat(DAY))[-30].isoformat()
    want = {"R30": ({"BBB", "CCC"}, [r30_start]), "MTD": ({"CCC"}, ["2026-10-01"]), "QTD": ({"BBB", "CCC"}, ["2026-07-01"])}
    got = {p: sec(p) for p in want}
    print("got:", got, "| want:", want)
    v.check(has and all(got[p][0] == want[p][0] and got[p][1] == want[p][1] for p in want),
            "(b) each period's lines are its own trades' securities, with its own window_start")
    ytd = sec("YTD")
    print("YTD:", ytd)
    v.check(ytd == ({"AAA", "BBB", "CCC"}, ["2026-01-02"]), "(c) control: YTD holds AAA, BBB, CCC from 2026-01-02, as today")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
