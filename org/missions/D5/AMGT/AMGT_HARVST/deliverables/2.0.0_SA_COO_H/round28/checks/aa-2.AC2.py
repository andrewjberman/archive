"""HVST-aa-2 AC2 (issuer, read-only), after the daily rebuild: the run record is a SOURCE of coverage, and
`publishers_found_codes` is SERVED.

PASS requires:
- the persisted run records number >= 1, and Lenovo's coverage from the run records ALONE (`run_record_spans`, no listing
  hits) holds a span for every CONCLUDED bbg/wsj job of this run;
- exactly one new chatter_daily part since `~77/aa2_before.json`;
- the served snapshot's Lenovo rows carry each concluded publisher in `publishers_covered_codes` on the days its run-record
  span covers;
- the served snapshot carries `publishers_found_codes` (q-5) on its rows, non-null on at least one Lenovo row.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa2_common as p  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402


def as_date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "aa2_before.json"))
    run = p.c.load(os.path.join(p.WK, "aa2_run.json"))
    records = list(pg._iter_run_records())
    print("persisted run records read: %d" % len(records))
    lenovo = [s for s in p.c.securities() if s.get("security_key") == p.LENOVO]
    spans = pg.run_record_spans([r for r in records if r.get("run_id") == run.get("run_id")], lenovo).get(p.LENOVO, {})
    print("Lenovo spans from THIS run's record ALONE: %s" % spans)
    ok_pubs = [j["publisher"] for j in run.get("jobs", []) if j.get("status") in pg.SUCCESSFUL_RUN_STATUSES]
    print("concluded publishers this run: %s" % ok_pubs)
    for pub in ok_pubs:
        if not spans.get(pub):
            failures.append("concluded %s job yields no run-record span for Lenovo" % pub)
    new_parts = [k for k in p.snapshot()["chatter_daily"] if k not in before["snapshot"]["chatter_daily"]]
    print("new chatter_daily parts: %d" % len(new_parts))
    if len(new_parts) != 1:
        failures.append("expected exactly 1 new chatter_daily part, found %d" % len(new_parts))
    rows = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE) if r["security_key"] == p.LENOVO]
    for pub in ok_pubs:
        for lo, hi in [tuple(s) for s in (spans.get(pub) or [])]:
            days = [r for r in rows if as_date(lo) <= as_date(r["day"]) <= as_date(hi)]
            missing = [r for r in days if pub not in (r.get("publishers_covered_codes") or [])]
            print("  %s span %s..%s: %d served Lenovo day(s); missing the code on %d" % (pub, lo, hi, len(days), len(missing)))
            if not days or missing:
                failures.append("%s: served Lenovo days in its span lack the code (%d of %d)" % (pub, len(missing), len(days)))
    found = [r for r in rows if r.get("publishers_found_codes")]
    has_col = bool(rows) and "publishers_found_codes" in rows[0]
    print("publishers_found_codes served: column present %s; non-null on %d of %d Lenovo rows" % (has_col, len(found), len(rows)))
    if not has_col or not found:
        failures.append("publishers_found_codes is not served on the rebuilt snapshot")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
