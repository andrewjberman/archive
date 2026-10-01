"""HVST-ad-2 AC2 (issuer, read-only): what sa batch 1 MEASURED.

Prints, per name: status, reached_span, listing pages OK, `skipped_pre_floor`, keys fetched and stored, and the stop status
if any. Then it prints the MEASURED sa pages per name (mean over the concluded jobs), the re-based sa ceiling for the other 79
resolved names (MEASURED when at least one job concluded, else DEFAULT 25), and the names REACHED.

PASS requires:
- every job records a status;
- every concluded job carries a `reached_span` and a page count;
- the batch either ran all 10 or ended at a recorded STOP status.
An honest stop passes when recorded.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ad2_common as c  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402

REMAINING = 79
DEFAULT_PAGES = 25


def main():
    failures = []
    runs = c.load(os.path.join(c.WK, "ad2_runs.json"))
    records = c.run_records(runs.get("run_record_keys") or [])
    jobs = [j for rec in sorted(records, key=lambda r: r.get("started_at") or "") for j in rec.get("jobs") or []]
    pages = {}
    for rec in records:
        for a in rec.get("request_attempts") or []:
            if a.get("request_kind") == "listing" and a.get("class") == "ok":
                pages[a.get("security_key")] = pages.get(a.get("security_key"), 0) + 1
    measured, reached, stop = [], [], None
    for j in jobs:
        k = j.get("security_key")
        concluded = j.get("status") in pg.SUCCESSFUL_RUN_STATUSES
        print("%-28s %-34s pages %3d span %s pre_floor %s fetched %s"
              % (k, j.get("status"), pages.get(k, 0), j.get("reached_span"), j.get("skipped_pre_floor"),
                 len(j.get("keys_fetched") or []) if isinstance(j.get("keys_fetched"), list) else j.get("keys_fetched")))
        if not j.get("status"):
            failures.append("%s: no status" % k)
        # Z-W88-S4 fix: a job MEASURES its pages when its listing reached a span, whatever its final status (a late
        # article 5xx or proxy error ends the job non-concluded after the listing completed). REACHED = concluded.
        if j.get("reached_span"):
            measured.append(pages.get(k, 0))
        if concluded:
            reached.append(k)
            if not j.get("reached_span"):
                failures.append("%s concluded with no reached_span" % k)
        if j.get("status") in c.STOP_STATUSES:
            stop = (k, j.get("status"))
    if len(jobs) < c.N and not stop:
        failures.append("the batch ran %d of %d names with no recorded STOP status" % (len(jobs), c.N))
    mean = sum(measured) / len(measured) if measured else None
    per = mean if mean is not None else DEFAULT_PAGES
    print("STOP: %s" % (("%s %s" % stop) if stop else "none (ran all %d)" % len(jobs)))
    print("MEASURED sa pages per name: mean %s over %d job(s) whose listing reached a span" % (mean, len(measured)))
    print("RE-BASED sa CEILING for the other %d resolved names: %.0f listing pages (%s; DEFAULT would be %d)"
          % (REMAINING, per * REMAINING, "MEASURED" if measured else "DEFAULT", REMAINING * DEFAULT_PAGES))
    print("NAMES REACHED: %d -- %s" % (len(reached), reached))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
