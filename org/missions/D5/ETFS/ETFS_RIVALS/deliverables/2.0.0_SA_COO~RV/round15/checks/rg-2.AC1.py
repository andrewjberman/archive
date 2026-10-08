"""RIV-rg-2 AC1 (PRD v0.19 C-OWED-GRAIN, G.4; row ETFS_RIVALS-Z-S71; CVO ADJUDICATION_v30 RIV-rg-1 J1; CTO rulings msgs 31477, 31480): THE UNION
IS NARROWED. The shared G4 reader (`gold_holding_contribution.g4_rows` / `g4_window`, merged in round 25 by RIV-rg-1) reads an object into
the union ONLY when `revision.capture_time` of its NAME is not None (a TIMED object, e.g. `market-20261002T111038Z-34d2fc770ae5.parquet`).
A date whose partition holds NO timed object is read as exactly ONE object: the `revision.newest` of the date's bare uris -- byte for byte
what `_newest_by_date` + `_read` returned before round 25. A date holding timed AND untimed objects is the union over the timed objects
only; its untimed objects are not read. Everything else RIV-rg-1 built stands (rg-1.AC1 / rg-1.AC2, amended in round 26).

Measured (cell text; row Z-S71): the live object `date=2026-09-29/market-20260929-53bc393958bd.parquet` holds the closes of 2026-09-30, a day
early; its `as_of` column says 2026-09-29. The merged union would read it. The old one-object readers ignored it by a name tie-break:
`revision.newest` of the date's two bare uris picks `market-20260929-afcd903ad844.parquet` (an import with no price; the later name).

Fixture (G4 objects built with the producer's own schema `enrichment_bloomberg.MARKET_COLUMNS` / `_market_table`; rows as in rg-1.AC1):
  2026-09-29 NAMED   `market-20260929-53bc393958bd.parquet` (source `blp_client.reference_data`, closes): LVO_US_Equity close 50.0 / total
                     return 0.4 / USD / Energy; SHR 20.0 / 0.1 / USD, no sector; SHS 30.0 / USD / Financials; N97284108 (a CUSIP) close 5.0 /
                     parsekey "NBIS US Equity"; and `market-20260929-afcd903ad844.parquet` (an import, `source` "import:...", NO price):
                     SHR Health Care; SHS Utilities; IMO_US_Equity Information Technology; 037833100 (a CUSIP) parsekey "AAPL US Equity"
  2026-09-30 MIXED   timed live `...T101500Z-aaaaaaaaaaaa` (T_ONLY close 10.0; BOTH no close, sector Utilities), timed live
                     `...T150000Z-bbbbbbbbbbbb` (T2_ONLY close 12.0), untimed live `market-20260930-53bc393958bd` (UNT_ONLY close 99.0; BOTH
                     close 21.0, sector Energy)
  2026-09-25 UNTIMED two untimed live objects: `market-20260925-bbbbbbbbbbbb` (close 40.0 for PRICED_US_Equity, sector Industrials) and
                     `market-20260925-aaaaaaaaaaaa` (the other one: a close for OTHER_US_Equity); `revision.newest` of the two bare uris is the
                     LATER name, `...-bbbbbbbbbbbb`, the one WITH closes for PRICED -- so "one object as before" reads its closes
  2026-10-01 TIMED   rg-1.AC1's top-up pair: base `...T110000Z-aaaaaaaaaaaa` (A close 10.0, B close 20.0), top-up `...T150000Z-bbbbbbbbbbbb`
                     (B no close, C close 30.0)

  - (a) THE NAMED CASE, every reader the round-25 checks drive, on the 2026-09-29 pair: each returns EXACTLY what it returns over a sink that
    holds only the object `revision.newest` picks (the import, printed), and the live closes reach no stage: `price_series.load` (no
    close for LVO, SHR, SHS, the CUSIP or IMO on 09-29), `gold_holding_contribution.handler_entry` (TXUE holding LVO, SHR, IMO; the
    rankings table equals the one-object sink's, LVO is holding_implied and no Energy bucket exists), `gold_buying_trend.handler_entry`
    (GQGU's security lines equal the one-object sink's and none sits under NBIS_US_Equity), `publish_page._chart_reads` (GQGU's trade keys
    equal), `gold_input_census.build` (price / gics cells equal, none `arrived` from the live closes), `gold_canonical_shape._g4_for`
    (its `rows` are exactly the import's four securities: LVO absent, close and sector equal), `gold_trade_schedule.load_parsekeys` (the CUSIP is not mapped to
    NBIS US Equity, the import's key IS: the chosen object is read, not dropped);
  - (b) `gold_holding_contribution.g4_rows(s, '2026-09-29')` returns exactly the chosen object's rows, read directly from its parquet bytes:
    the same securities, the same value in each of px_close, total_return_index, currency, gics_sector, source, security_parsekey, and no
    row of the other object;
  - (c) a date with timed AND untimed objects: `g4_rows` and `price_series.load` hold the union of the timed objects (T_ONLY 10.0, T2_ONLY
    12.0, BOTH without a close and with sector Utilities) and NOTHING of the untimed one (UNT_ONLY absent, BOTH's close 21.0 not read,
    BOTH's sector not Energy);
  - (d) a date with two untimed objects and nothing else: the closes of the object `revision.newest` picks (printed; the priced one) ARE
    read -- by `g4_rows` and by `price_series.load` -- the rule is "one object as before", not "drop untimed". PASSES at base (the base
    reads both objects, so the priced one's closes arrive too); it guards against a build that drops untimed objects entirely;
  - (e) the union still works for TIMED objects: the top-up pair reads A, B (base close kept) and C by `g4_rows` and `price_series.load`.
    PASSES at base;
  - (f) CONTROL (PASSES at base): the 2026-09-29 and 2026-09-30 fixtures are on the sink (2 and 3 objects listed); `revision.capture_time` is None for the two
    2026-09-29 names (and the 09-30 and 09-25 untimed ones) and a time for a timed name; `revision.newest` of the two bare 2026-09-29
    uris is `market-20260929-afcd903ad844.parquet`, the import (the object the old readers read).
FAIL at base bff3ec2e7f (RIV-rg-1 merged, RIV-rg-2 not built): see the last line of this docstring -- (a), (b), (c) FAIL (the merged union reads
untimed objects); (d), (e), (f) PASS.
At base bff3ec2e7f: AC1 RESULT: FAIL 3: a, b, c (measured).
"""
import datetime as dt
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LIVE_SRC, IMPORT_SRC = "blp_client.reference_data", "import:bbg/2026-09-29/characteristics.parquet"
D29 = "2026-09-29"
MISDATED, IMPORT_NAME = "market-20260929-53bc393958bd.parquet", "market-20260929-afcd903ad844.parquet"
LVO, SHR, SHS, IMO = "LVO_US_Equity", "SHR_US_Equity", "SHS_US_Equity", "IMO_US_Equity"
CUSIP, CUSIP_PK, ICUSIP, ICUSIP_PK = "N97284108", "NBIS US Equity", "037833100", "AAPL US Equity"
PAGE, ASOF = "2026-10-05", "2026-10-02"
ENTS = [{"group_id": "IDVZ", "fund_id": "TXUE", "ticker": "TXUE", "role": "rival"}]
CMP_COLS = ("px_close", "total_return_index", "currency", "gics_sector", "source", "security_parsekey")


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


