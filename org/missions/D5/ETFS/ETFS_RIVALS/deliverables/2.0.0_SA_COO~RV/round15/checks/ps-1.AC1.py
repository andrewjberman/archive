"""RIV-ps-1 AC1 (PRD v0.18 FWD-22, C-MODAL-PRICE-SOURCE; ROUND15_CELLS_DRAFT.md rev 1.5): one price series per security -- market
close first, holding-implied second, a gap with its reason third.

Measured (cell text): `gold/security_market` (G4) holds 4 day partitions, `trade_schedule` 504; no module assembles a per-security
daily series. At the base there is no `rivalfunds/price_series.py`.

Interface (prescribed, verbatim from the cell): new `rivalfunds/price_series.py`. `series(g4: DataFrame, g1: DataFrame, keys,
start: date, end: date) -> {key: {"points": [(date, price|None, "m"|"i"|None)], "gaps": [{"start","end","reason"}],
"source_words": str}}`. For each NYSE trading day in `[start, end]`: the G4 `px_close` of that date when present and positive
(`m`); else the price implied by any universe fund's G1 report of that date, `market_value / quantity` with quantity > 0 (`i`;
when several funds report, the median); else `None`. Consecutive `None` days form one gap with reason `"no market close on file
and no fund reported the holding"`. `source_words` names in plain words which sources the series uses. No vendor call, no S3
call: pure over frames. `load(s, keys, start, end)` reads the two tables through the sink for the publisher.

Fixture (frames in the stages' own column names: G4 = enrichment_bloomberg.MARKET_COLUMNS, G1 = gold_canonical_shape.SCHEMA), key
AAA_US_Equity over 2026-09-01 .. 2026-09-15 (10 NYSE trading days; 09-05/06 a weekend, 09-07 Labor Day, 09-12/13 a weekend):
  09-01 G4 100.0, and TXUE reports 900 / 10 (the market close wins)      -> 100.0 m
  09-02 no G4; TXUE 1010 / 10                                             -> 101.0 i
  09-03, 09-04, 09-08 nothing (09-05 a TXUE report and 09-07 a G4 row sit on non-trading days) -> None; ONE gap 09-03..09-08
  09-09 no G4; TXUE 1020 / 10 = 102, BASG 2120 / 20 = 106                 -> 104.0 i (median of two)
  09-10 no G4; TXUE 100, BASG 103, GQGU 130                               -> 103.0 i (median of three; the mean is 111)
  09-11 no G4; TXUE reports market_value 500 at quantity 0                -> None; a second gap 09-11..09-11
  09-14 G4 107.0                                                          -> 107.0 m
  09-15 G4 px_close 0.0 (not positive); TXUE 1080 / 10                    -> 108.0 i
Key BBB_US_Equity is asked for and is in neither frame.
  - (a) `price_series.series` returns, for AAA, exactly the 10 trading days ascending, each point a (day, price, code) triple;
  - (b) a day with a positive G4 close is `m` at that close (09-01 100.0 over the fund's 90.0; 09-14 107.0);
  - (c) a day with no usable G4 close and a fund report is `i` at market_value / quantity (09-02 101.0; 09-15 108.0 under a 0.0
    close); two funds -> the median 104.0; three funds -> the median 103.0;
  - (d) a day with neither is None with code None (a quantity-0 report implies nothing); the consecutive None days are ONE gap
    each: exactly [09-03..09-08] and [09-11..09-11], each with the prescribed reason;
  - (e) `source_words` is a non-empty string for AAA; BBB (no row in either frame) is still returned: 10 None points, ONE gap
    09-01..09-15; `price_series.load` is callable with parameters (s, keys, start, end);
  - (f) control: the fixture frames hold the planted values in the stages' own column names, and lib/trading_calendar reads the
    window as the 10 expected days.
FAIL at base: (a), (b), (c), (d), (e) FAIL (no rivalfunds.price_series); (f) PASSES."""
import datetime as dt
import inspect
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

AAA, BBB = "AAA_US_Equity", "BBB_US_Equity"
START, END = dt.date(2026, 9, 1), dt.date(2026, 9, 15)
DAYS = ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-08", "2026-09-09", "2026-09-10", "2026-09-11",
        "2026-09-14", "2026-09-15"]
