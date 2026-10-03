"""RIV-rp-1 AC1 (row ETFS_RIVALS-Z-S18): the census's holding-implied price fallback reads the books in the SAME key space
as the census subject. Source (measured, served 2026-10-02): round 7 moved PFOE 81762P102 (ServiceNow) and 98138H101
(Workday) from covered_by_fallback/holding_implied to missing under their new subjects NOW_US_Equity / WDAY_US_Equity,
while the rankings price both holding_implied (identical r6 and r7 holding_contribution rows).

The defect (base 75ad1e4d2e, `gold_input_census.py:139-142`): `alias = identity_maps(g1w)` over the rankings' wide G1
window (cg-1), but `books = _books(g1)` over the 14-day slice, and `_books` recomputes its OWN alias from that slice. A
CUSIP that resolved to a Bloomberg id only in an older report is therefore the census subject `NOW_US_Equity` but the
books key `81762P102`, and `_implied_priced(books, f, latest, k)` misses.

Interface (prescribed): `gold_input_census.handler_entry({"date": <page day>, "sink", "readings": []})`; a price row the
rankings take holding-implied reads `covered_by_fallback` with `fallback` "holding_implied", under the subject the
rankings use. `gold_holding_contribution.handler_entry` unchanged.

Offline, local sink (page day 2026-10-02, as-of 2026-10-01), fund PFOE, no G4 rows:
  N: resolved to NOW_US_Equity in the 2026-09-10 report (security_id set, raw 81762P102); on 09-30 and 10-01 the
     same raw CUSIP with NO security_id, quantity 100, value 1000 -> 1010.
  R: raw 999999999 only, never resolved, the same two recent reports (the control: one key space throughout).
  - (0) fixture: the rankings price N under NOW_US_Equity with price_source holding_implied;
  - (a) the census's PFOE price row for NOW_US_Equity reads covered_by_fallback / holding_implied (base: missing);
  - (b) control: the census's PFOE price row for 999999999 reads covered_by_fallback / holding_implied (base too).
FAIL at base: (a) FAILS; (0) and (b) PASS."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, AS = "2026-10-02", "2026-10-01"
REV = "20261001T000000Z-aaaaaaaaaaaa"
OLD, RECENT = "2026-09-10", ("2026-09-30", "2026-10-01")
NOW, CUSIP_N, CUSIP_R = "NOW_US_Equity", "81762P102", "999999999"


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def read_out(s, res):
    import pandas as pd
    import pyarrow.parquet as pq
    uri = (res.get("outputs") or [None])[0]
    return pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else pd.DataFrame()


def null(x) -> bool:
    return x is None or x != x


def g1_rows(d, i, resolved):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "market_value": 1000.0 + 10.0 * i, "weight": 0.2, "security_bloomberg": None, "security_isin": None,
            "security_sedol": None, "provider_security_type": None, "dataset_revision": REV, "gics_sector": "Information Technology",
            "fund_id": "PFOE", "fund_ticker": "PFOE"}
    return [dict(base, security_id=(NOW if resolved else None), raw_identifier=CUSIP_N, security_cusip=CUSIP_N,
                 security_name="ServiceNow Inc"),
            dict(base, security_id=None, raw_identifier=CUSIP_R, security_cusip=CUSIP_R, security_name="Rho Corp")]


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_rp1_')}"
    s = sinks.get_sink(spec)
    put_parquet(s, homes.canonical_shape(OLD, f"holdings-{REV}.parquet"), g1_rows(OLD, 0, resolved=True))
    for i, d in enumerate(RECENT):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i, resolved=False))

    rk_res = hc.handler_entry({"date": PAGE, "sink": spec})
    rk = read_out(s, rk_res)
    sec = rk[(rk.get("axis") == "security") & (rk.get("fund_id") == "PFOE") & (rk.get("period") == "MTD")] if len(rk) else rk
    src = {str(r.bucket): (None if null(r.price_source) else str(r.price_source)) for r in sec.itertuples()}
    print("rankings:", rk_res.get("status"), "| PFOE MTD price_source by security:", src)
    v.check(src.get(NOW) == "holding_implied",
            "(0) fixture: the rankings price N under NOW_US_Equity, holding-implied")

    ic_res = ic.handler_entry({"date": PAGE, "sink": spec, "readings": []})
    out = read_out(s, ic_res)
    cols = [k for k in ("fund_id", "input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    print("census:", ic_res.get("status"))
    if len(out):
        print(out[(out.input_kind == "price") & (out.fund_id == "PFOE")][cols].to_string(index=False))

    def row(subj):
        x = out[(out.fund_id == "PFOE") & (out.input_kind == "price") & (out.subject == subj)] if len(out) else out
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    n, r = row(NOW), row(CUSIP_R)
    v.check(n.get("status") == "covered_by_fallback" and n.get("fallback") == "holding_implied",
            "(a) the census prices NOW_US_Equity as the rankings do: covered_by_fallback / holding_implied "
            f"(reads {n.get('status')}/{'NULL' if null(n.get('fallback')) else n.get('fallback')})")
    v.check(r.get("status") == "covered_by_fallback" and r.get("fallback") == "holding_implied",
            "(b) control: the never-resolved line 999999999 reads covered_by_fallback / holding_implied")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