def named_rows(eb):
    """(the mis-dated live object's rows, the import's rows) of 2026-09-29."""
    live = [mrow(eb, LVO, D29, px=50.0, tri=0.4, ccy="USD", sector="Energy"),
            mrow(eb, SHR, D29, px=20.0, tri=0.1, ccy="USD"),
            mrow(eb, SHS, D29, px=30.0, ccy="USD", sector="Financials"),
            mrow(eb, CUSIP, D29, px=5.0, ccy="USD", pk=CUSIP_PK)]
    imp = [mrow(eb, SHR, D29, sector="Health Care", source=IMPORT_SRC, aos=None),
           mrow(eb, SHS, D29, sector="Utilities", source=IMPORT_SRC, aos=None),
           mrow(eb, IMO, D29, sector="Information Technology", source=IMPORT_SRC, aos=None),
           mrow(eb, ICUSIP, D29, source=IMPORT_SRC, aos=None, pk=ICUSIP_PK)]
    return live, imp


def put_named(eb, s, only=None):
    """The 2026-09-29 pair on the sink (or ONLY the object named `only`). Returns (live uri, import uri) -- addresses, planted or not."""
    live_rows, imp_rows = named_rows(eb)
    out = []
    for name, rows in ((MISDATED, live_rows), (IMPORT_NAME, imp_rows)):
        if only is None or only == name:
            out.append(put_obj(eb, s, D29, name, rows))
        else:
            out.append(eb.market_target_uri(D29, name[len("market-"):-len(".parquet")]))
    return out[0], out[1]


