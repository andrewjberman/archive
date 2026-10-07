"""RIV-pd-1 AC2 (PRD v0.18 FWD-23; ADDENDUM F.2, F.6): driven offline on a small fixture, both stages WRITE rows for R90 and R365
on calendar-day windows, keep their MTD / QTD / YTD rows, and say in their stage detail what the R30 window was and is.

Measured today: `build-holding-contribution` and `build-buying-trend` write rows for MTD, QTD, YTD and R30 only; R30 is the 30th
NYSE trading day ending on the day; neither stage's detail names an R30 window.

Interface (prescribed, verbatim): both modules' `PERIODS` gain `R90` and `R365` and keep `MTD`, `QTD`, `YTD`. `period_start(p, day)`
and `_period_starts(day)[p]` return, for `R30` / `R90` / `R365`, `date(day) - 30 / 90 / 365` calendar days (`day` here is the as-of
the stage already passes). A fund whose history starts after the window's first day keeps the existing partial rule
(`period_clipped`, `price_coverage`). Each table's stage detail states, for one fund, the old and the new R30 window
(`r30_window_was`, `r30_window_is`).
Fixture (offline, `local:` sink, no vendor, no S3):
  - holding_contribution through `handler_entry`: page day 2026-10-06 (as-of 2026-10-05); fund PFOE, one holding, reports on
    2026-10-02 and 2026-10-05 only, so every window is clipped to the first report;
  - buying_trend through `build` (pure over frames): day 2026-10-06; fund TXUE with reports 2025-01-02 and 2026-10-05; AAA add
    ending 2025-11-03 (R365 only), BBB add ending 2026-07-20 (R90, R365, YTD), CCC trim ending 2026-10-05 (every period);
  - buying_trend through `handler_entry` on the same sink (one PFOE trade planted) for its stage detail only.
  - (a) PFOE's holding_contribution rows exist for R90 and R365; their `period_nominal_start` is 2026-07-07 and 2025-10-05, R30's
        is 2026-09-05; each is `period_clipped` True with `period_start` 2026-10-02 (the partial rule kept);
  - (b) TXUE's buying_trend security lines are R30 {CCC} from 2026-09-05, R90 {BBB, CCC} from 2026-07-07, R365 {AAA, BBB, CCC}
        from 2025-10-05 -- the SAME as-of anchor as holding_contribution (as_of(2026-10-06) = 2026-10-05; PRD F.6), issuer ruling at the cut;
  - (c) both stages' result detail carries non-empty `r30_window_was` and `r30_window_is`;
  - (d) control: both stages return OK; PFOE's MTD and YTD rows keep nominal starts 2026-10-01 and 2026-01-01; TXUE's YTD lines
        are {BBB, CCC} from 2026-01-01 and its MTD lines {CCC} from 2026-10-01.
FAIL at base: (a), (b), (c) FAIL (no R90 / R365 rows; R30 from 2026-08-25; no window keys in the detail); (d) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-06"
REV = "20261005T000000Z-aaaaaaaaaaaa"
RECENT = ("2026-10-02", "2026-10-05")


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def pfoe_g1(d, i):
    return [{"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
             "market_value": 1000.0 + 10.0 * i, "weight": 0.2, "security_bloomberg": None, "security_isin": None,
             "security_sedol": None, "provider_security_type": None, "dataset_revision": REV,
             "gics_sector": "Information Technology", "fund_id": "PFOE", "fund_ticker": "PFOE", "security_id": None,
             "raw_identifier": "999999999", "security_cusip": "999999999", "security_name": "Rho Corp"}]


def txue_g1():
    import pandas as pd
    rows = []
    for d in ("2025-01-02", "2026-10-05"):
        for k in ("AAA", "BBB", "CCC"):
            rows.append({"report_date": d, "fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": f"{k}_US_Equity",
                         "raw_identifier": f"{k} US Equity", "security_bloomberg": f"{k} US Equity", "security_name": f"{k} Corp",
                         "gics_sector": "Industrials", "is_cash_line": False, "position_type": "long", "quantity": 100.0,
                         "market_value": 1000.0, "weight": 0.1, "dataset_revision": "fx"})
    return pd.DataFrame(rows)


def txue_g5():
    import pandas as pd
    t = [("AAA", "add", "2025-11-03", 1500000.0), ("BBB", "add", "2026-07-20", 900000.0), ("CCC", "trim", "2026-10-05", -400000.0)]
    return pd.DataFrame([{"fund_id": "TXUE", "security_key": f"{k}_US_Equity", "security_id": f"{k}_US_Equity", "action": a,
                          "window_end": we, "est_notional_base": n, "dataset_revision": "fx"} for k, a, we, n in t])


def detail_windows(res):
    d = res.get("detail") if isinstance(res, dict) else None
    return (d.get("r30_window_was"), d.get("r30_window_is")) if isinstance(d, dict) else (None, None)


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_pd1_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(RECENT):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), pfoe_g1(d, i))
    put_parquet(s, homes.trade_schedule(RECENT[1], f"trade_schedule-{REV}.parquet"),
                [{"fund_id": "PFOE", "fund_ticker": "PFOE", "security_id": None, "security_key": "999999999", "action": "add",
                  "window_end": RECENT[1], "est_notional_base": 1000.0}])

    res_hc = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (res_hc.get("outputs") or [None])[0]
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    hrows = [] if df is None else df[(df["fund_id"] == "PFOE") & (df["axis"] == "security")].to_dict("records")

    def seen(p):
        return sorted({(str(r.get("period_nominal_start"))[:10], str(r.get("period_start"))[:10], bool(r.get("period_clipped")))
                       for r in hrows if r.get("period") == p})

    got_hc = {p: seen(p) for p in ("R30", "R90", "R365", "MTD", "YTD")}
    print("holding_contribution status:", res_hc.get("status"), "| PFOE (nominal, start, clipped) by period:", got_hc)
    want_hc = {"R30": [("2026-09-05", "2026-10-02", True)], "R90": [("2026-07-07", "2026-10-02", True)],
               "R365": [("2025-10-05", "2026-10-02", True)]}
    v.check(all(got_hc[p] == want_hc[p] for p in want_hc),
            "(a) holding_contribution writes R90 and R365 rows on calendar-day windows, clipped to the fund's first report")

    out = bt.build(txue_g5(), None, txue_g1(), PAGE, [{"fund_id": "TXUE", "role": "rival"}])
    trows = out.to_dict("records")

    def sec(p):
        sel = [r for r in trows if str(r.get("axis")) == "security" and str(r.get("period")) == p]
        return {str(r["bucket"]).split("_")[0] for r in sel}, sorted({str(r.get("window_start"))[:10] for r in sel})

    want_bt = {"R30": ({"CCC"}, ["2026-09-05"]), "R90": ({"BBB", "CCC"}, ["2026-07-07"]),
               "R365": ({"AAA", "BBB", "CCC"}, ["2025-10-05"])}
    got_bt = {p: sec(p) for p in ("R30", "R90", "R365", "YTD", "MTD")}
    print("buying_trend TXUE (securities, window_start) by period:", got_bt)
    v.check(all(got_bt[p] == want_bt[p] for p in want_bt),
            "(b) buying_trend writes R90 and R365 lines on calendar-day windows; R30 starts 30 calendar days back")

    res_bt = bt.handler_entry({"date": PAGE, "sink": spec})
    w_hc, w_bt = detail_windows(res_hc), detail_windows(res_bt)
    print("r30_window_was / r30_window_is: holding_contribution", w_hc, "| buying_trend", w_bt)
    v.check(all(w_hc) and all(w_bt), "(c) both stages' detail states the old and the new R30 window")

    print("buying_trend status:", res_bt.get("status"), "| detail:", res_bt.get("detail"))
    v.check(res_hc.get("status") == "OK" and res_bt.get("status") == "OK"
            and [x[0] for x in got_hc["MTD"]] == ["2026-10-01"] and [x[0] for x in got_hc["YTD"]] == ["2026-01-01"]
            and got_bt["YTD"] == ({"BBB", "CCC"}, ["2026-01-01"]) and got_bt["MTD"] == ({"CCC"}, ["2026-10-01"]),
            "(d) control: both stages run; MTD and YTD rows keep their starts")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