REASON = "no market close on file and no fund reported the holding"
EXPECT = {"2026-09-01": (100.0, "m"), "2026-09-02": (101.0, "i"), "2026-09-03": (None, None), "2026-09-04": (None, None),
          "2026-09-08": (None, None), "2026-09-09": (104.0, "i"), "2026-09-10": (103.0, "i"), "2026-09-11": (None, None),
          "2026-09-14": (107.0, "m"), "2026-09-15": (108.0, "i")}
GAPS = [("2026-09-03", "2026-09-08"), ("2026-09-11", "2026-09-11")]
# (date, px_close): 09-07 is Labor Day (a row on a non-trading day), 09-15 is a close that is not positive
G4_ROWS = [("2026-09-01", 100.0), ("2026-09-07", 55.0), ("2026-09-14", 107.0), ("2026-09-15", 0.0)]
# (fund, report date, market_value, quantity): 09-05 is a Saturday; 09-11 is a report at quantity 0
G1_ROWS = [("TXUE", "2026-09-01", 900.0, 10.0), ("TXUE", "2026-09-02", 1010.0, 10.0), ("TXUE", "2026-09-05", 660.0, 10.0),
           ("TXUE", "2026-09-09", 1020.0, 10.0), ("BASG", "2026-09-09", 2120.0, 20.0),
           ("TXUE", "2026-09-10", 1000.0, 10.0), ("BASG", "2026-09-10", 2060.0, 20.0), ("GQGU", "2026-09-10", 650.0, 5.0),
           ("TXUE", "2026-09-11", 500.0, 0.0), ("TXUE", "2026-09-15", 1080.0, 10.0)]


def _d(v) -> str:
    return str(v)[:10]


def frames():
    import pandas as pd
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_canonical_shape as g1mod

    g4 = pd.DataFrame([{**{col: None for col in eb.MARKET_COLUMNS}, "security_id": AAA, "security_bloomberg": "AAA US Equity",
                        "date": dt.date.fromisoformat(d), "px_close": px, "currency": "USD", "source": "bloomberg",
                        "as_of": dt.date.fromisoformat(d), "security_name": "Aaa Corp"} for d, px in G4_ROWS],
                      columns=eb.MARKET_COLUMNS)
    g1_cols = [f.name for f in g1mod.SCHEMA]
    g1 = pd.DataFrame([{**{col: None for col in g1_cols}, "fund_id": f, "fund_ticker": f, "report_date": dt.date.fromisoformat(d),
                        "security_id": AAA, "raw_identifier": "AAA US Equity", "resolution_status": "RESOLVED",
                        "security_bloomberg": "AAA US Equity", "security_name": "Aaa Corp", "quantity": q, "market_value": mv,
                        "weight": 0.05, "position_type": "long", "asset_class": "Equity", "is_cash_line": False,
                        "source_used": "bloomberg", "dataset_revision": "20260916T000000Z-aaaaaaaaaaaa"}
                       for f, d, mv, q in G1_ROWS], columns=g1_cols)
    return g4, g1, eb.MARKET_COLUMNS, g1_cols


def _triples(points):
    out = []
    for p in points or []:
        p = list(p) if isinstance(p, (list, tuple)) else [None, None, None]
        p = (p + [None, None, None])[:3]
        out.append((_d(p[0]), None if p[1] is None or p[1] != p[1] else float(p[1]), p[2]))
    return out


def _gaps(gaps):
    return [(_d(g.get("start")), _d(g.get("end")), g.get("reason")) for g in gaps or [] if isinstance(g, dict)]


def _near(a, b) -> bool:
    return a is not None and b is not None and abs(a - b) < 1e-9


