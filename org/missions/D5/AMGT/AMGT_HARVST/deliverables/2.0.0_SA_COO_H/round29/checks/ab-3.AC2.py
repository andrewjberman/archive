"""HVST-ab-3 AC2 (issuer, read-only): what batch 1 MEASURED, per job, and the re-based ceiling for the other 180 names.

Prints, per (name, publisher):
- status, token_source, signed_in, request attempts by class, listing pages OK, `reached_span`, `skipped_pre_floor`;
- for a refusal, its kept body's path and first classifying line (`rejected_bodies/<job_id>*`, runtime; never values).

It then prints the MEASURED pages per publisher (mean over concluded batch-1 jobs), the re-based ceiling for the remaining 180
names with the basis per publisher (MEASURED when at least one batch-1 job of that publisher concluded, else DEFAULT 25), and
the names REACHED (at least one concluded job; phase B's name set).

PASS requires:
- every job records a status and a token_source;
- every CONCLUDED job carries a `reached_span` and a listing page count;
- every refused job names its class (a kept body, or its status when no body is kept).
An honest refusal passes when recorded.
"""
import collections
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab3_common as c  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402

REMAINING = 180
DEFAULT_PAGES = 25


def main():
    failures = []
    runs = c.load(os.path.join(c.WK, "ab3_runs.json"))
    records = c.run_records(sorted(runs.get("run_record_keys") or []))
    jobs = c.jobs_by_pair(records)
    pages = c.listing_pages(records)
    klass = collections.defaultdict(collections.Counter)
    for rec in records:
        for a in rec.get("request_attempts") or []:
            klass[(a.get("security_key"), a.get("publisher"))][a.get("class")] += 1
    measured = collections.defaultdict(list)
    reached = set()
    for (key, pub), j in sorted(jobs.items()):
        concluded = j.get("status") in pg.SUCCESSFUL_RUN_STATUSES
        n = pages.get((key, pub), 0)
        print("%-20s %-8s %-34s token %-22s signed_in %-5s pages %3d span %s pre_floor %s attempts %s"
              % (key, pub, j.get("status"), j.get("token_source"), j.get("signed_in"), n, j.get("reached_span"),
                 j.get("skipped_pre_floor"), dict(klass[(key, pub)])))
        if not j.get("status") or not j.get("token_source"):
            failures.append("%s %s: no status or no token_source" % (key, pub))
        if concluded:
            reached.add(key)
            measured[pub].append(n)
            if not j.get("reached_span"):
                failures.append("%s %s concluded with no reached_span" % (key, pub))
        else:
            bodies = sorted(glob.glob(os.path.join(c.RUNTIME, "rejected_bodies", "%s*" % j.get("job_id"))))
            print("    refusal: status %s; kept bodies %s" % (j.get("status"), [os.path.basename(b) for b in bodies]))
    print("MEASURED pages per publisher (mean over concluded batch-1 jobs):")
    total = 0
    for pub in c.PUBLISHERS:
        vals = measured.get(pub) or []
        if pub in c.LENOVO_PUBS:
            print("  %-8s Lenovo only -- not re-based over the 180 (%s)" % (pub, vals))
            continue
        mean = (sum(vals) / len(vals)) if vals else None
        basis = "MEASURED on %d job(s)" % len(vals) if vals else "DEFAULT"
        per = mean if mean is not None else DEFAULT_PAGES
        total += per * REMAINING
        print("  %-8s mean %s -> %d names x %.1f = %.0f pages (%s)" % (pub, mean, REMAINING, per, per * REMAINING, basis))
    print("RE-BASED CEILING for the other %d names over {bbg, wsj, sa}: %.0f listing pages (DEFAULT would be 180 x 3 x 25 = 13,500)"
          % (REMAINING, total))
    print("NAMES REACHED (phase B's set): %d -- %s" % (len(reached), sorted(reached)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
