"""HVST-p-5 AC2 (issuer, read-only), after the coverage rebuild: the run-record path is the SOURCE of a coverage mark.

PASS requires: the persisted run records (`publication_gold._iter_run_records`) number >= 1; Lenovo's coverage computed
from the run records ALONE (`run_record_spans`, no listing hits) holds a span for every SUCCESSFUL bbg/wsj job of the run;
exactly one new chatter_daily part since `~70/p5_before.json`, and the served snapshot's Lenovo rows carry each of those
publishers in `publishers_covered_codes` on the days the run-record span covers. The all-names guard is not graded here.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p5_common as p  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "p5_before.json"))
    records = list(pg._iter_run_records())
    print("persisted run records read: %d" % len(records))
    if not records:
        failures.append("no persisted run record")
    lenovo = [s for s in p.c.securities() if s.get("security_key") == p.LENOVO]
    spans = pg.run_record_spans(records, lenovo).get(p.LENOVO, {})
    print("Lenovo spans from run records ALONE: %s" % spans)
    run = p.c.load(os.path.join(p.WK, "p5_run.json"))
    ok_pubs = [j["publisher"] for j in run.get("jobs", []) if j.get("status") in pg.SUCCESSFUL_RUN_STATUSES]
    for pub in ok_pubs:
        if not spans.get(pub):
            failures.append("successful %s job yields no run-record span for Lenovo" % pub)
    new_parts = [k for k in p.snapshot()["chatter_daily"] if k not in before["snapshot"]["chatter_daily"]]
    print("new chatter_daily parts: %d" % len(new_parts))
    if len(new_parts) != 1:
        failures.append("expected exactly 1 new chatter_daily part, found %d" % len(new_parts))
    rows = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE) if r["security_key"] == p.LENOVO]
    for pub in ok_pubs:
        span = spans.get(pub)
        if not span:
            continue
        spans_list = span if isinstance(span, list) else [span]
        days = [r for r in rows for (lo, hi) in [tuple(s) for s in spans_list]
                if lo <= (r["day"] if isinstance(r["day"], datetime.date) else datetime.date.fromisoformat(str(r["day"]))) <= hi]
        missing = [r for r in days if pub not in (r.get("publishers_covered_codes") or [])]
        print("  %s: run-record span %s covers %d served Lenovo day(s); missing the code on %d" % (pub, span, len(days), len(missing)))
        if not days or missing:
            failures.append("%s: served Lenovo days in its run-record span lack the code (%d of %d)" % (pub, len(missing), len(days)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
