"""IRPT_DASHBD round 81 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5937: the open half of row D2-W124-S1.

Cell DB-b-156: does any reader the tie-out or the served dashboard uses key on the FILE's day and not the transaction's own date;
and, for the two sampled days, the ids' own dates against the files they now sit in.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB81-1-AC1  ~126/FILE_DAY_READERS.json: readers_considered (int > 0) == len(readers); each reader {file, line (int), used_by
              (TIE_OUT / SERVED_DASHBOARD / BOTH), keys_on (FILE_DAY / TRANSACTION_DATE / BOTH / NEITHER / NOT_ESTABLISHED),
              basis}; file_day_keyed (int) == the count of readers whose keys_on is FILE_DAY or BOTH; days (2) each {day,
              ids_then (int), ids_found_now (int), files_now (int), own_date_equals_then_file_day (int or "NOT_ESTABLISHED"),
              own_date_equals_now_file_day (int or "NOT_ESTABLISHED")}; answer {any_reader_keys_on_file_day (bool or
              "NOT_ESTABLISHED"), basis}; s3_writes 0; no string holds a run of 8 or more digits.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
NE = "NOT_ESTABLISHED"


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB81"))
        sys.exit(1)

    def is_int(v):
        return isinstance(v, int) and not isinstance(v, bool) and v >= 0

    if cid != "DB81-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (M + "0.9.0_WK_IRPT_DASHBD~126/FILE_DAY_READERS.json")
    if not p.is_file():
        fail("no record 0.9.0_WK_IRPT_DASHBD~126/FILE_DAY_READERS.json")
    r = json.loads(p.read_bytes().decode("utf-8"))
    rd = r.get("readers") or []
    if not is_int(r.get("readers_considered")) or r["readers_considered"] < 1 or r["readers_considered"] != len(rd):
        fail("readers_considered %r against %d reader(s) listed" % (r.get("readers_considered"), len(rd)))
    for x in rd:
        if not str(x.get("file") or "").strip() or not is_int(x.get("line")) or x.get("used_by") not in ("TIE_OUT", "SERVED_DASHBOARD", "BOTH") \
                or x.get("keys_on") not in ("FILE_DAY", "TRANSACTION_DATE", "BOTH", "NEITHER", NE) or not str(x.get("basis") or "").strip():
            fail("reader %r lacks its file, line, used_by, keys_on or basis" % x.get("file"))
    n = sum(1 for x in rd if x["keys_on"] in ("FILE_DAY", "BOTH"))
    if r.get("file_day_keyed") != n:
        fail("file_day_keyed %r against %d reader(s) so classed" % (r.get("file_day_keyed"), n))
    days = r.get("days") or []
    if len(days) != 2:
        fail("%d day(s), want 2" % len(days))
    for d in days:
        if not str(d.get("day") or "").strip() or not all(is_int(d.get(k)) for k in ("ids_then", "ids_found_now", "files_now")) \
                or not all(is_int(d.get(k)) or d.get(k) == NE for k in ("own_date_equals_then_file_day", "own_date_equals_now_file_day")):
            fail("day %r lacks a count" % d.get("day"))
    a = r.get("answer") or {}
    if a.get("any_reader_keys_on_file_day") not in (True, False, NE) or not str(a.get("basis") or "").strip():
        fail("answer needs any_reader_keys_on_file_day and its basis")
    if a.get("any_reader_keys_on_file_day") is True and n == 0 or a.get("any_reader_keys_on_file_day") is False and n != 0:
        fail("the answer disagrees with the readers table (%d keyed on the file day)" % n)
    if r.get("s3_writes") != 0:
        fail("s3_writes %r" % r.get("s3_writes"))
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: %d reader(s) considered, %d keyed on the file day; 2 days: ids then %s, found now %s; any reader keys on the file day: %s"
          % (len(rd), n, [d["ids_then"] for d in days], [d["ids_found_now"] for d in days], a["any_reader_keys_on_file_day"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