def run(v):
    c.setup_path()
    c.offline_guards()
    from lib import trading_calendar as tc
    from rivalfunds import universe

    g4, g1, g4_cols, g1_cols = frames()
    try:
        from rivalfunds import price_series
        why = None
    except ImportError as e:
        price_series, why = None, f"{type(e).__name__}: {e}"
    print("rivalfunds.price_series:", "imported" if price_series else f"ABSENT ({why})")

    out, err = {}, None
    if price_series is not None and hasattr(price_series, "series"):
        try:
            out = price_series.series(g4, g1, [AAA, BBB], START, END) or {}
        except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
            err = f"{type(e).__name__}: {e}"
    print("series() error:", err, "| keys returned:", sorted(out) if isinstance(out, dict) else type(out).__name__)
    a = out.get(AAA) if isinstance(out, dict) else None
    a = a if isinstance(a, dict) else {}
    pts = _triples(a.get("points"))
    by_day = {d: (p, code) for d, p, code in pts}
    for d, p, code in pts:
        print("  AAA", d, p, code)

    v.check([d for d, _, _ in pts] == DAYS and all(isinstance(p, (list, tuple)) and len(p) == 3 for p in a.get("points") or []),
            f"(a) AAA's points are exactly the 10 NYSE trading days ascending, each a 3-tuple ({len(pts)} points)")

    def is_(d):
        want_p, want_c = EXPECT[d]
        got = by_day.get(d)
        if got is None:
            return False
        return got[1] == want_c and (got[0] is None if want_p is None else _near(got[0], want_p))

    v.check(is_("2026-09-01") and is_("2026-09-14"),
            "(b) a positive G4 close is source m at that close (09-01 100.0 over the fund's implied 90.0; 09-14 107.0)")
    v.check(is_("2026-09-02") and is_("2026-09-15") and is_("2026-09-09") and is_("2026-09-10"),
            "(c) no usable G4 close + a fund report is source i at market_value / quantity (101.0; 108.0 under a 0.0 close); "
            "two funds -> the median 104.0; three funds -> the median 103.0")

    gaps = _gaps(a.get("gaps"))
    print("AAA gaps:", gaps)
    v.check(all(is_(d) for d in ("2026-09-03", "2026-09-04", "2026-09-08", "2026-09-11"))
            and sorted((s, e) for s, e, _ in gaps) == GAPS and all(r == REASON for _, _, r in gaps),
            "(d) a day with neither is None / None; the consecutive None days are ONE gap each (09-03..09-08, 09-11..09-11) "
            "with the prescribed reason")

    words = a.get("source_words")
    b = out.get(BBB) if isinstance(out, dict) else None
    b = b if isinstance(b, dict) else {}
    b_pts, b_gaps = _triples(b.get("points")), _gaps(b.get("gaps"))
    load = getattr(price_series, "load", None) if price_series is not None else None
    params = list(inspect.signature(load).parameters) if callable(load) else None
    print("AAA source_words:", repr(words), "| BBB points:", len(b_pts), "priced:", sum(1 for _, p, _ in b_pts if p is not None),
          "gaps:", b_gaps, "| load params:", params)
    v.check(isinstance(words, str) and bool(words.strip())
            and [d for d, _, _ in b_pts] == DAYS and all(p is None and code is None for _, p, code in b_pts)
            and b_gaps == [("2026-09-01", "2026-09-15", REASON)] and params == ["s", "keys", "start", "end"],
            "(e) source_words is a non-empty string; a key in neither frame is 10 None points and ONE gap 09-01..09-15; "
            "load(s, keys, start, end) is callable")

    cal = [d.isoformat() for d in tc.trading_days_between(START, END)]
    funds = {str(e["ticker"]) for e in universe.entries()}
    px = {_d(r.date): r.px_close for r in g4.itertuples()}
    implied = {}
    for r in g1.itertuples():
        if r.quantity > 0:
            implied.setdefault(_d(r.report_date), []).append(r.market_value / r.quantity)
    print("calendar days:", cal)
    print("fixture G4 px_close:", px, "| fixture G1 implied:", {d: sorted(x) for d, x in sorted(implied.items())})
    v.check(cal == DAYS and sorted(EXPECT) == DAYS
            and all(col in g4_cols for col in ("security_id", "date", "px_close"))
            and all(col in g1_cols for col in ("fund_ticker", "report_date", "security_id", "quantity", "market_value"))
            and px == {"2026-09-01": 100.0, "2026-09-07": 55.0, "2026-09-14": 107.0, "2026-09-15": 0.0}
            and implied["2026-09-01"] == [90.0] and implied["2026-09-02"] == [101.0] and sorted(implied["2026-09-09"]) == [102.0, 106.0]
            and sorted(implied["2026-09-10"]) == [100.0, 103.0, 130.0] and "2026-09-11" not in implied
            and implied["2026-09-15"] == [108.0] and {f for f, _, _, _ in G1_ROWS} <= funds,
            "(f) control: the fixture frames hold the planted closes and reports in the stages' own columns, every reporting fund "
            "is a universe fund, and the trading calendar reads the window as the 10 expected days")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
