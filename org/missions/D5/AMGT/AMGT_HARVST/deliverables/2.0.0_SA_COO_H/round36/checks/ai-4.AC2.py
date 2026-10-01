"""HVST-ai-4 AC2 (issuer, read-only): the stranded bbg backfill drains -- no bbg item stays pending on JSONDecodeError (row Z-S57).

Reads the live bbg runtime outbox (`.runtime/opal-data-harvest-bbg/progress.sqlite3`, table harvest_raw_outbox).
Prints the count per (status, error_code). PASS requires: 0 bbg rows pending with JSONDecodeError, and at least 700
bbg rows uploaded (772 were stranded when the row was filed).
"""
import os
import sqlite3
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
DB = os.path.join(ROOT, ".runtime/opal-data-harvest-bbg/progress.sqlite3")


def main():
    failures = []
    if not os.path.exists(DB):
        print("OUTBOX: absent (%s)" % DB)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no bbg runtime outbox")
        return 1
    db = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
    rows = db.execute("SELECT status, error_code, count(*) FROM harvest_raw_outbox WHERE publisher='bbg' "
                      "GROUP BY status, error_code").fetchall()
    total = sum(r[2] for r in rows)
    print("BBG OUTBOX (%d rows): %s" % (total, rows))
    stranded = sum(r[2] for r in rows if r[0] != "uploaded" and r[1] == "JSONDecodeError")
    uploaded = sum(r[2] for r in rows if r[0] == "uploaded")
    if stranded:
        failures.append("%d bbg rows still pending on JSONDecodeError" % stranded)
    if uploaded < 700:
        failures.append("only %d bbg rows uploaded (< 700)" % uploaded)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
