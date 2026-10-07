"""RIV-rg-1 AC1 (PRD v0.19 C-OWED-GRAIN, G.4; row ETFS_RIVALS-Z-S69; CTO rulings msgs 31416, 31428, 31432): THE READERS. Every reader of
gold security_market (G4) takes ALL objects of a date, one row per (security_id, date), not the one `revision.newest` object.

Measured at the base (cell text): 2026-09-29 holds a live pull `market-20260929-53bc393958bd.parquet` (closes, `source`
`blp_client.reference_data`) and an import `market-20260929-afcd903ad844.parquet` (no closes, GICS, `source` `import:...`). Neither
name carries a capture time and the readers hand `revision.newest` bare uris, so the NAME decides: the import wins and the live
closes reach no stage. A top-up with a later capture time REPLACES its base for that date.

Interface (prescribed, from the cell): ONE shared function returns a date's G4 rows as the union of all `.parquet` objects of the
date's partition, one row per (security_id, date); readers moved to it: `price_series.load`, `gold_holding_contribution.handler_entry`,
`gold_buying_trend.handler_entry`, `gold_input_census.build`, `publish_page._chart_reads`, `gold_canonical_shape._g4_for` (one date
per report date, that date's rows the union), `gold_trade_schedule.load_parsekeys`. This check names NO new function: it drives each
reader through its existing entry point on a `local:` sink (arms a-f), and the rule's own details are graded in rg-1.AC2.py. Where
a handler is not driven end to end the arm calls the reader function the census names at that call site with the fixture's sink
(arm d: `gold_input_census.build`; arm e: `gold_canonical_shape._g4_for` + `apply_g4`; arm f: `gold_trade_schedule.load_parsekeys`;
arm c2: `publish_page._chart_reads`), and the arm says so.

Fixture (G4 objects built with the producer's own schema `enrichment_bloomberg.MARKET_COLUMNS` / `_market_table`, named as the cell
names them; the live rows carry `as_of_source` "pull", the import rows `as_of_source` NULL and `source` "import:..." as
`enrichment_bloomberg` writes an import):
  2026-09-29  LIVE   LVO_US_Equity close 50.0 / total return 0.4 / USD / sector Energy; SHR_US_Equity close 20.0 / total return 0.1 /
                     USD / NO sector; SHS_US_Equity close 30.0 / USD / sector Financials; N97284108 (a CUSIP) close 5.0 / USD /
                     parsekey "NBIS US Equity"
              IMPORT SHR_US_Equity sector Health Care; SHS_US_Equity sector Utilities; IMO_US_Equity sector Information Technology;
                     037833100 (a CUSIP) parsekey "AAPL US Equity"; no row of the import carries a price
  So the two objects share SHR and SHS; each holds securities the other lacks.
  - (a) `price_series.load(s, keys, 2026-09-29, 2026-09-29)`: the 09-29 close is 50.0 (LVO, priced only in the live object), 20.0 (SHR),
    30.0 (SHS), 5.0 (the CUSIP); IMO (no close in either object) stays None;
  - (b) `gold_holding_contribution.handler_entry` (page day 2026-10-05, TXUE holding LVO, SHR, IMO, G1 reports 09-28 and 09-29): the
    R30 `price_source` of LVO and SHR is NOT holding_implied (the live pull's total return prices 09-29) and LVO's contribution is
    0.004 x its 0.2 weight; IMO (no price anywhere) stays holding_implied; the sector buckets are Energy (live GICS), Health Care (the
    import's, SHR's live row has none) and Information Technology, with no Unclassified bucket;
  - (c) `gold_buying_trend.handler_entry` (RIV-al-1's frames: GQGU keyed by the CUSIP N97284108, WCMG by NBIS_US_Equity; the parsekey
    is held ONLY in the live object, the object that loses today): GQGU's security lines sit under NBIS_US_Equity, none under the CUSIP;
    (c2) `publish_page._chart_reads` over the same sink gathers GQGU's G5 trade under NBIS_US_Equity (called directly, not through the
    publisher);
  - (d) `gold_input_census.build('2026-09-29', ...)` (TXUE holding LVO, SHR, SHS, IMO): the `price` input is `arrived` for LVO, SHR and
    SHS (the live closes) and not arrived for IMO; the `gics` input is `arrived` for LVO (live only), SHR (import only) and IMO;
  - (e) `gold_canonical_shape._g4_for(s, '2026-09-29', {})`: its rows hold LVO with sector Energy (GICS only in the live pull), SHR with
    Health Care (only in the import), SHS with Financials (both hold one: the live pull's), IMO with Information Technology, and
    `apply_g4` joins the sector onto G1 rows of SHR and LVO;
  - (f) `gold_trade_schedule.load_parsekeys(s, canonical over 2026-09-29)` returns N97284108 -> "NBIS US Equity" (live object) AND
    037833100 -> "AAPL US Equity" (import object);
  - (g) NEGATIVE CONTROL (CTO): 2026-10-01 holds a base `market-20261001T110000Z-aaaaaaaaaaaa` (A_US_Equity close 10.0, B_US_Equity close
    20.0 USD) and a TOP-UP `market-20261001T150000Z-bbbbbbbbbbbb` with a LATER capture time (B_US_Equity with NO close, C_US_Equity close
    30.0): `price_series.load` and `_g4_for` read A, B and C; A and B keep their base closes (10.0, 20.0), C is added, none is removed;
  - (h) CONTROL that must PASS at base: 2026-10-02 holds three identical objects (capture times 11:05Z, 12:33Z, 12:46Z; the shape of the
    live date): the readers read exactly the rows of one object (`_g4_for` holds 3 securities; `price_series.load` the planted closes;
    the rankings table and the input census over the three objects equal those over the one newest object alone), and a single-object
    date reads as it does today (`_g4_for` returns that object, `load` its closes).
FAIL at base 4611085187: (a), (b), (c), (c2), (d), (e), (f), (g) FAIL (AC1 RESULT: FAIL 8: a, b, c, c2, d, e, f, g); (h) PASSES (from the
unmodified base: the live closes of 09-29 are unread because the import's name wins; the top-up replaces its base).
"""
import datetime as dt
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LIVE_SRC, IMPORT_SRC = "blp_client.reference_data", "import:bbg/2026-09-29/characteristics.parquet"
D29 = "2026-09-29"
LIVE_NAME, IMPORT_NAME = "market-20260929-53bc393958bd.parquet", "market-20260929-afcd903ad844.parquet"
LVO, SHR, SHS, IMO = "LVO_US_Equity", "SHR_US_Equity", "SHS_US_Equity", "IMO_US_Equity"
CUSIP, CUSIP_PK, ICUSIP, ICUSIP_PK = "N97284108", "NBIS US Equity", "037833100", "AAPL US Equity"
PAGE, ASOF = "2026-10-05", "2026-10-02"
ENTS = [{"group_id": "IDVZ", "fund_id": "TXUE", "ticker": "TXUE", "role": "rival"}]


