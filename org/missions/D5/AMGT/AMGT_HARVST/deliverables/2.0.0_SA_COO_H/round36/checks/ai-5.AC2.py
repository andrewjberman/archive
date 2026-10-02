"""HVST-ai-5 AC2 (issuer, read-only): the bbg outbox is drained -- at most the one W91-S19 row stays pending (row Z-S58).

Reads the live bbg runtime outbox (`.runtime/opal-data-harvest-bbg/progress.sqlite3`, table harvest_raw_outbox) and
the bbg runtime's own `last-harvest-upload.json` receipt. Prints the count per (status, error_code). PASS requires: at
most 1 bbg row pending (any error code), and that row (if any) on SilverRowError, not JSONDecodeError.
"""
import json
import os
import sqlite3
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RT = os.path.join(ROOT, ".runtime/opal-data-harvest-bbg")
DB = os.path.join(RT, "progress.sqlite3")


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
    pending = [r for r in rows if r[0] != "uploaded"]
    n_pending = sum(r[2] for r in pending)
    if n_pending > 1:
        failures.append("%d bbg rows still pending (at most 1, the W91-S19 row, is allowed)" % n_pending)
    if any(r[1] != "SilverRowError" for r in pending):
        failures.append("a pending bbg row is not the SilverRowError row: %s" % pending)
    receipt = os.path.join(RT, "last-harvest-upload.json")
    if os.path.exists(receipt):
        with open(receipt, encoding="utf-8") as fh:
            print("LAST UPLOAD remaining_pending: %s" % json.load(fh).get("remaining_pending"))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
