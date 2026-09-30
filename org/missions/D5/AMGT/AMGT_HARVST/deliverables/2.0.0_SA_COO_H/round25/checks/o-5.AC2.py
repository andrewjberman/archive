"""HVST-o-5 AC2 (issuer check, read-only): the repeat, run the same day, fetches nothing.

PASS requires: a second run record exists, started the same UTC day as the first, with counts.fetched == 0 and
keys_fetched empty; since the after-run-1 snapshot no object moved or vanished, and no new object landed in any
bronze or silver ARTICLE table (a re-fetched listing page may be new: printed, not failed); no new sa object.
"""
import os
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
        print("run 2 %s: counts=%s" % (r2.get("run_id"), r2.get("counts")))
        if str(r1.get("started_at"))[:10] != str(r2.get("started_at"))[:10]:
            failures.append("run 2 started %s, not the same UTC day as run 1 (%s)" % (r2.get("started_at"), r1.get("started_at")))
        fetched = (r2.get("counts") or {}).get("fetched")
        if fetched != 0 or (r2.get("keys_fetched") or []):
            failures.append("run 2 fetched %r (keys %d), not 0" % (fetched, len(r2.get("keys_fetched") or [])))
        print("run 2 skipped as held: %s (run 1 fetched %s)" % ((r2.get("counts") or {}).get("skipped_as_held"), (r1.get("counts") or {}).get("fetched")))

    after1 = c.load(os.path.join(c.WK, "o5_after_run1.json"))
    after2 = c.snapshot()
    for publisher, (moved, removed, new) in sorted(c.diff(after1, after2).items()):
        by_table = {}
        for k in new:
            by_table[c.table_of(k)] = by_table.get(c.table_of(k), 0) + 1
        print("%-8s since run 1: moved=%d removed=%d new=%d  new by tier/table=%s" % (publisher, len(moved), len(removed), len(new), by_table))
        if moved or removed:
            failures.append("%s: %d object(s) moved, %d removed since run 1" % (publisher, len(moved), len(removed)))
        article_new = [k for k in new if "article" in c.table_of(k)]
        if article_new:
            failures.append("%s: %d new article object(s) on the repeat (first: %s)" % (publisher, len(article_new), article_new[0]))
        if publisher in c.NO_NEW and new:
            failures.append("%s: %d new object(s) -- this root must gain no object (sa waits on the renewal; barrons is Branch B)" % (publisher, len(new)))

    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