def mrow(eb, sec, date, px=None, tri=None, ccy=None, sector=None, source=LIVE_SRC, aos="pull", pk=None):
    """One G4 row in the producer's own column set; a column not named is NULL."""
    r = {col: None for col in eb.MARKET_COLUMNS}
    r.update(security_id=sec, security_bloomberg=sec.replace("_", " "), date=dt.date.fromisoformat(date), px_close=px,
             total_return_index=tri, currency=ccy, gics_sector=sector, source=source, as_of=dt.date.fromisoformat(date),
             as_of_source=aos, security_parsekey=pk, producer_version=eb.GOLD_VERSION, input_manifest="{}", claim="MEASURED",
             produced_at=f"{date}T01:00:00Z")
    return r


def put_obj(eb, s, date, name, rows):
    """One G4 object at the producer's own address `market-<revision>.parquet`. Returns its uri."""
    rev = name[len("market-"):-len(".parquet")]
    uri = eb.market_target_uri(date, rev)
    s.put(uri, eb._parquet_bytes(eb._market_table([dict(r, revision=rev) for r in rows])), "application/octet-stream")
    return uri


def two_objects(eb, s):
    """The 2026-09-29 two-object date. Returns (live uri, import uri)."""
    live = put_obj(eb, s, D29, LIVE_NAME, [
        mrow(eb, LVO, D29, px=50.0, tri=0.4, ccy="USD", sector="Energy"),
        mrow(eb, SHR, D29, px=20.0, tri=0.1, ccy="USD"),
        mrow(eb, SHS, D29, px=30.0, ccy="USD", sector="Financials"),
        mrow(eb, CUSIP, D29, px=5.0, ccy="USD", pk=CUSIP_PK)])
    imp = put_obj(eb, s, D29, IMPORT_NAME, [
        mrow(eb, SHR, D29, sector="Health Care", source=IMPORT_SRC, aos=None),
        mrow(eb, SHS, D29, sector="Utilities", source=IMPORT_SRC, aos=None),
        mrow(eb, IMO, D29, sector="Information Technology", source=IMPORT_SRC, aos=None),
        mrow(eb, ICUSIP, D29, source=IMPORT_SRC, aos=None, pk=ICUSIP_PK)])
    return live, imp


