"""RIV-ic-1 AC1 (FWD-20, amendment A1) -- the input census names every expected input's arrival; nothing expected is skipped.

Offline, local sink (day 2026-09-30): the day's G1 holds TXUE (securities A, B, C plus a cash line); SCHY has no rows. The
day's G4 holds A (px_close and gics_sector) and B (px_close, no gics_sector); C has no G4 row. Two readings are passed in:
fear_greed fresh and keyword_sentiment stale.
  - holdings: TXUE arrived; SCHY missing, with a reason;
  - price: A and B arrived, C missing; gics: A arrived, B and C missing; the cash line has no price or gics row;
  - market_reading: fear_greed arrived, keyword_sentiment stale;
  - control: exactly 10 rows (2 holdings + 3 price + 3 gics + 2 readings), every status in {arrived, missing, stale}."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-30"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}, {"group_id": "IDVZ", "fund_id": "SCHY", "role": "index_control"}]


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    s = sinks.get_sink(f"local:{c.tmpdir('rv_ic1_')}")
    g1 = [{"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": DAY, "security_id": k, "security_name": k,
           "is_cash_line": False, "position_type": "long", "weight": 0.3, "dataset_revision": "20260930T000000Z-aaaaaaaaaaaa"}
          for k in ("A", "B", "C")]
    g1.append({**g1[0], "security_id": None, "security_name": "Cash", "is_cash_line": True, "position_type": "cash"})
    put_parquet(s, homes.canonical_shape(DAY, "holdings-20260930T000000Z-aaaaaaaaaaaa.parquet"), g1)
    put_parquet(s, eb.market_target_uri(DAY, "20260930T010000Z-bbbbbbbbbbbb"),
                [{"security_id": "A", "date": DAY, "px_close": 10.0, "gics_sector": "Energy"},
                 {"security_id": "B", "date": DAY, "px_close": 20.0, "gics_sector": None}])
    rd = [{"source": "fear_greed", "name": "stock_price_strength", "status": "fresh", "as_of": "2026-09-30", "location": "s3://x"},
          {"source": "keyword_sentiment", "name": "tariffs", "status": "stale", "as_of": "2026-09-20", "location": "s3://y"}]
    out = ic.build(DAY, s, ENTRIES, readings=rd)
    print(out[["input_kind", "subject", "status", "reason"]].to_string(index=False))

    def st(kind, subj):
        x = out[(out.input_kind == kind) & (out.subject == subj)]
        return x.iloc[0]["status"] if len(x) == 1 else None

    sc = out[(out.input_kind == "holdings") & (out.subject == "SCHY")]
    v.check(st("holdings", "TXUE") == "arrived" and len(sc) == 1 and sc.iloc[0]["status"] == "missing" and sc.iloc[0]["reason"],
            "holdings: TXUE arrived, SCHY missing with a reason")
    v.check([st("price", k) for k in "ABC"] == ["arrived", "arrived", "missing"]
            and [st("gics", k) for k in "ABC"] == ["arrived", "missing", "missing"],
            "price A,B arrived and C missing; gics A arrived, B and C missing")
    v.check(st("market_reading", "stock_price_strength") == "arrived" and st("market_reading", "tariffs") == "stale",
            "readings: fear_greed arrived, keyword_sentiment stale")
    v.check(len(out) == 10 and set(out["status"]) <= {"arrived", "missing", "stale"},
            "control: 10 rows, every status in the enum (the cash line has no price or gics row)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
