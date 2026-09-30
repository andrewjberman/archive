"""HVST-ad-2 AC1 (issuer, read-only): sa batch 1 stayed inside its pair.

PASS requires, against `~88/ad2_before.json`, `~88/ad2_plan.json` and `~88/ad2_runs.json` (the act's own list):
- no pre-existing object moved or removed;
- no new object on bbg, wsj, barrons, ft or the gold roots;
- the new run records are exactly the act's list;
- every job is sa, and they run in the plan's name order;
- no invocation followed a job whose status is a STOP status;
- 0 sign-ins (`signed_in` false on every job);
- sa listing pages that returned OK per name do not exceed the pre-run print;
- the outbox has no pending sa row after the upload.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ad2_common as c  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "ad2_before.json"))
    plan = c.load(os.path.join(c.WK, "ad2_plan.json"))
    runs = c.load(os.path.join(c.WK, "ad2_runs.json"))
    d = c.diff(before["snapshot"], c.snapshot())
    for label, (moved, removed, new) in sorted(d.items()):
        print("%-26s moved %d removed %d new %d" % (label, len(moved), len(removed), len(new)))
        if moved or removed:
            failures.append("%s: %d moved / %d removed" % (label, len(moved), len(removed)))
        if label in c.NO_NEW and new:
            failures.append("%s: %d new object(s) on a no-write root" % (label, len(new)))
    keys = runs.get("run_record_keys") or []
    if set(d["run_record"][2]) != set(keys):
        failures.append("new run records != the act's list")
    records = c.run_records(keys)
    order = list(plan)
    jobs = [j for rec in sorted(records, key=lambda r: r.get("started_at") or "") for j in rec.get("jobs") or []]
    print("jobs: %d over %d run records" % (len(jobs), len(records)))
    stopped = False
    last_idx = -1
    for j in jobs:
        if j.get("publisher") != "sa":
            failures.append("a non-sa job: %s" % j.get("publisher"))
        if stopped:
            failures.append("a job ran after a STOP status (%s)" % j.get("security_key"))
        if j.get("signed_in"):
            failures.append("a sign-in on %s" % j.get("security_key"))
        idx = order.index(j.get("security_key")) if j.get("security_key") in order else -2
        if idx <= last_idx:
            failures.append("job out of plan order: %s" % j.get("security_key"))
        last_idx = idx
        if j.get("status") in c.STOP_STATUSES:
            stopped = True
        print("  %-28s %-34s signed_in %s" % (j.get("security_key"), j.get("status"), j.get("signed_in")))
    pages = {}
    for rec in records:
        for a in rec.get("request_attempts") or []:
            if a.get("request_kind") == "listing" and a.get("class") == "ok":
                pages[a.get("security_key")] = pages.get(a.get("security_key"), 0) + 1
    over = [(k, n) for k, n in pages.items() if n > (plan.get(k) or {}).get("pages", 0)]
    print("listing pages OK per name: %s; over the print: %d" % (pages, len(over)))
    if over:
        failures.append("pages over the pre-run print: %s" % over)
    left = [r for rows in c.outbox_pending().values() for r in rows if r[0] == "sa"]
    if left:
        failures.append("sa rows pending after the upload: %s" % left)
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
