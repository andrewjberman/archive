"""HVST-p-5 AC1 (issuer, read-only), after the collection and the upload.

PASS requires, against `~70/p5_before.json`: no pre-existing object moved or removed on any root; no new object under
barrons, ft or sa; EXACTLY ONE new object under the run-record table, whose JSON is the run named in `~70/p5_run.json`,
names 992_HK_Equity on exactly bbg and wsj, and carries a `reached_span` on every job whose status is successful; the
outbox holds no pending bbg/wsj row after the upload.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p5_common as p  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "p5_before.json"))
    after = p.snapshot()
    d = p.diff(before["snapshot"], after)
    for label, (moved, removed, new) in sorted(d.items()):
        print("%-13s moved %d removed %d new %d" % (label, len(moved), len(removed), len(new)))
        if moved or removed:
            failures.append("%s: %d moved / %d removed" % (label, len(moved), len(removed)))
        if label in p.NO_NEW and new:
            failures.append("%s: %d new object(s) on a no-write root" % (label, len(new)))
    rr_new = d["run_record"][2]
    if len(rr_new) != 1:
        failures.append("expected exactly 1 new persisted run record, found %d" % len(rr_new))
    else:
        rec = json.loads(store._default_client().get_object(Bucket=store.HARVEST_BUCKET, Key=rr_new[0])["Body"].read())
        run = p.c.load(os.path.join(p.WK, "p5_run.json"))
        print("persisted run record %s run_id %s (p5_run.json %s)" % (rr_new[0], rec.get("run_id"), run.get("run_id")))
        if rec.get("run_id") != run.get("run_id"):
            failures.append("persisted run_id != p5_run.json run_id")
        jobs = rec.get("jobs") or []
        pairs = sorted((j.get("publisher"), j.get("gold_security_key") or j.get("security_key")) for j in jobs)
        print("jobs: %s" % [(j.get("publisher"), j.get("status"), j.get("reached_span")) for j in jobs])
        if sorted(x[0] for x in pairs) != sorted(p.WRITE):
            failures.append("jobs %s are not exactly bbg and wsj" % pairs)
        for j in jobs:
            if j.get("status") in pg.SUCCESSFUL_RUN_STATUSES and not j.get("reached_span"):
                failures.append("successful job %s carries no reached_span" % j.get("publisher"))
    pend = p.outbox_pending()
    print("outbox pending after upload: %s" % pend)
    if any(r[0] in p.WRITE for rows in pend.values() for r in rows):
        failures.append("bbg/wsj rows still pending after the upload")
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
