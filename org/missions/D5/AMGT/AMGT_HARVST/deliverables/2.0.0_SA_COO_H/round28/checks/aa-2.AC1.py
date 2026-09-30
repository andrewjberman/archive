"""HVST-aa-2 AC1 (issuer, read-only), after the collection and the upload -- the CACHED-PATH arm (CTO ruling @cb107ff848).

PASS requires, against `~77/aa2_before.json`:
- no pre-existing object moved or removed on any root; no new object under barrons, ft or sa;
- EXACTLY ONE new persisted run record, the run named in `~77/aa2_run.json`, with jobs on exactly bbg and wsj;
- every CONCLUDED job carries a `reached_span`; the wsj span is marked `from_cache` (aa-1's cached reach);
- `bbg:NM5NLQ6K50XZ01` appears in the record's `keys_held` and NOT in `keys_fetched` (aa-1's hold);
- the outbox holds no pending bbg/wsj row after the upload.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa2_common as p  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HELD_KEY = "bbg:NM5NLQ6K50XZ01"


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "aa2_before.json"))
    d = p.diff(before["snapshot"], p.snapshot())
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
        run = p.c.load(os.path.join(p.WK, "aa2_run.json"))
        print("persisted run record %s run_id %s (aa2_run.json %s)" % (rr_new[0], rec.get("run_id"), run.get("run_id")))
        if rec.get("run_id") != run.get("run_id"):
            failures.append("persisted run_id != aa2_run.json run_id")
        jobs = rec.get("jobs") or []
        print("jobs: %s" % [(j.get("publisher"), j.get("status"), j.get("reached_span")) for j in jobs])
        if sorted(j.get("publisher") for j in jobs) != sorted(p.WRITE):
            failures.append("jobs are not exactly bbg and wsj")
        for j in jobs:
            if j.get("status") in pg.SUCCESSFUL_RUN_STATUSES and not j.get("reached_span"):
                failures.append("concluded job %s carries no reached_span" % j.get("publisher"))
            if j.get("publisher") == "wsj" and j.get("status") in pg.SUCCESSFUL_RUN_STATUSES:
                if not (j.get("reached_span") or {}).get("from_cache"):
                    failures.append("wsj's span is not marked from_cache (the cached-path arm)")
        held = [h.get("key") if isinstance(h, dict) else h for h in (rec.get("keys_held") or [])]
        fetched = rec.get("keys_fetched") or []
        print("keys_held %s; %s fetched: %s" % (held, HELD_KEY, HELD_KEY in fetched))
        if HELD_KEY not in held or HELD_KEY in fetched:
            failures.append("%s is not held (held %s, fetched %s)" % (HELD_KEY, HELD_KEY in held, HELD_KEY in fetched))
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
