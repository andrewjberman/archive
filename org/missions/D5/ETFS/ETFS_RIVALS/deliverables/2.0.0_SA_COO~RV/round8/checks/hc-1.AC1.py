"""RIV-hc-1 AC1 (PRD v0.14 FWD-13/14; Andrew smoke S3/S7): the rankings' rolling period is the last 30 TRADING days, and every
row says up front whether its window is the period's own or was clipped to the fund's first report. Measured: `R30` starts
29 calendar days back (`gold_holding_contribution.py:123`); YTD is clipped to the fund's first report (`:411`, `:417`) with no
field saying so, so the page labels IDVZ's 2026-08-21..10-01 window "Year to date (2026)".

Interface (prescribed):
  - `period_start("R30", day)` is the 30th NYSE trading day ending on `day` (inclusive): `trading_days_between(.., day)[-30]`;
  - every holding_contribution row carries `period_nominal_start` (the period's own start: 01-01 for YTD, the 30th trading
    day for R30, ...) and `period_clipped` (True when `period_start` > `period_nominal_start` because the fund's first
    report is later).
Fixture (offline, local sink): page day 2026-10-02 (as-of 2026-10-01); fund PFOE with reports on 2026-09-30 and 2026-10-01.
  - (a) `period_start("R30", "2026-10-01")` is the 30th trading day ending 2026-10-01;
  - (b) PFOE's YTD rows read period_nominal_start 2026-01-01, period_start 2026-09-30, period_clipped True;
  - (c) control: PFOE's MTD rows read period_start 2026-10-01 and period_clipped False.
FAIL at base: (a) and (b) FAIL; (c) FAILS only on the missing `period_clipped` column, so it is graded on period_start alone
when the column is absent (PASS at base)."""
import datetime as dt
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-02"
REV = "20261001T000000Z-aaaaaaaaaaaa"
RECENT = ("2026-09-30", "2026-10-01")


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows(d, i):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "market_value": 1000.0 + 10.0 * i, "weight": 0.2, "security_bloomberg": None, "security_isin": None,
            "security_sedol": None, "provider_security_type": None, "dataset_revision": REV,
            "gics_sector": "Information Technology", "fund_id": "PFOE", "fund_ticker": "PFOE", "security_id": None}
    return [dict(base, raw_identifier="999999999", security_cusip="999999999", security_name="Rho Corp")]


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from lib import trading_calendar as tc
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, sinks

    want = tc.trading_days_between(dt.date(2026, 7, 1), dt.date(2026, 10, 1))[-30]
    got = hc.period_start("R30", "2026-10-01")
    print("R30 start:", got, "| 30th trading day ending 2026-10-01:", want)
    v.check(got == want, "(a) R30 starts on the 30th trading day ending on the as-of date")

    spec = f"local:{c.tmpdir('rv_hc1_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(RECENT):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))
    res = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (res.get("outputs") or [None])[0]
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    rows = [] if df is None else df[(df["fund_id"] == "PFOE") & (df["axis"] == "security")].to_dict("records")

    def per(p):
        return [r for r in rows if r.get("period") == p]

    ytd, mtd = per("YTD"), per("MTD")
    show = [(r["period"], str(r.get("period_start"))[:10], str(r.get("period_nominal_start"))[:10], r.get("period_clipped"))
            for r in ytd[:1] + mtd[:1]]
    print("PFOE (period, start, nominal, clipped):", show)
    v.check(bool(ytd) and all(str(r.get("period_nominal_start"))[:10] == "2026-01-01" and str(r.get("period_start"))[:10] == "2026-09-30"
                              and r.get("period_clipped") in (True, 1) for r in ytd),
            "(b) PFOE's YTD rows name the nominal start 2026-01-01, the clipped start 2026-09-30, and period_clipped True")
    v.check(bool(mtd) and all(str(r.get("period_start"))[:10] == "2026-10-01" for r in mtd)
            and all(r.get("period_clipped") in (False, 0, None) for r in mtd),
            "(c) control: PFOE's MTD rows start 2026-10-01 and are not clipped")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
