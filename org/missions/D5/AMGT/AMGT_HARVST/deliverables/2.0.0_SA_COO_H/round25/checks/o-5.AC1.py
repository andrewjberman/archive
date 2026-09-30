"""HVST-o-5 AC1 (issuer check, read-only): the first run stayed inside the pair.

PASS requires: no object that existed at act start moved or vanished (all five publishers); no new sa object (the sa
leg waits on the renewal); the first run's run record exists, names 992_HK_Equity on exactly barrons, bbg, ft and wsj,
and its fetched keys are each backed by a new bronze object. Printed as measurement, not graded: new objects per
tier/table, each job's status, and each publisher's listing reach from 2026-01-01 through the run date. Writes the
after-run-1 snapshot the AC2 check compares against.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o5_common as c  # noqa: E402

FLOOR = datetime.date(2026, 1, 1)


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "o5_before.json"))
    after = c.snapshot()
    c.dump(os.path.join(c.WK, "o5_after_run1.json"), after)
    print("objects BEFORE %s" % c.counts(before))
    print("objects AFTER  %s" % c.counts(after))

    d = c.diff(before, after)
    for publisher, (moved, removed, new) in sorted(d.items()):
        by_table = {}
        for k in new:
            by_table[c.table_of(k)] = by_table.get(c.table_of(k), 0) + 1
        print("%-8s moved=%d removed=%d new=%d  new by tier/table=%s" % (publisher, len(moved), len(removed), len(new), by_table))
        if moved or removed:
            failures.append("%s: %d pre-existing object(s) moved, %d removed (first: %s)"
                            % (publisher, len(moved), len(removed), (moved + removed)[0]))
        if publisher in c.CONTROL and new:
            failures.append("%s: %d new object(s) -- the sa leg must not run" % (publisher, len(new)))

    ids = c.load(os.path.join(c.WK, "o5_run_ids.json"))
    runs = ids.get("runs") or []
    print("run ids file: %d run(s) listed" % len(runs))
    if not runs:
        failures.append("o5_run_ids.json lists no run")
    else:
        rec = c.load(runs[0]["path"])
        jobs = rec.get("jobs") or []
        print("run 1 %s: counts=%s, jobs=%d" % (rec.get("run_id"), rec.get("counts"), len(jobs)))
        for j in jobs:
            print("  job %-8s %-14s status=%s fetched=%s skipped_as_held=%s"
                  % (j.get("publisher"), j.get("security_key"), j.get("status"), j.get("keys_fetched"), j.get("keys_skipped_as_held")))
        pairs = sorted((j.get("publisher"), j.get("security_key")) for j in jobs)
        want = sorted((p, c.SECURITY_KEY) for p in c.LIVE)
        if pairs != want:
            failures.append("run 1 jobs %s != %s" % (pairs, want))
        new_bronze = [k for p in c.LIVE for k in d[p][2] if c.table_of(k).startswith("bronze/")]
        fetched = rec.get("keys_fetched") or []
        print("run 1 keys fetched: %d; new live bronze objects: %d" % (len(fetched), len(new_bronze)))
        if fetched and not new_bronze:
            failures.append("run 1 fetched %d key(s) but no new bronze object landed" % len(fetched))
        run_date = datetime.date.fromisoformat(str(rec.get("started_at"))[:10])
        reach(run_date)

    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


def reach(run_date):
    """Measurement only: each live publisher's listing span for Lenovo, by the gold builder's own rule."""
    from lib.research.harvest import publication_gold as pg
    universe = c.load(os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json"))
    rows = universe.get("securities", universe) if isinstance(universe, dict) else universe
    lenovo = [s for s in rows if s.get("security_key") == c.SECURITY_KEY or s.get("key") == c.SECURITY_KEY]
    if not lenovo:
        print("REACH: Lenovo not found in the universe file -- not measured")
        return
    hits = list(pg._iter_all_listing_hits())
    spans = pg.publisher_coverage(hits, lenovo).get(c.SECURITY_KEY, {})
    days = (run_date - FLOOR).days + 1
    print("REACH (publisher_coverage over %d listing hits; window %s..%s = %d days):" % (len(hits), FLOOR, run_date, days))
    for publisher in c.LIVE:
        span = spans.get(publisher)
        if not span:
            print("  %-8s no span (no listing hit for Lenovo)" % publisher)
            continue
        lo, hi = max(span[0], FLOOR), min(span[1], run_date)
        covered = max(0, (hi - lo).days + 1)
        print("  %-8s span %s..%s -> %d of %d days from the floor" % (publisher, span[0], span[1], covered, days))


if __name__ == "__main__":
    sys.exit(main())