def new_sink(tag):
    from rivalfunds import sinks
    spec = f"local:{c.tmpdir(f'rv_rg2_{tag}_')}"
    return spec, sinks.get_sink(spec)


def put_g1(s, rows_by_date):
    """TXUE G1 reports on a `local:` sink, the way test_r7cg1 writes them. rows_by_date {date: [(key, market_value), ...]}."""
    from rivalfunds import homes
    from rivalfunds.tests import test_r7cg1_census_reads_rankings_gics as t7
    for d, lines in rows_by_date.items():
        t7._put(s, homes.canonical_shape(d, f"holdings-{t7.REV}.parquet"),
                [dict(t7._line("TXUE", k, date=d), market_value=mv) for k, mv in lines])


def isnull(x):
    if x is None:
        return True
    try:
        return bool(x != x)
    except Exception:  # noqa: BLE001
        return False


def near(a, b, tol=1e-9):
    return not isnull(a) and not isnull(b) and abs(float(a) - float(b)) < tol


def same(a, b):
    """Two cell values equal, a null equal to a null."""
    if isnull(a) or isnull(b):
        return isnull(a) and isnull(b)
    return bool(a == b)


def day_price(ps, s, keys, d):
    """{key: close of day d} from price_series.load over [d, d]; None for an unpriced key."""
    out = ps.load(s, keys, dt.date.fromisoformat(d), dt.date.fromisoformat(d))
    got = {}
    for k in keys:
        pts = (out.get(k) or {}).get("points") or []
        got[k] = next((None if isnull(p[1]) else float(p[1]) for p in pts if str(p[0])[:10] == d), None)
    return got


def census_cell(df, kind, key):
    x = df[(df.fund_id == "TXUE") & (df.input_kind == kind) & (df.subject == key)]
    return (x.iloc[0]["status"], x.iloc[0]["fallback"]) if len(x) == 1 else (None, None)


