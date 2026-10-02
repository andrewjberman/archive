"""RIV-cs-1 AC1 (RFW-D02, "one fact, one number"): the census's holdings line agrees with the page header's
"<n> of <m> funds current". A fund whose newest report sits inside the header's freshness allowance reads COVERED in
the census, naming the fallback; a report outside the allowance stays `missing`.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base):
the header read "13 of 13 funds current" while the census read "9 of 13 arrived, 4 missing". The two rules differ:
  - header (render.py:508-510, `ctx["n_updated"]`): `guardrails.report_date_freshness` (guardrails.py:95-120) passes a
    fund whose newest report trails the expected date (the page day's previous trading day) by at most
    FRESHNESS_ALLOWANCE[source] trading days -- bloomberg 1, home_producer 1, issuer 0 -- where the source is
    `publish_page.fund_source` (home_producer for a home fund, else the G1 `source_used` of its newest report);
  - census (gold_input_census.py:109-113): `arrived` only for a G1 report dated EXACTLY the as-of day, else `missing`.
INTERFACE (prescribed; ic-2's states unchanged): `gold_input_census.handler_entry({"date": <page day>, "sink",
"readings": []})`. A holdings row whose fund has no report on the as-of day but whose newest report passes the header's
rule (same allowance table, same source rule) reads `covered_by_fallback` with `fallback` =
"prior_report_within_allowance" and `as_of` = that report's date. `arrived` keeps its meaning (the as-of day's
report arrived; a covered input did NOT arrive, as ic-2's render counts it); `missing` (NULL fallback) only outside
the allowance.

Offline, local sink (page day 2026-10-02, as-of 2026-10-01, the real 13-fund universe). G1 reports:
  TXUE  bloomberg      09-30 and 10-01   lag 0 -> header PASS; census arrived (control);
  BIDD  bloomberg      09-30             lag 1, allowance 1 -> PASS; census covered;
  CGIC  bloomberg      09-29             lag 2 -> FAIL; census missing (control);
  IDVZ  home_producer  09-30             lag 1, allowance 1 -> PASS; census covered;
  WCMG  issuer_first fund, newest report source_used bloomberg, 09-30 -> PASS (the header reads the source, not the
        policy); census covered;
  BASG  issuer         09-30             lag 1, allowance 0 -> FAIL; census missing (control);
  INEQ, SCHY, PFOE, GQGU, TSEL, ETFT, PCLG: no report -> FAIL; census missing (control).
  - BIDD, IDVZ and WCMG read covered_by_fallback, fallback prior_report_within_allowance, as_of 2026-09-30;
  - agreement: for all 13 funds, census arrived-or-covered <=> the header's own freshness check (guardrails
    `report_date_freshness` with `publish_page.fund_source`) PASSes;
  - control: TXUE arrived with a NULL fallback; CGIC, BASG and the seven funds with no report read missing with a NULL
    fallback; every holdings status is in {arrived, covered_by_fallback, missing, stale}.
FAIL at base: the first two limbs (BIDD, IDVZ, WCMG read missing); the control PASSes."""

import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, AS_OF = "2026-10-02", "2026-10-01"
REV = "20261001T230000Z-cccccccccccc"
REPORTS = {  # fund: (source_used of its reports, report dates)
    "TXUE": ("bloomberg", ("2026-09-30", "2026-10-01")),
    "BIDD": ("bloomberg", ("2026-09-30",)),
    "CGIC": ("bloomberg", ("2026-09-29",)),
    "IDVZ": ("home_producer", ("2026-09-30",)),
    "WCMG": ("bloomberg", ("2026-09-30",)),
    "BASG": ("issuer", ("2026-09-30",)),
}
COVERED = ("BIDD", "IDVZ", "WCMG")
FB = "prior_report_within_allowance"
STATES = {"arrived", "covered_by_fallback", "missing", "stale"}


