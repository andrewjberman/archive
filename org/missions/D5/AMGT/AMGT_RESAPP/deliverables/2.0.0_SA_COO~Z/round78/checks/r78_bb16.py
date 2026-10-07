"""AMGT_RESAPP round 78 -- AMGT-bb-16, the Seeking Alpha last-read reader over the collector's job records.

  python r78_bb16.py --crit AC1|AC2 --where local

AC1 (build) the pure reader `lib/research/freshness/collector_record.py` on fixtures:
  C1 a record with a stored article reads state "read" and its newest article time as the date;
  C2 two records: the date is the greatest newest_article_stored_at, the newest job is the greatest finished_at;
  C3 records that hold no article read state "checked", never a date and never "not collected";
  C4 NO record reads state "no_record": the reader never says "not collected" from an empty partition;
  C5 an object that does not match the contract is counted and not used as a date;
  C6 the September pilot stamp handed in beside no record does not become a date.
AC2 (build, the seam) the ONE contract file `lib/research/freshness/seeking_alpha_job_record.schema.json`:
  S1 the module's REQUIRED_FIELDS equal the schema's `required` list;
  S2 both of the schema's examples parse through the module (2 of 2);
  S3 the module's partition for a slash name is the slash-safe one the writer uses.
Verdict: R78 BB16 <crit> SERVED: YES|NO (exit 0|1). No store is read and nothing is written.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

SCHEMA = "lib/research/freshness/seeking_alpha_job_record.schema.json"
PILOT = "20260911T040304Z"


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _clause(results, name, cond, detail=""):
    results.append(bool(cond))
    print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))


def _rec(finished, stored, newest, status="new_articles", key="BA_US_Equity"):
    return {"schema_version": 1, "security_key": key, "finished_at": finished, "status": status, "stored": stored,
            "newest_article_stored_at": newest}


def _load(results, crit):
    try:
        from lib.research.freshness import collector_record
        return collector_record
    except Exception as exc:  # noqa: BLE001 -- the build check reports any import failure as its first clause
        _clause(results, "C0 lib.research.freshness.collector_record imports", False, str(exc)[:160])
        print("R78 BB16 %s SERVED: NO" % crit)
        return None


def ac1():
    results = []
    cr = _load(results, "AC1")
    if cr is None:
        return 1
    a = _rec("2026-10-07T01:33:00Z", 1992, "2026-10-07T01:32:41Z")
    b = _rec("2026-10-05T09:00:00Z", 3, "2026-10-05T08:59:10Z")
    s = cr.seeking_alpha_state([a])
    _clause(results, "C1 one record with a stored article reads as read, dated by its newest article",
            s.get("state") == "read" and s.get("last_read") == "2026-10-07T01:32:41Z", str(s)[:140])
    s = cr.seeking_alpha_state([b, a])
    _clause(results, "C2 two records: the greatest article time is the date and the greatest end time is the newest job",
            s.get("last_read") == "2026-10-07T01:32:41Z" and s.get("newest_job_finished_at") == "2026-10-07T01:33:00Z"
            and s.get("records") == 2, str(s)[:140])
    s = cr.seeking_alpha_state([_rec("2026-10-07T03:10:05Z", 0, None, status="no_new_articles")])
    _clause(results, "C3 jobs that hold no article read as checked, with no date",
            s.get("state") == "checked" and s.get("last_read") is None and "not collected" not in str(s.get("sentence", "")).lower(),
            str(s)[:140])
    s = cr.seeking_alpha_state([])
    _clause(results, "C4 no record reads no_record, never not collected",
            s.get("state") == "no_record" and s.get("last_read") is None
            and "not collected" not in str(s.get("sentence", "")).lower(), str(s)[:140])
    bad = {"schema_version": 1, "security_key": "BA", "finished_at": "yesterday", "status": "", "stored": -1}
    s = cr.seeking_alpha_state([bad, a])
    _clause(results, "C5 an object off the contract is counted and not used",
            s.get("rejected") == 1 and s.get("records") == 1 and s.get("last_read") == "2026-10-07T01:32:41Z", str(s)[:140])
    s = cr.seeking_alpha_state([], pilot_stamp=PILOT)
    _clause(results, "C6 the pilot stamp beside no record is not a date",
            s.get("state") == "no_record" and s.get("last_read") is None, str(s)[:140])
    ok = all(results)
    print("R78 BB16 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac2():
    results = []
    cr = _load(results, "AC2")
    if cr is None:
        return 1
    with open(os.path.join(_root(), SCHEMA), encoding="utf-8") as fh:
        schema = json.load(fh)
    _clause(results, "S1 the module's required fields are the schema's",
            sorted(cr.REQUIRED_FIELDS) == sorted(schema["required"]), "%s" % (sorted(schema["required"]),))
    parsed = [cr.parse_record(ex) for ex in schema["examples"]]
    good = [p for p in parsed if p is not None]
    _clause(results, "S2 the schema's examples parse through the module", len(good) == len(parsed) == 2,
            "%d of %d" % (len(good), len(parsed)))
    part = cr.partition_for("BP/_LN_Equity")
    _clause(results, "S3 a slash name's partition is the slash-safe one", part == "security_key=BP-SLASH-_LN_Equity", part)
    ok = all(results)
    print("R78 BB16 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    sys.path.insert(0, _root())
    return ac1() if a.crit == "AC1" else ac2()


if __name__ == "__main__":
    sys.exit(main())
