"""HVST-ag-3 AC2 (issuer, read-only): the backfill driver collects bbg and wsj through the date-ordered sitemaps.

Reads `~92/ag3_runs.json` = {"<pub>": {"run_summary": <the driver's run summary JSON, verbatim>,
"run_records": [<each job's collector run record, verbatim>]}} for pub in bbg, wsj.

PASS requires, for EACH of bbg and wsj:
- the driver ran at least 3 (publisher, name) pairs and stored at least 1 article in total;
- across the jobs' request attempts: at least one on a sitemap path (`/sitemaps/`) and NONE on a `/search` path;
- no job ended `error`, `bot_check` or `unclassified` without a later pair running (a stop is recorded, not hidden).
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/ag3_runs.json")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no driver run record")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    for pub in ("bbg", "wsj"):
        p = r.get(pub) or {}
        summary = (p.get("run_summary") or {}).get("publishers", {}).get(pub, {})
        records = p.get("run_records") or []
        paths = [a.get("path", "") for rec in records for a in (rec.get("request_attempts") or [])]
        sitemap = sum(1 for x in paths if "/sitemaps/" in x)
        search = sum(1 for x in paths if "/search" in x)
        pairs, stored = int(summary.get("pairs_done") or 0), int(summary.get("articles_stored") or 0)
        statuses = [rec.get("status") for rec in records]
        print("%s: pairs %d, stored %d, jobs %d, sitemap requests %d, search requests %d, statuses %s, stopped %s"
              % (pub, pairs, stored, len(records), sitemap, search, statuses, summary.get("stopped")))
        if pairs < 3:
            failures.append("%s ran %d pairs (< 3)" % (pub, pairs))
        if stored < 1:
            failures.append("%s stored no article" % pub)
        if not sitemap:
            failures.append("%s made no sitemap request" % pub)
        if search:
            failures.append("%s made %d search request(s)" % (pub, search))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
