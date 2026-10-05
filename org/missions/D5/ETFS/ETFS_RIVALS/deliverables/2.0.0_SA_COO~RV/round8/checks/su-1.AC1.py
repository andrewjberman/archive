"""RIV-su-1 AC1 (CTO~Z ruling msg 29426: "ETFS_RIVALS supplies its input: a published list of every security the rivals and
Opal ETFs hold"; laptop 1.0.0_SA_CTO msg 105132 via MSTR~Z 29470 reads it for MDPF_SECCLASS FWD-9/FWD-10; Andrew-direct
@357e681ddf: "a cap on all lookback of 3 years for rivalfunds inclusions"): ETFS_RIVALS serves one security list.
Measured: no such table exists (gold holds buying_trend, canonical_shape, corporate_actions, flow_reconciliation,
holding_contribution, holdings_coverage, input_census, peer_group_map, research_hypotheses, security_market, trade_schedule).

Interface (prescribed): `rivalfunds.gold_security_universe.handler_entry({"date": <page day>, "sink": <spec>})` reads every
canonical_shape report date from (as-of minus 3 calendar years) through the as-of (the page day's NYSE T-1), newest revision
per date, and writes ONE object at
`address("rivalfunds","etfs","gold","security_universe","date=<as-of>","universe-<revision>.parquet")`, returning it in
`outputs`. One row per security, keyed as G5 keys a position (`security_bloomberg`, else CUSIP, ISIN, SEDOL, ticker, else
`raw_identifier`), with `security_id`, `security_bloomberg`, `security_cusip`, `security_isin`, `security_ticker`,
`security_name`, `first_seen`, `last_seen`, `funds` (sorted, comma-joined fund ids) and `n_report_dates`. Cash and currency
lines are not securities. Read-only on its inputs.
Fixture (offline, local sink), page day 2026-10-02 (as-of 2026-10-01; the 3-year floor is 2023-10-01):
  2023-06-01 TXUE: OLD | 2025-03-03 TXUE: AAA + a USD cash line | 2026-09-30 TXUE: AAA, BBB; IDVZ: AAA | 2026-10-01 IDVZ: CCC.
  - (a) the object exists at the security_universe address for date=2026-10-01 and holds exactly AAA, BBB, CCC;
  - (b) AAA reads first_seen 2025-03-03, last_seen 2026-09-30, funds "IDVZ,TXUE", n_report_dates 2;
  - (c) OLD (before the 3-year floor) and the cash line are absent;
  - (d) control: the canonical_shape inputs are byte-identical after the run.
FAIL at base: (a), (b), (c) FAIL (no module); (d) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, ASOF = "2026-10-02", "2026-10-01"
REV = "20261001T000000Z-aaaaaaaaaaaa"


def row(d, fund, sec, cash=False):
    return {"report_date": d, "fund_id": fund, "fund_ticker": fund, "is_cash_line": cash,
            "position_type": "cash" if cash else "long", "asset_class": "Cash" if cash else "Equity", "quantity": 100.0,
            "market_value": 1000.0, "weight": 0.1, "security_bloomberg": None if cash else f"{sec} US Equity",
            "security_cusip": None, "security_isin": None, "security_sedol": None, "security_ticker": sec,
            "raw_identifier": f"{sec} US Equity" if not cash else "USD Curncy", "security_id": None if cash else f"{sec}_US_Equity",
            "security_name": f"{sec} Corp" if not cash else "US Dollar", "dataset_revision": REV, "gics_sector": "Industrials"}


BOOKS = {"2023-06-01": [("TXUE", "OLD", False)],
         "2025-03-03": [("TXUE", "AAA", False), ("TXUE", "USD", True)],
         "2026-09-30": [("TXUE", "AAA", False), ("TXUE", "BBB", False), ("IDVZ", "AAA", False)],
         "2026-10-01": [("IDVZ", "CCC", False)]}


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from lib.opal_naming import address
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_su1_')}"
    s = sinks.get_sink(spec)
    inputs = {}
    for d, held in BOOKS.items():
        uri = homes.canonical_shape(d, f"holdings-{REV}.parquet")
        put_parquet(s, uri, [row(d, f, sec, cash) for f, sec, cash in held])
        inputs[uri] = s.get(uri)

    try:
        from rivalfunds import gold_security_universe as su
        res = su.handler_entry({"date": PAGE, "sink": spec})
    except Exception as e:  # noqa: BLE001 -- the base has no module
        res = {"status": f"ERROR {type(e).__name__}: {e}", "outputs": []}
    uri = (res.get("outputs") or [None])[0]
    want_prefix = address("rivalfunds", "etfs", "gold", "security_universe", f"date={ASOF}")
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    secs = sorted(str(b).split()[0] for b in df["security_bloomberg"].dropna()) if df is not None else []
    print("status:", res.get("status"), "| object:", uri, "| securities:", secs)
    v.check(bool(uri) and uri.startswith(want_prefix) and secs == ["AAA", "BBB", "CCC"],
            "(a) one object at the security_universe address for the as-of date, holding AAA, BBB, CCC")
    a = df[df["security_bloomberg"] == "AAA US Equity"].to_dict("records") if df is not None else []
    a = a[0] if len(a) == 1 else {}
    print("AAA:", {k: a.get(k) for k in ("first_seen", "last_seen", "funds", "n_report_dates")})
    v.check(str(a.get("first_seen"))[:10] == "2025-03-03" and str(a.get("last_seen"))[:10] == "2026-09-30"
            and str(a.get("funds")) == "IDVZ,TXUE" and int(a.get("n_report_dates") or 0) == 2,
            "(b) AAA: first_seen 2025-03-03, last_seen 2026-09-30, funds IDVZ,TXUE, 2 report dates")
    v.check(df is not None and "OLD" not in secs and not any("USD" in str(x) for x in df.get("raw_identifier", [])),
            "(c) a security seen only before the 3-year floor, and the cash line, are absent")
    v.check(all(s.get(u) == b for u, b in inputs.items()), "(d) control: the canonical_shape inputs are unchanged")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
