"""HVST-ab-3 AC1 (issuer, read-only), after the collections and the upload (phase A).

PASS requires, against `~83/ab3_before.json` and `~83/ab3_plan.json`:
- no pre-existing object moved or removed on any root; no new object under the gold roots (no gold write in this cell);
- the new persisted run records are exactly those named in `~83/ab3_runs.json` (the act's own list, one per invocation);
- the jobs across them, (security_key, publisher) with a probe retry superseding, equal the owed set: 32, or 23 when
  `ab3_runs.json` records a PERSISTING sa 402 (then only the probe's sa job exists);
- every job carries `token_source`; listing requests that returned OK per pair do not exceed the pre-run print;
- the outbox holds no pending row for the five publishers after the upload.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab3_common as c  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "ab3_before.json"))
    plan = c.load(os.path.join(c.WK, "ab3_plan.json"))
    runs = c.load(os.path.join(c.WK, "ab3_runs.json"))
    d = c.diff(before["snapshot"], c.snapshot())
    for label, (moved, removed, new) in sorted(d.items()):
        print("%-26s moved %d removed %d new %d" % (label, len(moved), len(removed), len(new)))
        if moved or removed:
            failures.append("%s: %d moved / %d removed" % (label, len(moved), len(removed)))
        if label in c.NO_NEW and new:
            failures.append("%s: %d new object(s) on a no-write root" % (label, len(new)))
    rr_new = set(d["run_record"][2])
    named = set(runs.get("run_record_keys") or [])
    print("new run records %d; named by the act %d" % (len(rr_new), len(named)))
    if rr_new != named:
        failures.append("new run records != the act's list (+%d / -%d)" % (len(rr_new - named), len(named - rr_new)))
    records = c.run_records(sorted(rr_new))
    jobs = c.jobs_by_pair(records)
    sa_in = not runs.get("sa_402_persisted", False)
    want = c.expected_jobs(sa_in)
    print("jobs: %d (owed %d; sa in batch %s)" % (len(jobs), len(want), sa_in))
    if set(jobs) != want:
        failures.append("jobs != owed (+%s / -%s)" % (sorted(set(jobs) - want)[:3], sorted(want - set(jobs))[:3]))
    no_src = sorted(k for k, j in jobs.items() if not j.get("token_source"))
    if no_src:
        failures.append("%d job(s) carry no token_source (first %s)" % (len(no_src), no_src[0]))
    pages = c.listing_pages(records)
    over = []
    for (key, pub), n in sorted(pages.items()):
        cap = (plan.get("%s|%s" % (key, pub)) or {}).get("pages")
        if cap is None or n > cap:
            over.append((key, pub, n, cap))
    print("listing pages OK per pair: %d pairs, max %d; over the pre-run print: %d" % (len(pages), max(pages.values() or [0]), len(over)))
    if over:
        failures.append("%d pair(s) spent more listing pages than printed (first %s)" % (len(over), over[0]))
    pend = c.outbox_pending()
    left = [r for rows in pend.values() for r in rows if r[0] in c.PUBLISHERS]
    print("outbox pending after upload: %s" % pend)
    if left:
        failures.append("rows still pending after the upload: %s" % left)
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
