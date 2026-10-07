"""RIV-pk-1 AC1 (row Z-S43; round-10 analysis addendum 1 @982e914b1d): Bloomberg's own key for every CUSIP/ISIN-keyed security
rides the EXISTING G4 reference request, and the one-key join reads it. Measured 2026-10-06 on G1 2026-10-01: GQGU reports Nebius
CUSIP-only (security_id null, raw N97284108, cusip N97284108, isin NL0009805522), WCMG reports `NBIS_US_Equity` with NO
CUSIP/ISIN; RIV-ok-1's CUSIP/ISIN join cannot meet them and a refresh publish at its code is byte-identical to the control.

Interface (prescribed):
  - `enrichment_bloomberg` mode `market`: the current-value reference request for an identifier-keyed security ('/cusip/..',
    '/isin/..') also asks `PARSEKYABLE_DES`; a Bloomberg-keyed security's request does NOT ask it. The answer lands in G4 column
    `security_parsekey` (e.g. "NBIS US Equity"; null when not asked or not answered).
  - `gold_holding_contribution` (and the trade schedule's position key, RIV-ok-1's `row_keys` / `stable_key`): a row keyed by a
    CUSIP/ISIN whose G4 row carries `security_parsekey` P takes the key `security_key(P)` (`NBIS_US_Equity`) when another row
    in the input window carries that key; otherwise it keeps its own key.
Fixture (offline, local sink, stubbed `_blp_reference_data` / `_blp_historical_data`; the LIVE row shape):
  - (a) the market pull for ['/cusip/N97284108', '/cusip/999999999', 'NBIS US Equity'] asks PARSEKYABLE_DES exactly for the two
    identifier keys, and G4 stores N97284108 -> "NBIS US Equity", 999999999 -> "ZZZ US Equity"; NBIS_US_Equity's parsekey is null;
  - (b) holding_contribution over G1 (GQGU N97284108 CUSIP-only, WCMG NBIS_US_Equity with no CUSIP) + that G4: both rows are in
    bucket NBIS_US_Equity, no N97284108 bucket;
  - (c) control: 999999999 (its parsekey names a key no row carries) keeps its CUSIP bucket.
FAIL at base: (a) and (b) FAIL; (c) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-05"
DAYS = ("2026-10-01", "2026-10-02")
REV = "20261002T000000Z-dddddddddddd"
SECS = ["/cusip/N97284108", "/cusip/999999999", "NBIS US Equity"]
PK = {"/cusip/N97284108": "NBIS US Equity", "/cusip/999999999": "ZZZ US Equity"}


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows(d, i):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "weight": 0.2, "security_sedol": None, "provider_security_type": None, "dataset_revision": REV,
            "gics_sector": "Information Technology"}
    mv = 1000.0 + 10.0 * i
    return [dict(base, fund_id="GQGU", fund_ticker="GQGU", security_id=None, raw_identifier="N97284108",
                 security_cusip="N97284108", security_isin="NL0009805522", security_bloomberg=None,
                 security_name="NEBIUS GROUP NV", market_value=mv),
            dict(base, fund_id="WCMG", fund_ticker="WCMG", security_id="NBIS_US_Equity", raw_identifier="NBIS US Equity",
                 security_cusip=None, security_isin=None, security_bloomberg="NBIS US Equity",
                 security_name="Nebius Group NV", market_value=mv),
            dict(base, fund_id="GQGU", fund_ticker="GQGU", security_id=None, raw_identifier="999999999",
                 security_cusip="999999999", security_isin=None, security_bloomberg=None, security_name="Zzz Corp",
                 market_value=mv)]


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, revision, sinks

    spec = f"local:{c.tmpdir('rv_pk1_')}"
    s = sinks.get_sink(spec)
    calls = []

    def ref(secs, fields, overrides=None, timeout_s=90.0):
        calls.append((list(secs), list(fields)))
        out = {}
        for x in secs:
            row = {f: None for f in fields}
            row.update({"PX_LAST": 242.81, "CRNCY": "USD", "GICS_SECTOR_NAME": "Information Technology",
                        "LONG_COMP_NAME": "Nebius Group NV" if "999" not in x else "Zzz Corp"})
            if "PARSEKYABLE_DES" in fields:
                row["PARSEKYABLE_DES"] = PK.get(x)
            out[x] = {k: row.get(k) for k in fields}
        return out

    eb._blp_reference_data = ref
    eb._blp_historical_data = lambda secs, fields, start, end, timeout_s=90.0: {}
    g4 = {}
    for d in DAYS:
        r = eb.handler_entry({"mode": "market", "date": d, "batch_id": f"pk1-{d}", "sink": spec, "securities": SECS})
        pre = homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}") + "/"
        objs = [u for u in s.list(pre) if u.endswith(".parquet")]
        df = pq.read_table(io.BytesIO(s.get(revision.newest(objs)))).to_pandas() if objs else None
        g4[d] = df
        print("G4", d, r.get("status"), "| parsekey:",
              None if df is None or "security_parsekey" not in df.columns else dict(zip(df["security_id"], df["security_parsekey"])))
    asked = {x for secs, fields in calls if "PARSEKYABLE_DES" in fields for x in secs}
    df = g4[DAYS[-1]]
    pk = {} if df is None or "security_parsekey" not in df.columns else dict(zip(df["security_id"].astype(str), df["security_parsekey"]))
    print("asked PARSEKYABLE_DES for:", sorted(asked))
    v.check(asked == {"/cusip/N97284108", "/cusip/999999999"} and pk.get("N97284108") == "NBIS US Equity"
            and pk.get("999999999") == "ZZZ US Equity" and not pk.get("NBIS_US_Equity"),
            "(a) the G4 reference request asks PARSEKYABLE_DES for exactly the identifier-keyed securities and stores it")

    for i, d in enumerate(DAYS):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))
    r = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (r.get("outputs") or [None])[0]
    out = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    sec = out[out["axis"] == "security"] if out is not None else None
    got = set() if sec is None else {(f, b) for f, b in zip(sec["fund_id"].astype(str), sec["bucket"].astype(str))}
    print("holding_contribution", r.get("status"), "| (fund, bucket):", sorted(got))
    v.check(("GQGU", "NBIS_US_Equity") in got and ("WCMG", "NBIS_US_Equity") in got and ("GQGU", "N97284108") not in got,
            "(b) GQGU's CUSIP-only Nebius row joins WCMG's NBIS_US_Equity through G4's parsekey")
    v.check(("GQGU", "999999999") in got, "(c) control: a CUSIP whose parsekey names a key no row carries keeps its CUSIP")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
