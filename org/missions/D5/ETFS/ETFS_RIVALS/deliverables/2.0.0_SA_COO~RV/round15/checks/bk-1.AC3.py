"""RIV-bk-1 AC3 (PRD v0.18 FWD-15 / FWD-22; row ETFS_RIVALS-Z-S57 and its cause Z-S61; change 4 of the cell): the buying
trend's own G4 read loads `security_parsekey`, so a fund whose lines are keyed by a CUSIP joins the Bloomberg key the
other funds carry (RIV-al-1's join, which today only `build` has: the stage never hands it the column).

Measured at the base: `gold_buying_trend.handler_entry` reads G4 with the column tuple ("security_id", "date",
"security_name"), so `parsekey_map(g4)` is {} in the stage and the CUSIP-keyed rows keep the CUSIP as their bucket.

Interface (prescribed, from the cell): `gold_buying_trend.handler_entry`'s own G4 read loads `security_parsekey`. The read
is the module's `_read(s, uris, columns)`; this check wraps `gold_buying_trend._read` and accepts a security_market read
whose column tuple names `security_parsekey`, or one that passes no column filter at all (every column loaded).

Fixture builders reused: `rivalfunds.tests.test_r13al1_readers_parsekey` (`_g1`, `_g5`, `ENTRIES`: RIV-al-1's own frames --
GQGU holds raw identifier N97284108 with no security_id, WCMG holds NBIS_US_Equity / "NBIS US Equity", reports 2026-10-01
and 2026-10-02; one GQGU add of 5,000,000 under security_key N97284108 in the window ending 2026-10-02) written to a
`local:` sink at `homes.canonical_shape` / `homes.trade_schedule` the way `test_r8bt1_periods` writes its handler fixture,
and G4 for 2026-10-02 built by the producer's own row builder (`enrichment_bloomberg.market_rows`) from the request
"/cusip/N97284108" answered PARSEKYABLE_DES "NBIS US Equity": one row security_id N97284108, security_parsekey
"NBIS US Equity". Page day 2026-10-05; `universe.entries` pinned to the two funds.
  - (a) `handler_entry` returns OK and the written trend table carries GQGU's security lines under ONE bucket,
    NBIS_US_Equity, with no row of the table under the CUSIP N97284108;
  - (b) the stage's security_market read asks for `security_parsekey` (or filters no column);
  - (c) control: `gold_holding_contribution.parsekey_map` over the fixture's full G4 object returns
    {N97284108: NBIS_US_Equity}; `build` handed that full frame gives the one bucket NBIS_US_Equity and handed the frame
    cut to the base's three columns gives N97284108 (so arm (a) can fail); the stage made a security_market read.
FAIL at base 0ed013f33d: (a), (b) FAIL (the bucket is N97284108; the read's columns are security_id, date, security_name);
(c) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY, WINDOW = "2026-10-05", "2026-10-02"
CUSIP, KEY, PARSEKEY = "N97284108", "NBIS_US_Equity", "NBIS US Equity"
BASE_COLUMNS = ["security_id", "date", "security_name"]


def fixture():
    """The RIV-al-1 frames on a fresh `local:` sink. Returns (spec, sink, g4 uri)."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks
    from rivalfunds.tests import test_r13al1_readers_parsekey as al1

    spec = f"local:{c.tmpdir('rv_bk1_trend_')}"
    s = sinks.get_sink(spec)

    def put(uri, df):
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(df, preserve_index=False), buf)
        s.put(uri, buf.getvalue())

    g1 = al1._g1()
    for d in sorted(set(g1["report_date"])):
        put(homes.canonical_shape(d, f"holdings-{d.replace('-', '')}T000000Z-aaaaaaaaaaaa.parquet"),
            g1[g1["report_date"] == d].reset_index(drop=True))
    put(homes.trade_schedule(WINDOW, "trades-20261002T000000Z-bbbbbbbbbbbb.parquet"), al1._g5())
    prov = {"revision": "20261002T010000Z-cccccccccccc", "produced_at": "2026-10-02T01:00:00Z",
            "producer_version": eb.GOLD_VERSION, "input_manifest": "{}"}
    rows = eb.market_rows({f"/cusip/{CUSIP}": {"PX_LAST": 5.0, "CRNCY": "USD", eb.PARSEKEY_FIELD: PARSEKEY}}, WINDOW,
                          eb.MARKET_SOURCE_LIVE, prov, "pull")
    g4_uri = eb.market_target_uri(WINDOW, prov["revision"])
    s.put(g4_uri, eb._parquet_bytes(eb._market_table(rows)), "application/octet-stream")
    return spec, s, g4_uri


def buckets(df, fund="GQGU"):
    if df is None or not len(df):
        return []
    return sorted(set(df[(df["axis"] == "security") & (df["fund_id"].astype(str) == fund)]["bucket"].astype(str)))


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow.parquet as pq

    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds.tests import test_r13al1_readers_parsekey as al1

    spec, s, g4_uri = fixture()
    bt.universe.entries = lambda: list(al1.ENTRIES)
    reads, inner = [], bt._read

    def recording(sink, uris, columns=None, *a, **k):
        reads.append((sorted((uris or {}).values()) if isinstance(uris, dict) else list(uris or []),
                      None if columns is None else tuple(columns)))
        return inner(sink, uris, columns, *a, **k)

    bt._read = recording
    try:
        r = bt.handler_entry({"date": DAY, "sink": spec})
    except Exception as e:  # noqa: BLE001 -- a raising stage is a failed arm, not a dead check
        r = {"status": f"RAISED {type(e).__name__}", "detail": str(e), "outputs": []}
    finally:
        bt._read = inner
    outs = r.get("outputs") or []
    table = pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas() if r.get("status") == "OK" and outs else None
    got = buckets(table)
    every = [] if table is None else sorted(set(table["bucket"].astype(str)))
    print(f"handler_entry: status {r.get('status')} | rows {None if table is None else len(table)} | GQGU security buckets {got} | "
          f"every bucket of the table {every}")
    v.check(r.get("status") == "OK" and got == [KEY] and CUSIP not in every,
            "(a) the trend table carries the CUSIP-keyed fund's lines under the one Bloomberg key, none under the CUSIP")

    g4_reads = [cols for uris, cols in reads if any("security_market" in u for u in uris)]
    print(f"_read calls: {len(reads)} | security_market reads and their columns: {g4_reads}")
    v.check(bool(g4_reads) and all(cols is None or "security_parsekey" in cols for cols in g4_reads),
            "(b) the stage's own security_market read loads security_parsekey")

    full = pq.read_table(io.BytesIO(s.get(g4_uri))).to_pandas()
    pk = hc.parsekey_map(full)
    with_pk = buckets(bt.build(al1._g5(), pd.DataFrame(), al1._g1(), DAY, al1.ENTRIES, full))
    without = buckets(bt.build(al1._g5(), pd.DataFrame(), al1._g1(), DAY, al1.ENTRIES, full[BASE_COLUMNS]))
    print(f"control: parsekey_map(full G4) {pk} | build on the full frame {with_pk} | build on the frame cut to {BASE_COLUMNS} "
          f"{without} | security_market reads seen {len(g4_reads)}")
    v.check(pk == {CUSIP: KEY} and with_pk == [KEY] and without == [CUSIP] and len(g4_reads) >= 1,
            "(c) control: the fixture's G4 maps the CUSIP to the Bloomberg key, build joins on it when handed the column and "
            "keeps the CUSIP when it is not")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
