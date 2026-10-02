"""RIV-ic-2 AC3 (CONTROL): an input that ARRIVED stays `arrived` with no fallback named, and a stale reading stays
`stale` -- the third state touches only inputs that did not arrive.

Interface: `gold_input_census.build(day, sink, universe_entries, readings=None)`; column `fallback` NULL on an
arrived row (absent at the base, which reads as NULL).

Offline, local sink (day 2026-09-30): the day's G1 holds TXUE's report with security A (sector Energy in the file);
the day's G4 holds A with px_close and gics_sector. Readings: fear_greed fresh, keyword_sentiment stale.
  - holdings TXUE, price A and gics A read arrived, each with a NULL fallback;
  - the fresh reading reads arrived and the stale reading reads stale."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-30"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
REV = "20260930T000000Z-aaaaaaaaaaaa"
G1 = {"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": DAY, "security_id": "A", "security_name": "Alpha",
      "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "weight": 0.9, "quantity": 10.0,
      "market_value": 100.0, "gics_sector": "Energy", "dataset_revision": REV}
READINGS = [{"source": "fear_greed", "name": "stock_price_strength", "status": "fresh", "as_of": DAY,
             "location": "s3://x"},
            {"source": "keyword_sentiment", "name": "tariffs", "status": "stale", "as_of": "2026-09-20",
             "location": "s3://y"}]


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def null(x) -> bool:
    return x is None or x != x


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    s = sinks.get_sink(f"local:{c.tmpdir('rv_ic2c_')}")
    put_parquet(s, homes.canonical_shape(DAY, f"holdings-{REV}.parquet"), [G1])
    put_parquet(s, eb.market_target_uri(DAY, "20260930T010000Z-bbbbbbbbbbbb"),
                [{"security_id": "A", "date": DAY, "px_close": 10.0, "gics_sector": "Energy"}])
    out = ic.build(DAY, s, ENTRIES, readings=READINGS)
    cols = [k for k in ("input_kind", "subject", "status", "fallback") if k in out.columns]
    print(out[cols].to_string(index=False))

    def row(kind, subj):
        x = out[(out.input_kind == kind) & (out.subject == subj)]
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    arrived = [row("holdings", "TXUE"), row("price", "A"), row("gics", "A")]
    v.check(all(r.get("status") == "arrived" and null(r.get("fallback")) for r in arrived),
            "holdings TXUE, price A and gics A read arrived with a NULL fallback")
    v.check(row("market_reading", "stock_price_strength").get("status") == "arrived"
            and row("market_reading", "tariffs").get("status") == "stale",
            "the fresh reading reads arrived, the stale reading stays stale")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