def new_sink(tag):
    from rivalfunds import sinks
    spec = f"local:{c.tmpdir(f'rv_rg1_{tag}_')}"
    return spec, sinks.get_sink(spec)


def put_g1(s, rows_by_date):
    """TXUE G1 reports on a `local:` sink, the way test_r7cg1 writes them. rows_by_date {date: [(key, market_value), ...]}."""
    from rivalfunds import homes
    from rivalfunds.tests import test_r7cg1_census_reads_rankings_gics as t7
    for d, lines in rows_by_date.items():
        t7._put(s, homes.canonical_shape(d, f"holdings-{t7.REV}.parquet"),
                [dict(t7._line("TXUE", k, date=d), market_value=mv) for k, mv in lines])


def rankings(hc, pq, spec, s):
    try:
        r = hc.handler_entry({"date": PAGE, "sink": spec})
    except Exception as e:  # noqa: BLE001 -- a raising stage is a failed arm, not a dead check
        return {"status": f"RAISED {type(e).__name__}", "detail": str(e), "outputs": []}, None
    outs = r.get("outputs") or []
    return r, (pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas() if r.get("status") == "OK" and outs else None)


def sec_row(df, key, period="R30"):
    if df is None:
        return {}
    x = df[(df.fund_id == "TXUE") & (df.axis == "security") & (df.bucket == key) & (df.period == period)]
    return x.iloc[0].to_dict() if len(x) == 1 else {}


def near(a, b, tol=1e-9):
    return a is not None and b is not None and a == a and b == b and abs(float(a) - float(b)) < tol


def day_price(ps, s, keys, d):
    """{key: close of day d} from price_series.load over [d, d]; None for an unpriced key."""
    out = ps.load(s, keys, dt.date.fromisoformat(d), dt.date.fromisoformat(d))
    got = {}
    for k in keys:
        pts = (out.get(k) or {}).get("points") or []
        got[k] = next((p[1] for p in pts if str(p[0])[:10] == d), None)
        if got[k] is not None and got[k] != got[k]:
            got[k] = None
    return got, out


def census_cell(df, kind, key):
    x = df[(df.fund_id == "TXUE") & (df.input_kind == kind) & (df.subject == key)]
    return (x.iloc[0]["status"], x.iloc[0]["fallback"]) if len(x) == 1 else (None, None)


