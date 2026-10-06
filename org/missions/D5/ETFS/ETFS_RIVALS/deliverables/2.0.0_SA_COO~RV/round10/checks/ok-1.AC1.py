"""RIV-ok-1 AC1 (round-9 analysis ruling 7, COO P3): one key per security. Measured on the served 10-05 page: Nebius Group is two
securities -- `N97284108` (GQGU reports it by CUSIP only) and `NBIS_US_Equity` (WCMG reports the Bloomberg id, the same CUSIP on
the row) -- two dialogs, two ranking rows; Broadcom and Intuit carry the same class in the page's name map (`AVGO_US_Equity`,
'AVGO US Equity', '11135F101'). `gold_holding_contribution._books` keys a row by `security_id`, else by an alias of its
`raw_identifier`; the alias never joins on the CUSIP / ISIN columns.

Interface (prescribed): a row whose key is a CUSIP or ISIN takes the Bloomberg-id key that another row in the same input window
carries for that same CUSIP / ISIN (`security_cusip` / `security_isin` columns); a CUSIP with no Bloomberg counterpart keeps its
CUSIP key. The same rule keys the trade schedule's positions.
Fixture (offline, local sink): page day 2026-10-05 (as-of 10-02); reports on 10-01 and 10-02; fund GQGU holds NEB by CUSIP only
(security_id None, raw_identifier and security_cusip 'N97284108'); fund WCMG holds the same security with security_id
'NBIS_US_Equity' and security_cusip 'N97284108'; GQGU also holds ZZZ by CUSIP only ('999999999', no Bloomberg counterpart):
  - (a) holding_contribution keys GQGU's and WCMG's Nebius rows under ONE bucket, 'NBIS_US_Equity';
  - (b) control: GQGU's ZZZ keeps the bucket '999999999'.
FAIL at base: (a) FAILS (GQGU's row is bucketed 'N97284108'); (b) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-05"
DAYS = ("2026-10-01", "2026-10-02")
REV = "20261002T000000Z-dddddddddddd"


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows(d, i):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "weight": 0.2, "security_isin": None, "security_sedol": None, "provider_security_type": None,
            "dataset_revision": REV, "gics_sector": "Information Technology"}
    mv = 1000.0 + 10.0 * i
    return [dict(base, fund_id="GQGU", fund_ticker="GQGU", security_id=None, raw_identifier="N97284108",
                 security_cusip="N97284108", security_bloomberg=None, security_name="Nebius Group Nv", market_value=mv),
            dict(base, fund_id="WCMG", fund_ticker="WCMG", security_id="NBIS_US_Equity", raw_identifier="NBIS US Equity",
                 security_cusip="N97284108", security_bloomberg="NBIS US Equity", security_name="Nebius Group NV", market_value=mv),
            dict(base, fund_id="GQGU", fund_ticker="GQGU", security_id=None, raw_identifier="999999999",
                 security_cusip="999999999", security_bloomberg=None, security_name="Zzz Corp", market_value=mv)]


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_ok1_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(DAYS):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))
    r = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (r.get("outputs") or [None])[0]
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    sec = df[df["axis"] == "security"] if df is not None else None
    got = {} if sec is None else {(f, b) for f, b in zip(sec["fund_id"].astype(str), sec["bucket"].astype(str))}
    print("status", r.get("status"), "| (fund, bucket):", sorted(got))
    v.check(("GQGU", "NBIS_US_Equity") in got and ("WCMG", "NBIS_US_Equity") in got and ("GQGU", "N97284108") not in got,
            "(a) GQGU's CUSIP-only Nebius row and WCMG's row share the one bucket NBIS_US_Equity")
    v.check(("GQGU", "999999999") in got, "(b) control: a CUSIP with no Bloomberg counterpart keeps its CUSIP bucket")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