def rows_by_sec(df):
    """A g4_rows frame as {security_id: {col: value}} (one entry per security; a duplicate security keeps the LAST and is flagged)."""
    out, dup = {}, []
    for r in df.to_dict("records"):
        k = str(r.get("security_id"))
        if k in out:
            dup.append(k)
        out[k] = r
    return out, dup


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
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_canonical_shape as g1mod
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import gold_trade_schedule as ts
    from rivalfunds import homes, price_series, publish_page, revision
    from rivalfunds.tests import test_r13al1_readers_parsekey as al1

    keys_a = [LVO, SHR, SHS, CUSIP, IMO]

    def rankings(spec, s):
        try:
            r = hc.handler_entry({"date": PAGE, "sink": spec})
        except Exception as e:  # noqa: BLE001
            print(f"    rankings raised {type(e).__name__}: {e}")
            return None
        outs = r.get("outputs") or []
        if r.get("status") != "OK" or not outs:
            print(f"    rankings: {r.get('status')} {r.get('detail')}")
            return None
        t = pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas()
        return t.drop(columns=["revision", "produced_at", "input_manifest"], errors="ignore").reset_index(drop=True)

    def read_all(tag, only):
        """Every reader the round-25 checks drive, on a sink holding the 09-29 pair (or only the object `only`)."""
        spec, s = new_sink(tag)
        put_named(eb, s, only)
        put_g1(s, {"2026-09-28": [(k, 1000.0) for k in (LVO, SHR, IMO)], D29: [(k, 1010.0) for k in (LVO, SHR, IMO)]})
        hc.universe.entries = lambda: list(ENTS)
        res = {"load": day_price(price_series, s, keys_a, D29)}
        res["rankings"] = rankings(spec, s)
        # the buying trend and the chart reads: RIV-al-1's frames
        g1 = al1._g1()
        for d in sorted(set(g1["report_date"])):
            buf = io.BytesIO()
            pq.write_table(pa.Table.from_pandas(g1[g1["report_date"] == d].reset_index(drop=True), preserve_index=False), buf)
            s.put(homes.canonical_shape(d, f"holdings-{d.replace('-', '')}T000000Z-aaaaaaaaaaaa.parquet"), buf.getvalue())
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(al1._g5(), preserve_index=False), buf)
        s.put(homes.trade_schedule(ASOF, "trades-20261002T000000Z-bbbbbbbbbbbb.parquet"), buf.getvalue())
        bt.universe.entries = lambda: list(al1.ENTRIES)
        r = bt.handler_entry({"date": PAGE, "sink": spec})
        outs = r.get("outputs") or []
        if r.get("status") == "OK" and outs:
            t = pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas()
            res["trend"] = sorted(set(t[(t["axis"] == "security") & (t["fund_id"].astype(str) == "GQGU")]["bucket"].astype(str)))
        else:
            print(f"    buying trend: {r.get('status')} {r.get('detail')}")
            res["trend"] = None
        rows, _mv = publish_page._chart_reads(s, ["GQGU", "WCMG"], dt.date(2026, 9, 1), dt.date.fromisoformat(ASOF), PAGE)
        res["chart"] = sorted(rows.get("GQGU", {}))
        df = ic.build(D29, s, list(ENTS), readings=[], page_day=D29)
        res["census"] = {(kind, k): census_cell(df, kind, k) for kind, ks in (("price", (LVO, SHR, SHS, IMO)), ("gics", (LVO, SHR, IMO)))
                         for k in ks}
        g = g1mod._g4_for(s, D29, {})
        res["g4for"] = {k: (None if isnull(x.get("px_close")) else float(x["px_close"]), None if isnull(x.get("gics_sector")) else x["gics_sector"])
                        for k, x in ((g or {}).get("rows") or {}).items()}
        res["parsekeys"] = ts.load_parsekeys(s, pd.DataFrame({"report_date": [D29]}))
        return res

    def chosen_name():
        _, s = new_sink("pick")
        live, imp = put_named(eb, s)
        pick = revision.newest([live, imp])
        return live, imp, pick

    # ---- (a) the named case, every reader --------------------------------------------------------------------------------
    def arm_a():
        live, imp, pick = chosen_name()
        pick_name = pick.rsplit("/", 1)[-1]
        print(f"  revision.newest of the two bare uris: {pick_name} ({'the import' if pick == imp else 'the mis-dated live object'})")
        two = read_all("a_two", None)
        one = read_all("a_one", pick_name)
        ok = pick_name in (MISDATED, IMPORT_NAME)
        verdicts = {}
        verdicts["load"] = two["load"] == one["load"] and all(x is None for x in two["load"].values())
        verdicts["rankings"] = (two["rankings"] is not None and one["rankings"] is not None and two["rankings"].equals(one["rankings"])
                                and "Energy" not in set(two["rankings"][(two["rankings"].axis == "sector")]["bucket"].astype(str)))
        lvo = two["rankings"][(two["rankings"].axis == "security") & (two["rankings"].bucket == LVO) & (two["rankings"].period == "R30")] \
            if two["rankings"] is not None else pd.DataFrame()
        verdicts["rankings_lvo_implied"] = len(lvo) == 1 and lvo.iloc[0]["price_source"] == "holding_implied"
        verdicts["trend"] = two["trend"] is not None and two["trend"] == one["trend"] and "NBIS_US_Equity" not in two["trend"]
        verdicts["chart"] = two["chart"] == one["chart"] and "NBIS_US_Equity" not in two["chart"]
        verdicts["census"] = two["census"] == one["census"] and all(st != "arrived" for (kind, k), (st, _) in two["census"].items()
                                                                  if kind == "price")
        # the chosen object is READ, not dropped: its own securities and its parsekey arrive (a build that drops untimed objects fails here)
        verdicts["g4for"] = two["g4for"] == one["g4for"] and sorted(two["g4for"]) == sorted([ICUSIP, IMO, SHR, SHS])
        verdicts["parsekeys"] = (two["parsekeys"] == one["parsekeys"] and two["parsekeys"].get(CUSIP) != CUSIP_PK
                                 and two["parsekeys"].get(ICUSIP) == ICUSIP_PK)
        for name, val in verdicts.items():
            print(f"    {'OK ' if val else 'BAD'} {name}")
        print(f"  load {two['load']} | trend GQGU {two['trend']} | chart GQGU {two['chart']} | g4for {sorted(two['g4for'])} | parsekeys {two['parsekeys']}")
        print(f"  one-object sink: load {one['load']} | trend GQGU {one['trend']} | chart GQGU {one['chart']} | g4for {sorted(one['g4for'])} | "
              f"parsekeys {one['parsekeys']}")
        return ok and all(verdicts.values())

    guard(v, "a", "every reader of the 2026-09-29 pair returns what it returns over the chosen (revision.newest) object alone, and the mis-dated "
                  "object's closes reach no stage (load: no close; LVO holding_implied, no Energy bucket; no NBIS line; no census price "
                  "arrived; LVO absent from _g4_for; the CUSIP not mapped)", arm_a)

    # ---- (b) g4_rows on the named date ----------------------------------------------------------------------------------
    def arm_b():
        _, s = new_sink("b")
        live, imp = put_named(eb, s)
        pick = revision.newest([live, imp])
        want = pq.read_table(io.BytesIO(s.get(pick))).to_pandas()
        got = hc.g4_rows(s, D29)
        g, dup = rows_by_sec(got)
        w, _ = rows_by_sec(want)
        print(f"  chosen object {pick.rsplit('/', 1)[-1]}: {sorted(w)} | g4_rows: {sorted(g)} (duplicates {dup})")
        if sorted(g) != sorted(w) or dup:
            return False
        bad = [(k, col) for k in w for col in CMP_COLS if not same(g[k].get(col), w[k].get(col))]
        print(f"  columns differing from the chosen object's rows: {bad}")
        return not bad

    guard(v, "b", "g4_rows(2026-09-29) returns exactly the rows of the object revision.newest picks (same securities, same values, no "
                  "row of the other object)", arm_b)

    # ---- (c) timed AND untimed ------------------------------------------------------------------------------------------
    def arm_c():
        _, s = new_sink("c")
        d = "2026-09-30"
        put_obj(eb, s, d, "market-20260930T101500Z-aaaaaaaaaaaa.parquet",
                [mrow(eb, "T_ONLY", d, px=10.0, ccy="USD"), mrow(eb, "BOTH", d, sector="Utilities")])
        put_obj(eb, s, d, "market-20260930T150000Z-bbbbbbbbbbbb.parquet", [mrow(eb, "T2_ONLY", d, px=12.0, ccy="USD")])
        put_obj(eb, s, d, "market-20260930-53bc393958bd.parquet",
                [mrow(eb, "UNT_ONLY", d, px=99.0, ccy="USD"), mrow(eb, "BOTH", d, px=21.0, ccy="USD", sector="Energy")])
        g, dup = rows_by_sec(hc.g4_rows(s, d))
        px = day_price(price_series, s, ["T_ONLY", "T2_ONLY", "BOTH", "UNT_ONLY"], d)
        both = g.get("BOTH") or {}
        print(f"  g4_rows securities {sorted(g)} (duplicates {dup}) | BOTH close {both.get('px_close')} sector {both.get('gics_sector')!r} | load {px}")
        return (sorted(g) == ["BOTH", "T2_ONLY", "T_ONLY"] and not dup and isnull(both.get("px_close")) and both.get("gics_sector") == "Utilities"
                and near((g.get("T_ONLY") or {}).get("px_close"), 10.0) and near((g.get("T2_ONLY") or {}).get("px_close"), 12.0)
                and near(px["T_ONLY"], 10.0) and near(px["T2_ONLY"], 12.0) and px["BOTH"] is None and px["UNT_ONLY"] is None)

    guard(v, "c", "a date with timed AND untimed objects is the union of the timed only: UNT_ONLY absent, BOTH's close 21.0 not read and its "
                  "sector Utilities (not the untimed Energy), the timed closes 10.0 and 12.0 read", arm_c)

    # ---- (d) two untimed objects only: one object as before, the newest ---------------------------------------------------
    def arm_d():
        _, s = new_sink("d")
        d = "2026-09-25"
        priced = put_obj(eb, s, d, "market-20260925-bbbbbbbbbbbb.parquet",
                         [mrow(eb, "PRICED_US_Equity", d, px=40.0, ccy="USD", sector="Industrials")])
        other = put_obj(eb, s, d, "market-20260925-aaaaaaaaaaaa.parquet", [mrow(eb, "OTHER_US_Equity", d, px=7.0, ccy="USD")])
        pick = revision.newest([priced, other])
        g, _ = rows_by_sec(hc.g4_rows(s, d))
        px = day_price(price_series, s, ["PRICED_US_Equity"], d)
        print(f"  revision.newest of the two untimed uris: {pick.rsplit('/', 1)[-1]} (the priced one is ...-bbbbbbbbbbbb) | g4_rows securities "
              f"{sorted(g)} | load {px}")
        return (pick == priced and near((g.get("PRICED_US_Equity") or {}).get("px_close"), 40.0)
                and (g.get("PRICED_US_Equity") or {}).get("gics_sector") == "Industrials" and near(px["PRICED_US_Equity"], 40.0))

    guard(v, "d", "a date with two untimed objects is read as one object, the revision.newest one (the priced one here): its closes ARE "
                  "read by g4_rows and price_series.load", arm_d)

    # ---- (e) the union still works for timed objects --------------------------------------------------------------------
    def arm_e():
        _, s = new_sink("e")
        d = "2026-10-01"
        put_obj(eb, s, d, "market-20261001T110000Z-aaaaaaaaaaaa.parquet",
                [mrow(eb, "A_US_Equity", d, px=10.0, ccy="USD"), mrow(eb, "B_US_Equity", d, px=20.0, ccy="USD")])
        put_obj(eb, s, d, "market-20261001T150000Z-bbbbbbbbbbbb.parquet",
                [mrow(eb, "B_US_Equity", d), mrow(eb, "C_US_Equity", d, px=30.0, ccy="USD")])
        g, dup = rows_by_sec(hc.g4_rows(s, d))
        px = day_price(price_series, s, ["A_US_Equity", "B_US_Equity", "C_US_Equity"], d)
        print(f"  g4_rows securities {sorted(g)} (duplicates {dup}) | load {px}")
        return (sorted(g) == ["A_US_Equity", "B_US_Equity", "C_US_Equity"] and not dup and near(px["A_US_Equity"], 10.0)
                and near(px["B_US_Equity"], 20.0) and near(px["C_US_Equity"], 30.0))

    guard(v, "e", "timed objects are still unioned: A and B (base close kept) and C (top-up only) are all read", arm_e)

    # ---- (f) control ----------------------------------------------------------------------------------------------------
    def arm_f():
        _, s = new_sink("f")
        live, imp = put_named(eb, s)
        d = "2026-09-30"
        t1 = put_obj(eb, s, d, "market-20260930T101500Z-aaaaaaaaaaaa.parquet", [mrow(eb, "T_ONLY", d, px=10.0, ccy="USD")])
        t2 = put_obj(eb, s, d, "market-20260930T150000Z-bbbbbbbbbbbb.parquet", [mrow(eb, "T2_ONLY", d, px=12.0, ccy="USD")])
        u1 = put_obj(eb, s, d, "market-20260930-53bc393958bd.parquet", [mrow(eb, "UNT_ONLY", d, px=99.0, ccy="USD")])
        listed = {x: sorted(u for u in s.list(eb.market_target_uri(x, "x").rsplit("/", 1)[0] + "/") if u.endswith(".parquet"))
                  for x in (D29, d)}
        times = {u.rsplit("/", 1)[-1]: revision.capture_time(u) for u in (live, imp, t1, t2, u1)}
        newest = revision.newest([live, imp])
        print(f"  listed {{date: n}} {({x: len(u) for x, u in listed.items()})} | capture_time {times}")
        print(f"  revision.newest of the two bare 2026-09-29 uris: {newest.rsplit('/', 1)[-1]}")
        return (len(listed[D29]) == 2 and len(listed[d]) == 3 and times[MISDATED] is None and times[IMPORT_NAME] is None
                and times[u1.rsplit("/", 1)[-1]] is None and times[t1.rsplit("/", 1)[-1]] is not None
                and times[t2.rsplit("/", 1)[-1]] is not None and newest == imp)

    guard(v, "f", "control: the fixture objects are on the sink; capture_time is None for the untimed names and a time for the timed ones; "
                  "revision.newest of the two bare 2026-09-29 uris is the import (afcd903ad844)", arm_f)


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
