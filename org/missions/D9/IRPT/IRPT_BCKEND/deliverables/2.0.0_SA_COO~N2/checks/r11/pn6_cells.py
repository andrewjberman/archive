"""IRPT_BCKEND workstream ~PO round 11 (issuer 2.0.0_SA_COO~N2) -- the checks of the WORLD read-only order IB-pn-6: the two reads the
CTO ruling @2f780e14a6 asks for before ADDENDUM 5 (the roster's earliest start date and the day count N, and the measured size of the
first scheduled run's bronze and silver objects).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
Grades the record the seat writes at deliverables/0.7.0_AE_CloudOps~IB2/IBN6-1_reads_record.json (counts, dates, bytes and flags only).

  IBN6-AC1  the roster read: earliest start date, first scheduled run's day, N equal to the days between them, households within 294,
            accounts counted, the null-start-date count stated, and whether N is within the script's 4000-day limit stated and consistent
  IBN6-AC2  the size read: the first run's bronze and silver objects each one key, one version, bytes above zero
  IBN6-AC3  read-only: no write to AWS, no Orion request, and the record holds only the named members (no identifier of any kind)
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IBN6-1_reads_record.json"
LIMIT = 4000
BOUND = 294
TOP = {"reads", "aws_writes_made", "orion_requests"}
READS = {"read_at_utc", "first_run_day", "earliest_start_date", "day_count_n", "n_within_limit", "household_count",
         "accounts_in_universe", "accounts_with_null_start_date", "bronze_object", "silver_object"}
OBJ = {"keys", "versions", "bytes"}
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def need(cid, cond, why):
    if not cond:
        fail(cid, why)


def load(root, cid):
    path = root / RECORD
    if not path.is_file():
        fail(cid, "reads record absent: " + RECORD)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail(cid, "reads record is not JSON: %s" % exc)
    need(cid, isinstance(doc, dict) and isinstance(doc.get("reads"), dict), "record: no reads object")
    return doc


def day(cid, value, label):
    need(cid, isinstance(value, str) and DAY.match(value) is not None, "record: %s is not a YYYY-MM-DD date" % label)
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        fail(cid, "record: %s is not a calendar date" % label)


def is_int(value):
    return type(value) is int


def ac1(root):
    cid = "IBN6-AC1"
    r = load(root, cid)["reads"]
    first, earliest = day(cid, r.get("first_run_day"), "first_run_day"), day(cid, r.get("earliest_start_date"), "earliest_start_date")
    need(cid, earliest <= first, "record: the earliest start date is after the first run's day")
    n = r.get("day_count_n")
    need(cid, is_int(n) and n == (first - earliest).days, "record: day_count_n must equal the days from the earliest start date to the first run's day")
    need(cid, r.get("n_within_limit") is (n <= LIMIT), "record: n_within_limit must state whether N is within %d days" % LIMIT)
    hc = r.get("household_count")
    need(cid, is_int(hc) and 0 < hc <= BOUND, "record: household count above the bound %d or absent" % BOUND)
    acc, null = r.get("accounts_in_universe"), r.get("accounts_with_null_start_date")
    need(cid, is_int(acc) and acc > 0 and is_int(null) and 0 <= null <= acc, "record: account counts absent or inconsistent")
    need(cid, isinstance(r.get("read_at_utc"), str) and STAMP.match(r["read_at_utc"]) is not None, "record: read_at_utc is not a UTC stamp")


def ac2(root):
    cid = "IBN6-AC2"
    r = load(root, cid)["reads"]
    for name in ("bronze_object", "silver_object"):
        o = r.get(name)
        need(cid, isinstance(o, dict) and set(o) == OBJ, "record: %s must hold exactly keys, versions, bytes" % name)
        need(cid, o["keys"] == 1 and o["versions"] == 1, "record: %s must be one key with one version" % name)
        need(cid, is_int(o["bytes"]) and o["bytes"] > 0, "record: %s bytes must be an integer above zero" % name)


def ac3(root):
    cid = "IBN6-AC3"
    doc = load(root, cid)
    need(cid, set(doc) == TOP, "record: top-level members must be exactly %s" % sorted(TOP))
    need(cid, set(doc["reads"]) == READS, "record: reads members must be exactly %s" % sorted(READS))
    need(cid, doc["aws_writes_made"] == 0 and doc["orion_requests"] == 0, "record: a write to AWS or an Orion request was made")
    need(cid, is_int(doc["aws_writes_made"]) and is_int(doc["orion_requests"]), "record: the write and request counts must be integers")


CHECKS = {"IBN6-AC1": ac1, "IBN6-AC2": ac2, "IBN6-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn6_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
