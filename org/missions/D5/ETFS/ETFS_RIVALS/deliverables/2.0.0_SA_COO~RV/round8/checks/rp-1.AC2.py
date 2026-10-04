"""RIV-rp-1 AC2 (the round-8 register measure, outside any acceptance text): a census price row that reads `missing` does
not claim the rankings price it. Source (measured, served 2026-10-02, rv-publish-1002r7): 44 price rows read `missing`
with the reason "no G4 row for 2026-10-01; the rankings price it from the fund's own reported valuation". That is the
fixed `why` text `gold_input_census.py:183` appends to EVERY price miss, so it contradicts the status for every line the
rankings leave unpriced.

Interface (prescribed): `gold_input_census.handler_entry({"date": <page day>, "sink", "readings": []})`. A `missing` price
row's reason states why no price exists (the cell's words). It never claims a price the rankings take. A
`covered_by_fallback` / `holding_implied` row keeps its reason (it names the holding-implied price).

Offline, local sink (page day 2026-10-02, as-of 2026-10-01), fund PFOE, no G4 rows:
  M: raw 888888888 only in the 10-01 report (no prior report to imply a price from) -> the rankings leave it unpriced;
  R: raw 999999999 in the 09-30 and 10-01 reports -> the rankings price it holding-implied.
  - (0) fixture: the rankings price R holding_implied and do not price M;
  - (a) M's census price row reads missing, and its reason does not say the rankings price it;
  - (b) control: R reads covered_by_fallback / holding_implied, and its reason names the holding-implied price.
FAIL at base: (a) FAILS (the reason says "the rankings price it from the fund's own reported valuation"); (0) and (b) PASS."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-02"
REV = "20261001T000000Z-aaaaaaaaaaaa"
RECENT = ("2026-09-30", "2026-10-01")
M, R = "888888888", "999999999"
CLAIM = "the rankings price it"


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


def g1_rows(d, i):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "market_value": 1000.0 + 10.0 * i, "weight": 0.2, "security_bloomberg": None, "security_isin": None,
            "security_sedol": None, "provider_security_type": None, "dataset_revision": REV,
            "gics_sector": "Information Technology", "fund_id": "PFOE", "fund_ticker": "PFOE", "security_id": None}
    rows = [dict(base, raw_identifier=R, security_cusip=R, security_name="Rho Corp")]
    if d == RECENT[-1]:
        rows.append(dict(base, raw_identifier=M, security_cusip=M, security_name="Mu Corp"))
    return rows


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_rp1b_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(RECENT):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))

    rk = read_out(s, hc.handler_entry({"date": PAGE, "sink": spec}))
    sec = rk[(rk.get("axis") == "security") & (rk.get("fund_id") == "PFOE") & (rk.get("period") == "MTD")] if len(rk) else rk
    src = {str(r.bucket): (None if null(r.price_source) else str(r.price_source)) for r in sec.itertuples()}
    print("rankings PFOE MTD price_source by security:", src)
    v.check(src.get(R) == "holding_implied" and src.get(M) != "holding_implied",
            "(0) fixture: the rankings price R holding-implied and leave M unpriced")

    out = read_out(s, ic.handler_entry({"date": PAGE, "sink": spec, "readings": []}))
    cols = [k for k in ("fund_id", "input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    if len(out):
        print(out[(out.input_kind == "price") & (out.fund_id == "PFOE")][cols].to_string(index=False))

    def row(subj):
        x = out[(out.fund_id == "PFOE") & (out.input_kind == "price") & (out.subject == subj)] if len(out) else out
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    m, r = row(M), row(R)
    m_reason, r_reason = str(m.get("reason") or ""), str(r.get("reason") or "")
    v.check(m.get("status") == "missing" and m_reason and CLAIM not in m_reason.lower(),
            f"(a) M reads missing and its reason does not claim the rankings price it (reason: {m_reason!r})")
    v.check(r.get("status") == "covered_by_fallback" and r.get("fallback") == "holding_implied"
            and "holding-implied" in r_reason.lower(),
            "(b) control: R reads covered_by_fallback / holding_implied and its reason names the holding-implied price")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
