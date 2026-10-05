"""RIV-hc-1 AC2 (row ETFS_RIVALS-Z-S26): a G4 total-return day is the day's own percent return, never a ratio of two days.
Measured on the served 10-05 page: G4 `total_return_index` is filled from Bloomberg DAY_TO_DAY_TOT_RETURN_GROSS_DVDS
(`enrichment_bloomberg.py:115`), the day's total return in PERCENT (MSFT 10-02: 0.9223869 against px_close 512.80 -> 517.53);
`gold_holding_contribution._daily` divides two days of it as an index (`b[1] / a[1] - 1.0`), so MSFT returned about -4,830%
on 10-02 and 7 of 13 funds were refused in every window (total_below_minus_100pct).

Interface (prescribed): the `g4_tri` return of security s on day d is `total_return_index(s, d) / 100`, read from day d's G4 row
alone (it already measures d-1 -> d); `g4_close` (px_close ratio of d-1 and d) and `holding_implied` keep their rules and order.
Fixture (offline, local sink): page day 2026-10-05 (as-of 2026-10-02); reports on 2026-10-01 and 2026-10-02: fund PFOE holds
AAA (weight 0.2), fund PCLG holds BBB (weight 0.2); G4 for 2026-10-01 and 2026-10-02:
  AAA total_return_index -0.01949698 then 0.9223869, px_close 512.80 then 517.53;  BBB total_return_index null, px_close 100 then 101.
  - (a) PFOE's MTD contribution for AAA is 0.2 x 0.009223869 (to 1e-9) with price_source g4_tri, and PFOE has no refused row;
  - (b) control: PCLG's MTD contribution for BBB is 0.2 x 0.01 (to 1e-9) with price_source g4_close.
FAIL at base: (a) FAILS (the ratio reads about -48.3, the fund is refused); (b) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-05"
REV = "20261002T000000Z-bbbbbbbbbbbb"
G4REV = "20261004T000000Z-cccccccccccc"
DAYS = ("2026-10-01", "2026-10-02")
G4 = {"2026-10-01": {"AAA_US_Equity": (512.80, -0.01949698), "BBB_US_Equity": (100.0, None)},
      "2026-10-02": {"AAA_US_Equity": (517.53, 0.9223869), "BBB_US_Equity": (101.0, None)}}


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows(d):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "weight": 0.2, "security_isin": None, "security_sedol": None, "provider_security_type": None,
            "dataset_revision": REV, "gics_sector": "Information Technology",
            "security_cusip": None}
    return [dict(base, fund_id="PFOE", fund_ticker="PFOE", security_id="AAA_US_Equity", raw_identifier="AAA US Equity", security_bloomberg="AAA US Equity",
                 security_name="Aaa Corp", market_value=51280.0),
            dict(base, fund_id="PCLG", fund_ticker="PCLG", security_id="BBB_US_Equity", raw_identifier="BBB US Equity", security_bloomberg="BBB US Equity",
                 security_name="Bbb Corp", market_value=10000.0)]


def g4_rows(d):
    return [{"security_id": k, "security_bloomberg": k.replace("_", " "), "date": d, "px_close": px, "total_return_index": tri,
             "gics_sector": "Information Technology", "security_name": k[:3].title() + " Corp"} for k, (px, tri) in G4[d].items()]


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_hc1_ac2_')}"
    s = sinks.get_sink(spec)
    for d in DAYS:
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d))
        put_parquet(s, homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", f"market-{G4REV}.parquet"),
                    g4_rows(d))
    res = hc.handler_entry({"date": PAGE, "sink": spec})
    uri = (res.get("outputs") or [None])[0]
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
    rows = [] if df is None else df.to_dict("records")
    mtd = {r.get("bucket"): r for r in rows if r.get("axis") == "security" and r.get("period") == "MTD"}
    refused = [(r.get("fund_id"), r.get("period"), r.get("bucket")) for r in rows if r.get("axis") == "refused"
               and r.get("fund_id") == "PFOE"]
    a, b = mtd.get("AAA_US_Equity", {}), mtd.get("BBB_US_Equity", {})
    print("status:", res.get("status"), str(res.get("detail"))[:300], "| MTD buckets:", sorted(mtd), "| refused:", refused)
    print("AAA:", a.get("contribution"), a.get("price_source"), "| BBB:", b.get("contribution"), b.get("price_source"))

    def near(x, want):
        return x is not None and abs(float(x) - want) < 1e-9

    v.check(near(a.get("contribution"), 0.2 * 0.009223869) and a.get("price_source") == "g4_tri" and not refused,
            "(a) AAA's MTD contribution is 0.2 x its 10-02 percent return / 100, sourced g4_tri; PFOE is not refused")
    v.check(near(b.get("contribution"), 0.2 * 0.01) and b.get("price_source") == "g4_close",
            "(b) control: PCLG's BBB (no total return) takes its px_close ratio, sourced g4_close")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
