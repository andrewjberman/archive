"""RIV-pc-1 AC1 (PRD v0.18 FWD-22; row ETFS_RIVALS-Z-S55; 1.0.0_SA_CTO~Z ruling msg 30787, shape (a)): a holding-implied
price is drawn only for a listing whose STORED quote currency is exactly USD.

Interface (prescribed, from the cell): `price_series.series(g4, g1, keys, start, end)` reads each key's quote currency from
the G4 frame: the `currency` of the key's newest G4 row that carries one (a row with no `px_close` still counts); read,
never inferred from the exchange code. Exactly "USD" -> as before (`m`, then `i`, then a gap). Anything else, and a key
with no stored currency -> market closes only: a day with no positive close is None whatever the funds report, with the
gap reason REASON_NON_USD. Each key's result gains "currency": <the stored string> | None.

Fixture (G4 = enrichment_bloomberg.MARKET_COLUMNS, G1 = gold_canonical_shape.SCHEMA), window 2026-09-01 .. 2026-09-04 (4 NYSE
trading days); on every day a fund reports market_value 1000 at quantity 10 (implied 100.0) for every key:
  AAA_US_Equity  G4 09-01 px 100.0 USD                           -> 100.0 m, then 100.0 i x3; currency "USD"
  DDD_US_Equity  G4 09-02 px None, currency USD (no close at all) -> 100.0 i x4; currency "USD" (a row without a close counts)
  JJJ_JP_Equity  G4 09-01 px 15400.0 JPY                          -> 15400.0 m, then None x3 (ONE gap 09-02..09-04); "JPY"
  LLL_LN_Equity  G4 09-03 px 812.0 GBp                            -> None x2, 812.0 m, None; two gaps; "GBp"
  XXX_LN_Equity  G4 09-01 px 9.5 USD (a London listing in dollars) -> 9.5 m, then 100.0 i x3; "USD" (not inferred from LN)
  NNN_US_Equity  no G4 row (a US-looking key with nothing stored)   -> None x4, ONE gap; currency None (unknown = non-dollar)
  CCC_US_Equity  G4 09-01 px 50.0 EUR, then 09-03 px None USD       -> 50.0 m, then 100.0 i x3; "USD" (the NEWEST row wins)
  - (a) every key is returned with a "currency" entry equal to the stored value above (None for NNN);
  - (b) the dollar keys (AAA, DDD, XXX, CCC) carry holding-implied points on the days without a close;
  - (c) the non-dollar and unknown keys (JJJ, LLL, NNN) carry NO `i` point: a day without a close is None / None;
  - (d) their gaps are exactly the runs of None days, each with REASON_NON_USD; a dollar key has no gap;
  - (e) control: the fixture frames hold the planted closes, currencies and reports in the stages' own columns, and the
    trading calendar reads the window as the 4 expected days.
FAIL at base 370ae7a279: (a), (c), (d) FAIL (no "currency" in the result; JJJ, LLL and NNN carry `i` points); (b), (e) PASS."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

START, END = dt.date(2026, 9, 1), dt.date(2026, 9, 4)
DAYS = ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"]
REASON_NON_USD = ("no market close on file (the funds' holding reports are in US dollars and this listing is not quoted "
                  "in US dollars)")
# key -> [(G4 date, px_close | None, currency | None)]
G4_ROWS = {
    "AAA_US_Equity": [("2026-09-01", 100.0, "USD")],
    "DDD_US_Equity": [("2026-09-02", None, "USD")],
    "JJJ_JP_Equity": [("2026-09-01", 15400.0, "JPY")],
    "LLL_LN_Equity": [("2026-09-03", 812.0, "GBp")],
    "XXX_LN_Equity": [("2026-09-01", 9.5, "USD")],
    "NNN_US_Equity": [],
    "CCC_US_Equity": [("2026-09-01", 50.0, "EUR"), ("2026-09-03", None, "USD")],
}
KEYS = list(G4_ROWS)
CCY = {"AAA_US_Equity": "USD", "DDD_US_Equity": "USD", "JJJ_JP_Equity": "JPY", "LLL_LN_Equity": "GBp",
       "XXX_LN_Equity": "USD", "NNN_US_Equity": None, "CCC_US_Equity": "USD"}
IMP = (100.0, "i")
NIL = (None, None)
EXPECT = {
    "AAA_US_Equity": [(100.0, "m"), IMP, IMP, IMP],
    "DDD_US_Equity": [IMP, IMP, IMP, IMP],
    "JJJ_JP_Equity": [(15400.0, "m"), NIL, NIL, NIL],
    "LLL_LN_Equity": [NIL, NIL, (812.0, "m"), NIL],
    "XXX_LN_Equity": [(9.5, "m"), IMP, IMP, IMP],
    "NNN_US_Equity": [NIL, NIL, NIL, NIL],
    "CCC_US_Equity": [(50.0, "m"), IMP, IMP, IMP],
}
GAPS = {"JJJ_JP_Equity": [("2026-09-02", "2026-09-04")], "LLL_LN_Equity": [("2026-09-01", "2026-09-02"), ("2026-09-04", "2026-09-04")],
        "NNN_US_Equity": [("2026-09-01", "2026-09-04")]}
USD_KEYS = [k for k in KEYS if CCY[k] == "USD"]
OTHER_KEYS = [k for k in KEYS if CCY[k] != "USD"]


def _d(v) -> str:
    return str(v)[:10]


def _bbg(key: str) -> str:
    return key.replace("_", " ")


def frames():
    import pandas as pd
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_canonical_shape as g1mod

    g4 = pd.DataFrame([{**{col: None for col in eb.MARKET_COLUMNS}, "security_id": k, "security_bloomberg": _bbg(k),
                        "date": dt.date.fromisoformat(d), "px_close": px, "currency": ccy, "source": "bloomberg",
                        "as_of": dt.date.fromisoformat(d), "security_name": k[:3] + " Corp"}
                       for k, rows in G4_ROWS.items() for d, px, ccy in rows], columns=eb.MARKET_COLUMNS)
    g1_cols = [f.name for f in g1mod.SCHEMA]
    g1 = pd.DataFrame([{**{col: None for col in g1_cols}, "fund_id": "TXUE", "fund_ticker": "TXUE",
                        "report_date": dt.date.fromisoformat(d), "security_id": k, "raw_identifier": _bbg(k),
                        "resolution_status": "RESOLVED", "security_bloomberg": _bbg(k), "security_name": k[:3] + " Corp",
                        "quantity": 10.0, "market_value": 1000.0, "weight": 0.05, "position_type": "long",
                        "asset_class": "Equity", "is_cash_line": False, "source_used": "bloomberg",
                        "dataset_revision": "20260916T000000Z-aaaaaaaaaaaa"} for k in KEYS for d in DAYS], columns=g1_cols)
    return g4, g1, eb.MARKET_COLUMNS, g1_cols


def _pairs(points):
    out = []
    for p in points or []:
        p = (list(p) if isinstance(p, (list, tuple)) else []) + [None, None, None]
        out.append((_d(p[0]), None if p[1] is None or p[1] != p[1] else float(p[1]), p[2]))
    return out


def _same(got, want) -> bool:
    if len(got) != len(want) or [d for d, _, _ in got] != DAYS:
        return False
    for (_, p, code), (wp, wc) in zip(got, want):
        if code != wc or (p is None) != (wp is None) or (p is not None and abs(p - wp) > 1e-9):
            return False
    return True


def run(v):
    c.setup_path()
    c.offline_guards()
    from lib import trading_calendar as tc
    from rivalfunds import price_series, universe

    g4, g1, g4_cols, g1_cols = frames()
    out, err = {}, None
    try:
        out = price_series.series(g4, g1, KEYS, START, END) or {}
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        err = f"{type(e).__name__}: {e}"
    print("series() error:", err, "| keys returned:", sorted(out) if isinstance(out, dict) else type(out).__name__)
    res = {k: (out.get(k) if isinstance(out.get(k), dict) else {}) for k in KEYS} if isinstance(out, dict) else {k: {} for k in KEYS}
    pts = {k: _pairs(res[k].get("points")) for k in KEYS}
    for k in KEYS:
        print(f"  {k}: currency {res[k].get('currency', '<absent>')!r} | points {[(p, code) for _, p, code in pts[k]]} | gaps "
              f"{[(_d(g.get('start')), _d(g.get('end'))) for g in res[k].get('gaps') or [] if isinstance(g, dict)]}")

    v.check(all("currency" in res[k] and res[k]["currency"] == CCY[k] for k in KEYS),
            "(a) every key carries its stored quote currency (the newest G4 row that has one; None when none is stored)")
    v.check(all(_same(pts[k], EXPECT[k]) for k in USD_KEYS),
            "(b) a listing stored as USD keeps its holding-implied points on days without a close (a London listing stored "
            "as USD included; a row with no close still gives the currency; the newest row wins over an older EUR one)")
    v.check(all(_same(pts[k], EXPECT[k]) for k in OTHER_KEYS) and not any(code == "i" for k in OTHER_KEYS for _, _, code in pts[k]),
            "(c) a listing stored as JPY or GBp, and a key with no stored currency, carries no holding-implied point: a day "
            "without a close is None / None")
    ok_d = True
    for k in OTHER_KEYS:
        gaps = sorted((_d(g.get("start")), _d(g.get("end")), g.get("reason")) for g in res[k].get("gaps") or [] if isinstance(g, dict))
        ok_d = ok_d and [(s, e) for s, e, _ in gaps] == GAPS[k] and all(r == REASON_NON_USD for _, _, r in gaps)
    ok_d = ok_d and all(not (res[k].get("gaps") or []) for k in USD_KEYS)
    v.check(ok_d, "(d) their gaps are exactly the runs of None days with the non-dollar reason; a dollar key has no gap")

    cal = [d.isoformat() for d in tc.trading_days_between(START, END)]
    funds = {str(e["ticker"]) for e in universe.entries()}
    planted = {k: [(_d(r.date), None if r.px_close != r.px_close or r.px_close is None else float(r.px_close), r.currency)
                   for r in g4[g4.security_id == k].itertuples()] for k in KEYS}
    implied = {(r.security_id, _d(r.report_date)): r.market_value / r.quantity for r in g1.itertuples()}
    print("calendar days:", cal, "| G4 rows planted:", sum(len(x) for x in planted.values()), "| G1 rows:", len(g1))
    v.check(cal == DAYS and all(col in g4_cols for col in ("security_id", "date", "px_close", "currency"))
            and all(col in g1_cols for col in ("fund_ticker", "report_date", "security_id", "quantity", "market_value"))
            and planted == {k: [(d, px, ccy) for d, px, ccy in rows] for k, rows in G4_ROWS.items()}
            and len(implied) == len(KEYS) * len(DAYS) and set(implied.values()) == {100.0} and "TXUE" in funds,
            "(e) control: the fixture frames hold the planted closes, currencies and reports in the stages' own columns, and "
            "the trading calendar reads the window as the 4 expected days")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
