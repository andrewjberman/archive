"""HVST-o-5 AC2 (issuer check, read-only), AMENDMENT 2: the same-day repeat re-fetches NOTHING HELD (FWD-3's words).

AMENDMENT 2 replaces `counts.fetched == 0`: a listing can surface a genuinely new item between two runs, and an item
fetched but never stored is not held. PASS requires: a second run record, the same UTC day as the first, over the
same three jobs; it skipped >= 1 key as held; and every key it fetched is either absent from run 1's fetched keys
(new to the listing) or absent from the collector's local store after run 1 (fetched, never stored) -- never a key
run 1 fetched AND stored. Each fetched key is printed with its reason.
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o5_common as c  # noqa: E402


def main():
    failures = []
    ids = c.load(os.path.join(c.WK, "o5_run_ids.json"))
    runs = ids.get("runs") or []
    print("run ids file: %d run(s) listed" % len(runs))
    if len(runs) < 2:
        failures.append("no second run listed")
    else:
        r1, r2 = c.load(runs[0]["path"]), c.load(runs[1]["path"])
        print("run 1 %s counts=%s" % (r1.get("run_id"), r1.get("counts")))
        print("run 2 %s counts=%s" % (r2.get("run_id"), r2.get("counts")))
        if str(r1.get("started_at"))[:10] != str(r2.get("started_at"))[:10]:
            failures.append("run 2 is not the same UTC day as run 1")
        jobs2 = sorted(j.get("publisher") for j in r2.get("jobs") or [])
        if jobs2 != sorted(c.JOB_PUBLISHERS):
            failures.append("run 2 jobs %s != %s" % (jobs2, sorted(c.JOB_PUBLISHERS)))
        skipped = (r2.get("counts") or {}).get("skipped_as_held") or 0
        if skipped < 1:
            failures.append("run 2 skipped nothing as held")
        db = sqlite3.connect(os.path.join(c.RUNTIME, "progress.sqlite3"))
        stored = {r[0] for r in db.execute("SELECT article_key FROM harvest_raw_outbox")}
        run1 = set(r1.get("keys_fetched") or [])
        for k in r2.get("keys_fetched") or []:
            if k not in run1:
                why = "NEW to the listing (not fetched by run 1)"
            elif k not in stored:
                why = "fetched by run 1 but NEVER STORED (not held)"
            else:
                why = "RE-FETCH OF A HELD KEY"
                failures.append("run 2 re-fetched held key %s" % k)
            print("  run 2 fetched %s -> %s" % (k, why))
        print("run 2 skipped as held: %d" % skipped)

    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
