"""RIV-ic-2 AC2 (RFW-D14): a GICS input the fund's own file lacks but ANOTHER fund's file carries (CRO~RV CALL 9, the
cross-fund fallback buying_trend already uses) reads `covered_by_fallback` with fallback `other_fund`; a GICS input
no file carries reads `missing`. Today both read 'missing'.

Interface (prescribed): `gold_input_census.build(day, sink, universe_entries, readings=None)`; status arrived |
covered_by_fallback | missing | stale; column `fallback` = "other_fund" for a GICS sector taken from another fund's
file, NULL when nothing covers the input.

Offline, local sink (day 2026-09-30): the day's G1 holds TXUE (X and Y, no gics_sector on either) and BASG (X with
gics_sector Energy); the day's G4 holds X and Y with px_close and NO gics_sector (the served state, RFW-D04).
  - TXUE's gics row for X reads covered_by_fallback with fallback other_fund;
  - control: TXUE's gics row for Y (no file and no G4 row carries it) reads missing with a NULL fallback.
BASG's own gics row for X (its own file carries the sector, G4 does not) is NOT graded: that case is not
prescribed."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-30"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"},
           {"group_id": "PFOE", "fund_id": "BASG", "role": "rival"}]
REV = "20260930T000000Z-aaaaaaaaaaaa"


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

    s = sinks.get_sink(f"local:{c.tmpdir('rv_ic2b_')}")
    base = {"report_date": DAY, "is_cash_line": False, "position_type": "long", "asset_class": "Equity",
            "weight": 0.5, "quantity": 10.0, "market_value": 100.0, "dataset_revision": REV}
    g1 = [dict(base, fund_id="TXUE", fund_ticker="TXUE", security_id="X", security_name="Xeno", gics_sector=None),
          dict(base, fund_id="TXUE", fund_ticker="TXUE", security_id="Y", security_name="Ypsilon", gics_sector=None),
          dict(base, fund_id="BASG", fund_ticker="BASG", security_id="X", security_name="Xeno", gics_sector="Energy")]
    put_parquet(s, homes.canonical_shape(DAY, f"holdings-{REV}.parquet"), g1)
    put_parquet(s, eb.market_target_uri(DAY, "20260930T010000Z-bbbbbbbbbbbb"),
                [{"security_id": k, "date": DAY, "px_close": 10.0, "gics_sector": None} for k in ("X", "Y")])
    out = ic.build(DAY, s, ENTRIES, readings=[])
    cols = [k for k in ("fund_id", "input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    print(out[cols].to_string(index=False))

    def row(fund, kind, subj):
        x = out[(out.fund_id == fund) & (out.input_kind == kind) & (out.subject == subj)]
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    x, y = row("TXUE", "gics", "X"), row("TXUE", "gics", "Y")
    v.check(x.get("status") == "covered_by_fallback" and x.get("fallback") == "other_fund",
            "TXUE gics X (sector only in BASG's file) reads covered_by_fallback, fallback other_fund")
    v.check(y.get("status") == "missing" and null(y.get("fallback")),
            "control: TXUE gics Y (no file, no G4 row carries it) reads missing with a NULL fallback")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