def g1_rows(fund, src, d):
    base = {"fund_id": fund, "fund_ticker": fund, "report_date": d, "source_used": src, "dataset_revision": REV,
            "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "raw_identifier_kind": "cusip",
            "resolution_status": "RESOLVED", "gics_sector": "Energy"}
    return [dict(base, security_id=f"{fund}A_US_Equity", raw_identifier=f"{fund}A", security_name=f"{fund} Alpha",
                 quantity=10.0, market_value=100.0, weight=0.5),
            dict(base, security_id=None, raw_identifier="USD Curncy", security_name="Cash", quantity=5.0,
                 market_value=5.0, weight=0.01, is_cash_line=True, position_type="cash", asset_class="Cash",
                 resolution_status="UNRESOLVED", gics_sector=None)]


def plant(s):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rivalfunds import homes

    by_date: dict = {}
    for fund, (src, dates) in REPORTS.items():
        for d in dates:
            by_date.setdefault(d, []).extend(g1_rows(fund, src, d))
    for d, rows in by_date.items():
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
        s.put(homes.canonical_shape(d, f"holdings-{REV}.parquet"), buf.getvalue())
    return by_date


def null(x) -> bool:
    return x is None or x != x


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    from rivalfunds import gold_input_census as ic
    from rivalfunds import guardrails, publish_page, sinks, universe

    spec = f"local:{c.tmpdir('rv_cs1_')}"
    s = sinks.get_sink(spec)
    by_date = plant(s)
    r = ic.handler_entry({"date": PAGE, "sink": spec, "readings": []})
    if r.get("status") != "OK" or not r.get("outputs"):
        v.check(False, f"the census handler wrote its table ({r})")
        return
    out = pd.read_parquet(io.BytesIO(s.get(r["outputs"][0])))
    h = out[out["input_kind"] == "holdings"].set_index("subject")
    print(h[["status", "fallback", "as_of", "reason"]].to_string())

    def row(f):
        return h.loc[f].to_dict() if f in h.index else {}

    cov = {f: (row(f).get("status"), row(f).get("fallback"), str(row(f).get("as_of"))[:10]) for f in COVERED}
    v.check(all(x == ("covered_by_fallback", FB, "2026-09-30") for x in cov.values()),
            f"BIDD, IDVZ, WCMG (inside the allowance) read covered_by_fallback, fallback {FB}, as_of 2026-09-30 "
            f"({cov})")
    header, census = {}, {}
    for e in universe.entries():
        f = str(e["fund_id"])
        rows = [x for d in sorted(by_date) for x in by_date[d] if x["fund_id"] == f]
        dates = sorted({x["report_date"] for x in rows})
        latest = pd.DataFrame([x for x in rows if x["report_date"] == dates[-1]]) if dates else pd.DataFrame()
        res = guardrails.report_date_freshness(PAGE, dates, guardrails.load_config(),
                                               publish_page.fund_source(e, latest))
        header[f] = res["status"] == "PASS"
        census[f] = row(f).get("status") in ("arrived", "covered_by_fallback")
    off = {f: (header[f], census[f]) for f in header if header[f] != census[f]}
    print(f"header current {sum(header.values())} of {len(header)}; census covered {sum(census.values())} of "
          f"{len(census)}; disagree (header, census): {off}")
    v.check(not off and len(header) == 13,
            "agreement: census arrived-or-covered <=> the header's freshness PASS, for 13 of 13 funds")
    miss = [f for f in header if f not in REPORTS or f in ("CGIC", "BASG")]
    ok_miss = all(row(f).get("status") == "missing" and null(row(f).get("fallback")) for f in miss)
    t = row("TXUE")
    v.check(t.get("status") == "arrived" and null(t.get("fallback")) and ok_miss and len(miss) == 9
            and set(h["status"]) <= STATES,
            "control: TXUE arrived (NULL fallback); CGIC, BASG and the 7 funds with no report missing (NULL fallback)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
