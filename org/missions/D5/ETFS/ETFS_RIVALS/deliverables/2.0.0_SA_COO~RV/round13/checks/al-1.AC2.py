"""RIV-al-1 AC2 (ROUND_ANALYSIS.round10.md ADDENDUM 5 @a8fb9c1df1): one security under two listings resolves to ONE key in the
rankings, the trend and the input census alike, through G4's `security_parsekey` (RIV-pk-1).

Plant (offline, local sink): G1 for 2026-10-01 and 2026-10-02 -- GQGU holds Nebius CUSIP-only (security_id null, raw/cusip
N97284108), WCMG holds `NBIS_US_Equity` (no CUSIP); G4 at both dates carries N97284108 -> security_parsekey "NBIS US Equity"
(and px_close / gics_sector for both keys); a G5 trade of GQGU keyed `N97284108` (the key a G5 written before pk-1 carries).
  - (a) rankings: `gold_holding_contribution.handler_entry` buckets GQGU's and WCMG's Nebius rows under NBIS_US_Equity, none
    under N97284108 (pk-1, already true: the control that the plant is live);
  - (b) trend: `gold_buying_trend.build(g5, g6, g1, day, entries, g4)` puts GQGU's Nebius trade in security bucket NBIS_US_Equity,
    no N97284108 bucket (the reader takes the parsekey from the `g4` it is given);
  - (c) census: `gold_input_census.build(day, sink, entries)` names GQGU's Nebius price/gics inputs by NBIS_US_Equity, no
    N97284108 subject.
FAIL at base: (b) and (c) FAIL; (a) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-05"
DAYS = ("2026-10-01", "2026-10-02")
REV = "20261002T000000Z-dddddddddddd"
G4REV = "20261002T010000Z-ffffffffffff"
ENTRIES = [{"group_id": "G1", "fund_id": "GQGU", "ticker": "GQGU", "role": "home"},
           {"group_id": "G1", "fund_id": "WCMG", "ticker": "WCMG", "role": "rival"}]


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
                 security_name="Nebius Group NV", market_value=mv)]


def g4_rows(d):
    base = {"date": d, "px_close": 242.81, "gics_sector": "Information Technology", "security_name": "Nebius Group NV",
            "currency": "USD", "as_of": d, "as_of_source": "pull", "revision": G4REV}
    return [dict(base, security_id="N97284108", security_parsekey="NBIS US Equity"),
            dict(base, security_id="NBIS_US_Equity", security_parsekey=None)]


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow.parquet as pq

    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_al1_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(DAYS):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))
        put_parquet(s, homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", f"market-{G4REV}.parquet"),
                    g4_rows(d))

    r = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (r.get("outputs") or [None])[0]
    out = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    sec = out[out["axis"] == "security"] if out is not None else None
    got = set() if sec is None else {(f, b) for f, b in zip(sec["fund_id"].astype(str), sec["bucket"].astype(str))}
    print("rankings:", r.get("status"), sorted(got))
    v.check(("GQGU", "NBIS_US_Equity") in got and ("GQGU", "N97284108") not in got,
            "(a) rankings: GQGU's Nebius row is bucket NBIS_US_Equity (pk-1; the plant is live)")

    g1 = pd.concat([pd.DataFrame(g1_rows(d, i)) for i, d in enumerate(DAYS)], ignore_index=True)
    g4 = pd.concat([pd.DataFrame(g4_rows(d)) for d in DAYS], ignore_index=True)
    g5 = pd.DataFrame([{"fund_id": "GQGU", "fund_ticker": "GQGU", "security_id": None, "security_key": "N97284108",
                        "action": "add", "window_end": DAYS[-1], "est_notional_base": 5_000_000.0}])
    try:
        tb = bt.build(g5, pd.DataFrame(), g1, PAGE, ENTRIES, g4)
        tsec = tb[(tb["axis"] == "security") & (tb["fund_id"].astype(str) == "GQGU")]
        tbk = set(tsec["bucket"].astype(str))
    except Exception as e:  # noqa: BLE001
        print("trend build raised:", type(e).__name__, e)
        tbk = set()
    print("trend GQGU security buckets:", sorted(tbk))
    v.check("NBIS_US_Equity" in tbk and "N97284108" not in tbk,
            "(b) trend: GQGU's Nebius trade is bucket NBIS_US_Equity, no N97284108 bucket")

    try:
        cdf = ic.build(DAYS[-1], s, ENTRIES, [], page_day=PAGE)
        rows = cdf[(cdf["fund_id"].astype(str) == "GQGU") & (cdf["input_kind"].isin(["price", "gics"]))]
        subj = set(rows["subject"].astype(str))
    except Exception as e:  # noqa: BLE001
        print("census build raised:", type(e).__name__, e)
        subj = set()
    print("census GQGU price/gics subjects:", sorted(subj))
    v.check("NBIS_US_Equity" in subj and "N97284108" not in subj,
            "(c) census: GQGU's Nebius price/gics inputs are named NBIS_US_Equity, none N97284108")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
