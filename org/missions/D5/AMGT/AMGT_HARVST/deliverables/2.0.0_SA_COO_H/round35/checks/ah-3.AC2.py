"""HVST-ah-3 AC2 (issuer, read-only): ft article bodies unlock -- the locked share falls from the measured 91%.

Reads `~92/ah3_ft_runs.json` = {"before": <run record path>, "after": [<collector run record, verbatim>, ...]} (at least
one ft job run AFTER the fix, through the real collector). Locked = a fetch outcome whose issues include
`publisher_did_not_unlock_body`. PASS requires, over the after-records: at least 40 body fetches, a locked share at or
below 10%, and at least 1 article stored.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/ah3_ft_runs.json")


def shares(records):
    fetches = locked = stored = 0
    for rec in records:
        for o in (rec.get("fetch_outcomes") or {}).values():
            fetches += 1
            if "publisher_did_not_unlock_body" in (o.get("issues") or []):
                locked += 1
            if o.get("outcome") == "stored":
                stored += 1
    return fetches, locked, stored


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no ft run record")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    after = r.get("after") or []
    f, lk, st = shares(after)
    print("AFTER: %d job(s), fetches %d, locked %d (%.0f pct), stored %d" % (len(after), f, lk, 100.0 * lk / f if f else 0, st))
    if f < 40:
        failures.append("only %d body fetches (< 40)" % f)
    if f and lk > 0.10 * f:
        failures.append("locked share %.0f pct > 10 pct" % (100.0 * lk / f))
    if st < 1:
        failures.append("no article stored")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for x in failures:
        print("  FAIL: " + x)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
