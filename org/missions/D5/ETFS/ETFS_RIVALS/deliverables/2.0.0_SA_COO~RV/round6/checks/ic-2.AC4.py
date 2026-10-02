"""RIV-ic-2 AC4 (RFW-D14; CRO GICS census section 1 and section 3 "Also"): the census reads the fund's OWN G1 sector
before it calls a GICS input missing. Source: docs/briefs/rivalfunds-gics-census-20261002.md (308f982bb8): the
component lists 763 of 763 GICS inputs missing because it checks only G4; 410 of them carry GICS in the fund's own
file. Today `gold_input_census.build` marks a gics row arrived only when the day's G4 row carries `gics_sector`
(`gold_input_census.py` :92-96), so an own-file sector with no G4 row reads 'missing, no G4 row ... the sector is
read from the fund's G1 report where present'.

Interface: `gold_input_census.build(day, sink, universe_entries, readings=None)`; status arrived | covered_by_fallback
| missing | stale; column `fallback` ("holding_implied" | "other_fund" | NULL), as ic-2.AC1-3 read them.

Offline, local sink (day 2026-09-30). The day's G1 holds TXUE (P, Q, R) and BASG (R, S); the day's G4 holds ONE row,
BASG's S (px_close, gics_sector Materials), so the G4 partition exists and P, Q, R have no G4 row:
  P: TXUE's file states gics_sector Health Care                      -> gics arrived (the fund's own file);
  Q: no gics_sector in any file                                      -> gics missing, fallback NULL (control);
  R: no gics_sector in TXUE's file; BASG's file states Industrials   -> gics covered_by_fallback, other_fund.
  - (a) TXUE's gics row for P reads arrived (not missing);
  - (b) control: TXUE's gics row for Q reads missing with a NULL fallback;
  - (c) TXUE's gics row for R reads covered_by_fallback with fallback other_fund -- ic-2.AC2's limb with no G4 row at
    all (AC2's X has a G4 row without a sector); the same rule, not a new one.
FAIL at base: (a) FAILs (P reads missing); (b) PASSes (the `fallback` column is absent at base and reads NULL);
(c) FAILs, as ic-2.AC2 does at base. ic-2.AC2 left the own-file case ungraded ("not prescribed"); this limb (a)
prescribes it as arrived and grades nothing AC2 grades."""
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

    s = sinks.get_sink(f"local:{c.tmpdir('rv_ic2d_')}")
    base = {"report_date": DAY, "is_cash_line": False, "position_type": "long", "asset_class": "Equity",
            "weight": 0.3, "quantity": 10.0, "market_value": 100.0, "dataset_revision": REV}
    tx = dict(base, fund_id="TXUE", fund_ticker="TXUE")
    bs = dict(base, fund_id="BASG", fund_ticker="BASG")
    g1 = [dict(tx, security_id="P", security_name="Pi", gics_sector="Health Care"),
          dict(tx, security_id="Q", security_name="Qoppa", gics_sector=None),
          dict(tx, security_id="R", security_name="Rho", gics_sector=None),
          dict(bs, security_id="R", security_name="Rho", gics_sector="Industrials"),
          dict(bs, security_id="S", security_name="Sigma", gics_sector="Materials")]
    put_parquet(s, homes.canonical_shape(DAY, f"holdings-{REV}.parquet"), g1)
    put_parquet(s, eb.market_target_uri(DAY, "20260930T010000Z-bbbbbbbbbbbb"),
                [{"security_id": "S", "date": DAY, "px_close": 10.0, "gics_sector": "Materials"}])
    out = ic.build(DAY, s, ENTRIES, readings=[])
    cols = [k for k in ("fund_id", "input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    print(out[cols].to_string(index=False))

    def row(fund, kind, subj):
        x = out[(out.fund_id == fund) & (out.input_kind == kind) & (out.subject == subj)]
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    p, q, r = row("TXUE", "gics", "P"), row("TXUE", "gics", "Q"), row("TXUE", "gics", "R")
    v.check(p.get("status") == "arrived",
            "(a) TXUE gics P (sector in its own file, no G4 row) reads arrived, not missing")
    v.check(q.get("status") == "missing" and null(q.get("fallback")),
            "(b) control: TXUE gics Q (no own sector, no G4 row, no other file) reads missing with a NULL fallback")
    v.check(r.get("status") == "covered_by_fallback" and r.get("fallback") == "other_fund",
            "(c) TXUE gics R (sector only in BASG's file, no G4 row) reads covered_by_fallback, fallback other_fund")


failures = c.guarded("AC4", run)
print("AC4 RESULT: PASS 0 failures" if failures == 0 else f"AC4 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
