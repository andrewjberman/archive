"""HVST-af-4 AC2 (issuer, read-only): one live bbg collector job lists through the date-ordered sitemap, never search.

Reads `~92/af4_bbg_run.json` = the collector's own run record of that job (copied verbatim) plus
{"run_record_path": ...}. PASS requires:
- `publisher` == "bbg" and a status that is not `error` / `bot_check` / `unclassified`;
- at least one request attempt on a `/sitemaps/news/` path and NONE on a `/search` path;
- `accepted` holds at least 1 article.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/af4_bbg_run.json")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no bbg run record")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    paths = [a.get("path", "") for a in r.get("request_attempts") or []]
    sitemap = [p for p in paths if "/sitemaps/news/" in p]
    search = [p for p in paths if "/search" in p]
    print("JOB: %s %s status=%s accepted=%d attempts=%d sitemap=%d search=%d"
          % (r.get("publisher"), r.get("security_key"), r.get("status"), len(r.get("accepted") or []), len(paths),
             len(sitemap), len(search)))
    if r.get("publisher") != "bbg":
        failures.append("not a bbg job")
    if r.get("status") in ("error", "bot_check", "unclassified", None):
        failures.append("status %r" % r.get("status"))
    if not sitemap:
        failures.append("no request on a /sitemaps/news/ path")
    if search:
        failures.append("%d request(s) on a /search path" % len(search))
    if len(r.get("accepted") or []) < 1:
        failures.append("no article accepted")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
