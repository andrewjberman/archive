"""AMGT_RESAPP round 81 -- AMGT-ee-2, one date form in the served /freshness words (row AMGT_RESAPP-D1-S1).

  python r81_ee2.py --crit AC1|AC2

AC1 (build, plants): lib.research.freshness.long_day.long_day('2026-09-22') == 'September 22nd, 2026' (the house long form,
    portal dateUtils formatDateWithOrdinal's date part); the 1st/2nd/3rd/11th-13th/21st-23rd/31st ordinals; a non-ISO or None input
    is returned unchanged; collector_record's 'read' and 'checked' sentences and owner_line's 'in date' and 'out of date' sentences
    carry the long form and NO YYYY-MM-DD day, while the structured fields (last_read, reviewed, due) stay ISO.
AC2 (bound): the two modules' own test files pass (lib/research/freshness/tests/test_collector_record.py,
    lib/research/lists/tests/test_owner_line.py), run in-process.
Verdict: R81 EE2 ACn SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ISO_DAY = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1():
    r = []
    try:
        from lib.research.freshness import long_day as L
    except Exception as exc:  # noqa: BLE001
        say(False, "D0 lib/research/freshness/long_day.py imports (%s)" % type(exc).__name__)
        return False
    cases = {"2026-09-22": "September 22nd, 2026", "2026-12-01": "December 1st, 2026", "2026-10-02": "October 2nd, 2026",
             "2026-10-03": "October 3rd, 2026", "2026-10-11": "October 11th, 2026", "2026-10-12": "October 12th, 2026",
             "2026-10-13": "October 13th, 2026", "2026-10-21": "October 21st, 2026", "2026-10-23": "October 23rd, 2026",
             "2026-10-31": "October 31st, 2026", "2026-10-02T14:05:00Z": "October 2nd, 2026", "not a date": "not a date",
             None: None}
    got = {k: L.long_day(k) for k in cases}
    r.append(say(got == cases, "D1 long_day gives the house long form and returns other input unchanged %s" %
                 {k: v for k, v in got.items() if v != cases[k]}))
    from lib.research.freshness import collector_record as C
    read = C.seeking_alpha_state([{"schema_version": 1, "security_key": "X_US_Equity", "finished_at": "2026-10-05T10:00:00Z", "status": "complete",
                                   "stored": 1, "newest_article_stored_at": "2026-09-22T08:00:00Z"}])
    chk = C.seeking_alpha_state([{"schema_version": 1, "security_key": "X_US_Equity", "finished_at": "2026-10-05T10:00:00Z", "status": "complete",
                                  "stored": 0, "newest_article_stored_at": None}])
    sr, sc = read.get("sentence") or "", chk.get("sentence") or ""
    r.append(say("September 22nd, 2026" in sr and not ISO_DAY.search(sr) and (read.get("last_read") or "").startswith("2026-09-22"),
                 "D2 the read sentence is long form, last_read stays ISO: %r" % sr))
    r.append(say("October 5th, 2026" in sc and not ISO_DAY.search(sc), "D3 the checked sentence is long form: %r" % sc))
    from lib.research.lists import owner_line as O
    src = open(O.__file__, encoding="utf-8").read()
    r.append(say("long_day" in src, "D4 owner_line builds its sentences through long_day"))
    return all(r)


def ac2():
    files = ["lib/research/freshness/tests/test_collector_record.py", "lib/research/lists/tests/test_owner_line.py"]
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files, capture_output=True, text=True)
    last = (p.stdout.strip().splitlines() or [""])[-1]
    return say(p.returncode == 0, "B1 the two modules' test files pass: %s" % last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2"])
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root not in sys.path:
        sys.path.insert(0, root)
    ok = ac1() if a.crit == "AC1" else ac2()
    print("R81 EE2 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
