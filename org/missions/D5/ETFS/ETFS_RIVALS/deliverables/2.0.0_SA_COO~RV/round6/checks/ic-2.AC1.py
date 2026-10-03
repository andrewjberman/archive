"""RIV-ic-2 AC1 (RFW-D14, RFW-U11 data half): the census has a THIRD state. A price input with no G4 row that the
rankings price from the fund's own valuation (the holding-implied fallback, CRO~RV CALL 1) reads
`covered_by_fallback`, naming the fallback -- not `missing`. Today all 765 such securities read 'missing, no G4 row
... the rankings price it from the fund's own reported valuation'.

Interface (prescribed): `gold_input_census.build(day, sink, universe_entries, readings=None)` -> a frame whose
`status` is one of arrived | covered_by_fallback | missing | stale, with a new column `fallback`: "holding_implied"
(a price) or "other_fund" (a GICS sector from another fund's file, CALL 9), NULL otherwise; `missing` only when no
fallback covers the input. The frame's `status` column is what the page counts per state.

Offline, local sink (day 2026-09-30, its previous trading day 2026-09-29): TXUE reports on BOTH days, holding
  A: a G4 row on 2026-09-30 with px_close                             -> price arrived;
  B: no G4 row; quantity 100 on both reports, market value 1000 -> 1050 -> price covered_by_fallback, holding_implied;
  D: no G4 row; no quantity and no market value on either report      -> price missing, fallback NULL (control);
  plus a cash line (no price row).
  - B's price row reads covered_by_fallback with fallback holding_implied;
  - control: D's price row reads missing with a NULL fallback, and A's reads arrived;
  - every status is in {arrived, covered_by_fallback, missing, stale}."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY, PREV = "2026-09-30", "2026-09-29"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
REV = "20260930T000000Z-aaaaaaaaaaaa"
STATES = {"arrived", "covered_by_fallback", "missing", "stale"}


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows(date, b_mv):
    base = {"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": date, "is_cash_line": False,
            "position_type": "long", "asset_class": "Equity", "weight": 0.3, "dataset_revision": REV}
    return [dict(base, security_id="A", security_name="Alpha", quantity=10.0, market_value=100.0),
            dict(base, security_id="B", security_name="Beta", quantity=100.0, market_value=b_mv),
            dict(base, security_id="D", security_name="Delta", quantity=None, market_value=None),
            dict(base, security_id=None, security_name="Cash", quantity=5.0, market_value=5.0, is_cash_line=True,
                 position_type="cash", asset_class="Cash")]


def null(x) -> bool:
    return x is None or x != x


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    s = sinks.get_sink(f"local:{c.tmpdir('rv_ic2a_')}")
    for d, mv in ((PREV, 1000.0), (DAY, 1050.0)):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, mv))
    put_parquet(s, eb.market_target_uri(DAY, "20260930T010000Z-bbbbbbbbbbbb"),
                [{"security_id": "A", "date": DAY, "px_close": 10.0, "gics_sector": "Energy"}])
    out = ic.build(DAY, s, ENTRIES, readings=[])
    cols = [k for k in ("input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    print(out[cols].to_string(index=False))

    def row(kind, subj):
        x = out[(out.input_kind == kind) & (out.subject == subj)]
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    b, d, a = row("price", "B"), row("price", "D"), row("price", "A")
    v.check(b.get("status") == "covered_by_fallback" and b.get("fallback") == "holding_implied",
            "B (no G4 row, valued on both reports) reads covered_by_fallback, fallback holding_implied")
    v.check(d.get("status") == "missing" and null(d.get("fallback")) and a.get("status") == "arrived",
            "control: D (no valuation) reads missing with a NULL fallback; A (G4 px_close) reads arrived")
    v.check(set(out["status"]) <= STATES, "every status is in {arrived, covered_by_fallback, missing, stale}")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