def guard(v, label, desc, fn):
    """Run one arm; a raising reader is that arm's failure, never a dead check."""
    try:
        ok = fn()
    except Exception as e:  # noqa: BLE001
        print(f"  ({label}) raised {type(e).__name__}: {e}")
        ok = False
    v.check(bool(ok), f"({label}) {desc}")


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_canonical_shape as g1mod
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import gold_trade_schedule as ts
    from rivalfunds import homes, price_series, publish_page, revision
    from rivalfunds.tests import test_r13al1_readers_parsekey as al1

    # ---- (a) price_series.load ------------------------------------------------------------------------------------------
    def arm_a():
        _, s = new_sink("a")
        two_objects(eb, s)
        got, out = day_price(price_series, s, [LVO, SHR, SHS, CUSIP, IMO], D29)
        print(f"  load 2026-09-29: {got} | LVO currency {(out.get(LVO) or {}).get('currency')!r}")
        return (near(got[LVO], 50.0) and near(got[SHR], 20.0) and near(got[SHS], 30.0) and near(got[CUSIP], 5.0)
                and got[IMO] is None)

    guard(v, "a", "price_series.load reads the live pull's closes of 2026-09-29 (50.0, 20.0, 30.0, 5.0) beside the import's "
                  "unpriced rows (IMO stays None)", arm_a)

    # ---- (b) the rankings -----------------------------------------------------------------------------------------------
    def arm_b():
        spec, s = new_sink("b")
        two_objects(eb, s)
        put_g1(s, {"2026-09-28": [(k, 1000.0) for k in (LVO, SHR, IMO)], D29: [(k, 1010.0) for k in (LVO, SHR, IMO)]})
        hc.universe.entries = lambda: list(ENTS)
        r, t = rankings(hc, pq, spec, s)
        rows = {k: sec_row(t, k) for k in (LVO, SHR, IMO)}
        sectors = sorted(set(t[(t.axis == "sector") & (t.period == "R30")]["bucket"].astype(str))) if t is not None else None
        for k, x in rows.items():
            print(f"  {k}: price_source {x.get('price_source')} | contribution {x.get('contribution')} | "
                  f"n_days_holding_implied {x.get('n_days_holding_implied')}")
        print(f"  status {r.get('status')} | R30 sector buckets {sectors}")
        not_implied = lambda x: x.get("price_source") not in (None, "holding_implied", "missing")  # noqa: E731
        return (r.get("status") == "OK" and not_implied(rows[LVO]) and not_implied(rows[SHR])
                and near(rows[LVO].get("contribution"), 0.004 * 0.2)
                and rows[IMO].get("price_source") == "holding_implied"
                and sectors == ["Energy", "Health Care", "Information Technology"])

    guard(v, "b", "gold_holding_contribution.handler_entry prices 2026-09-29 from the live pull's total return (LVO and SHR not "
                  "holding_implied, LVO contribution 0.0008), keeps IMO holding_implied, and classifies the sectors from both objects", arm_b)

    # ---- (c) the buying trend, (c2) the chart reads ---------------------------------------------------------------------
    def trend_sink(tag):
        spec, s = new_sink(tag)
        two_objects(eb, s)
        g1 = al1._g1()
        for d in sorted(set(g1["report_date"])):
            buf = io.BytesIO()
            import pyarrow as pa
            pq.write_table(pa.Table.from_pandas(g1[g1["report_date"] == d].reset_index(drop=True), preserve_index=False), buf)
            s.put(homes.canonical_shape(d, f"holdings-{d.replace('-', '')}T000000Z-aaaaaaaaaaaa.parquet"), buf.getvalue())
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(al1._g5(), preserve_index=False), buf)
        s.put(homes.trade_schedule(ASOF, "trades-20261002T000000Z-bbbbbbbbbbbb.parquet"), buf.getvalue())
        return spec, s

    def arm_c():
        spec, s = trend_sink("c")
        bt.universe.entries = lambda: list(al1.ENTRIES)
        r = bt.handler_entry({"date": PAGE, "sink": spec})
        outs = r.get("outputs") or []
        t = pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas() if r.get("status") == "OK" and outs else None
        if t is None:
            print(f"  handler_entry: {r.get('status')} {r.get('detail')}")
            return False
        gq = sorted(set(t[(t["axis"] == "security") & (t["fund_id"].astype(str) == "GQGU")]["bucket"].astype(str)))
        every = sorted(set(t["bucket"].astype(str)))
        print(f"  GQGU security buckets {gq} | every bucket {every}")
        return gq == ["NBIS_US_Equity"] and CUSIP not in every

    guard(v, "c", "gold_buying_trend.handler_entry joins the CUSIP-keyed fund to NBIS_US_Equity: the parsekey is held only in the "
                  "live object of the two-object date", arm_c)

    def arm_c2():
        _, s = trend_sink("c2")
        rows, _mv = publish_page._chart_reads(s, ["GQGU", "WCMG"], dt.date(2026, 9, 1), dt.date.fromisoformat(ASOF), PAGE)
        keys = sorted(rows.get("GQGU", {}))
        print(f"  _chart_reads: GQGU trade keys {keys}")
        return keys == ["NBIS_US_Equity"]

    guard(v, "c2", "publish_page._chart_reads (called directly) gathers GQGU's trade under NBIS_US_Equity", arm_c2)

    # ---- (d) the input census -------------------------------------------------------------------------------------------
    def arm_d():
        _, s = new_sink("d")
        two_objects(eb, s)
        put_g1(s, {D29: [(k, 1010.0) for k in (LVO, SHR, SHS, IMO)]})
        df = ic.build(D29, s, list(ENTS), readings=[], page_day=D29)
        price = {k: census_cell(df, "price", k) for k in (LVO, SHR, SHS, IMO)}
        gics = {k: census_cell(df, "gics", k) for k in (LVO, SHR, IMO)}
        print(f"  price {price} | gics {gics}")
        return (all(price[k][0] == "arrived" for k in (LVO, SHR, SHS)) and price[IMO][0] != "arrived"
                and all(gics[k][0] == "arrived" for k in (LVO, SHR, IMO)))

    guard(v, "d", "gold_input_census.build counts the live pull's price as arrived for LVO, SHR, SHS on 2026-09-29 (not IMO) and the "
                  "GICS of both objects as arrived", arm_d)

    # ---- (e) the canonical shape's G4 join ------------------------------------------------------------------------------
    def arm_e():
        _, s = new_sink("e")
        two_objects(eb, s)
        g = g1mod._g4_for(s, D29, {})
        rows = (g or {}).get("rows") or {}
        want = {LVO: "Energy", SHR: "Health Care", SHS: "Financials", IMO: "Information Technology"}
        got = {k: (rows.get(k) or {}).get("gics_sector") for k in want}
        g1rows = [{"security_id": k, "is_cash_line": False, "asset_class": None} for k in (SHR, LVO)]
        n = g1mod.apply_g4(g1rows, g)
        joined = {r["security_id"]: r.get("gics_sector") for r in g1rows}
        print(f"  _g4_for date {(g or {}).get('date')} sectors {got} | apply_g4 resolved {n}: {joined}")
        return got == want and n == 2 and joined == {SHR: "Health Care", LVO: "Energy"}

    guard(v, "e", "gold_canonical_shape._g4_for + apply_g4 join GICS for a security whose sector is only in the import (SHR) AND "
                  "for one only in the live pull (LVO); both-objects SHS takes the live pull's", arm_e)

    # ---- (f) load_parsekeys ---------------------------------------------------------------------------------------------
    def arm_f():
        _, s = new_sink("f")
        two_objects(eb, s)
        got = ts.load_parsekeys(s, pd.DataFrame({"report_date": [D29]}))
        print(f"  load_parsekeys: {got}")
        return got.get(CUSIP) == CUSIP_PK and got.get(ICUSIP) == ICUSIP_PK

    guard(v, "f", "gold_trade_schedule.load_parsekeys returns the key held only in the live object AND the one held only in the "
                  "import", arm_f)

    # ---- (g) NEGATIVE CONTROL: a top-up adds and removes nothing ----------------------------------------------------------
    def arm_g():
        _, s = new_sink("g")
        d = "2026-10-01"
        base = put_obj(eb, s, d, "market-20261001T110000Z-aaaaaaaaaaaa.parquet",
                       [mrow(eb, "A_US_Equity", d, px=10.0, ccy="USD"), mrow(eb, "B_US_Equity", d, px=20.0, ccy="USD")])
        top = put_obj(eb, s, d, "market-20261001T150000Z-bbbbbbbbbbbb.parquet",
                      [mrow(eb, "B_US_Equity", d), mrow(eb, "C_US_Equity", d, px=30.0, ccy="USD")])
        got, _ = day_price(price_series, s, ["A_US_Equity", "B_US_Equity", "C_US_Equity"], d)
        g = g1mod._g4_for(s, d, {})
        keys = sorted(((g or {}).get("rows") or {}))
        print(f"  top-up later than base ({revision.newest([base, top]).rsplit('/', 1)[-1]} is newest): load {got} | _g4_for keys {keys}")
        return (near(got["A_US_Equity"], 10.0) and near(got["B_US_Equity"], 20.0) and near(got["C_US_Equity"], 30.0)
                and keys == ["A_US_Equity", "B_US_Equity", "C_US_Equity"])

    guard(v, "g", "negative control: a top-up with a later capture time ADDS C and REMOVES nothing; A and B keep their base closes", arm_g)

    # ---- (h) CONTROL (passes at base): three identical objects, and a single-object date --------------------------------
    def triple_sink(tag, names):
        spec, s = new_sink(tag)
        d = ASOF
        uris = [put_obj(eb, s, d, n, [mrow(eb, "P_US_Equity", d, px=11.0, ccy="USD", sector="Energy"),
                                      mrow(eb, "Q_US_Equity", d, px=12.0, ccy="USD", sector="Utilities"),
                                      mrow(eb, "R_US_Equity", d, px=13.0, ccy="USD", sector="Materials")]) for n in names]
        put_g1(s, {"2026-10-01": [(k, 1000.0) for k in ("P_US_Equity", "Q_US_Equity", "R_US_Equity")],
                   d: [(k, 1010.0) for k in ("P_US_Equity", "Q_US_Equity", "R_US_Equity")]})
        return spec, s, uris

    def arm_h():
        names = ["market-20261002T110500Z-aaaaaaaaaaaa.parquet", "market-20261002T123300Z-bbbbbbbbbbbb.parquet",
                 "market-20261002T124600Z-cccccccccccc.parquet"]
        spec3, s3, u3 = triple_sink("h3", names)
        spec1, s1, u1 = triple_sink("h1", names[-1:])
        keys = ["P_US_Equity", "Q_US_Equity", "R_US_Equity"]
        want = {"P_US_Equity": 11.0, "Q_US_Equity": 12.0, "R_US_Equity": 13.0}
        ok = True
        hc.universe.entries = lambda: list(ENTS)
        tabs, cens, picks, loads = {}, {}, {}, {}
        for tag, spec, s in (("three", spec3, s3), ("one", spec1, s1)):
            loads[tag], _ = day_price(price_series, s, keys, ASOF)
            g = g1mod._g4_for(s, ASOF, {})
            picks[tag] = (sorted((g or {}).get("rows") or {}), (g or {}).get("uri"))
            _, t = rankings(hc, pq, spec, s)
            tabs[tag] = None if t is None else t.drop(columns=["revision", "produced_at", "input_manifest"], errors="ignore").reset_index(drop=True)
            cens[tag] = ic.build(ASOF, s, list(ENTS), readings=[], page_day=PAGE)
        newest3 = revision.newest(u3)
        print(f"  three objects: load {loads['three']} | _g4_for keys {picks['three'][0]} | rankings rows "
              f"{None if tabs['three'] is None else len(tabs['three'])} | census rows {len(cens['three'])}")
        print(f"  one object:    load {loads['one']} | _g4_for keys {picks['one'][0]} | rankings rows "
              f"{None if tabs['one'] is None else len(tabs['one'])} | census rows {len(cens['one'])}")
        ok &= all(near(loads[t][k], want[k]) for t in ("three", "one") for k in keys)
        ok &= picks["three"][0] == keys and picks["one"][0] == keys and picks["one"][1] == u1[0]
        ok &= tabs["three"] is not None and tabs["one"] is not None and len(tabs["one"]) > 0 and tabs["three"].equals(tabs["one"])
        ok &= cens["three"].reset_index(drop=True).drop(columns=["location"]).equals(cens["one"].reset_index(drop=True).drop(columns=["location"]))
        ok &= newest3 == u3[-1]
        return ok

    guard(v, "h", "control: three identical objects read as one object's rows (no duplicate, tables equal to the one-object date) "
                  "and a single-object date reads as today", arm_h)


v = c.Verdict("AC1")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- a dead fixture is a failed check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = [m.split(")")[0].lstrip("(") for m in v.fails]
print("AC1 RESULT: PASS 0 failures" if not v.fails else f"AC1 RESULT: FAIL {len(v.fails)}: {', '.join(labels)}")
sys.exit(0 if not v.fails else 1)
