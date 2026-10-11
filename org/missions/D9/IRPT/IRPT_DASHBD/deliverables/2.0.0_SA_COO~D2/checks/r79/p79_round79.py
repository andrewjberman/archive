"""IRPT_DASHBD round 79 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-78 ANALYSIS @bf620b7e50, section 3 items 3 and 4.

Item 1 is the issuer's own act (deliverables/2.0.0_SA_COO~D2/ISSUER_RUNS_ROUND78_ITEM1.md); items 2 and 5 were issued as round 78.
Cells: DB-b-151 (item 3, row D2-W116-S2) the copy against the original on the three sampled days, metadata and row counts only, and
every figure of the tie-out records named with the store it was read from; DB-b-152 and DB-b-153 (item 4, row D2-W118-S1) the three
withdrawn figures amended in the two records that quote them.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB79-1-AC1  ~124/COPY_VS_ORIGINAL.json: days (3) each {day, original {read, rows, last_modified}, copy {read, rows,
              last_modified}, rows_equal (bool or "NOT_ESTABLISHED")}; original_rewritten_after_copy (true / false /
              "NOT_ESTABLISHED") with a reason; figure_sources (42) each {record, figure, store}; store is one of COPY, ORIGINAL,
              FEED, SERVED_GOLD, CUSTODIAN_PULL, DERIVED, WITHDRAWN; s3_writes 0; no string holds a run of 8 or more digits.
  DB79-2-AC1  ~104/UNEXPLAINED_244.json carries withdrawn_figures with 2 entries, each {figure, why, withdrawn_by}; the record
              still states its 244 and its classes summing to it.
  DB79-3-AC1  ~113/UNREPRODUCED_18.json carries withdrawn_figures with 1 entry {figure, why, withdrawn_by}; the record still
              states its denominator 18.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
STORES = {"COPY", "ORIGINAL", "FEED", "SERVED_GOLD", "CUSTODIAN_PULL", "DERIVED", "WITHDRAWN"}


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
        print("%s FAIL" % (cid or "DB79"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def withdrawn(r, n):
        w = r.get("withdrawn_figures")
        if not isinstance(w, list) or len(w) != n:
            fail("withdrawn_figures holds %s entr(ies), want %d" % (len(w) if isinstance(w, list) else "no", n))
        for x in w:
            if not str(x.get("figure") or "").strip() or not str(x.get("why") or "").strip() or not str(x.get("withdrawn_by") or "").strip():
                fail("a withdrawn figure lacks its text, its why or who withdrew it")

    if cid == "DB79-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~124/COPY_VS_ORIGINAL.json")
        days = r.get("days") or []
        if len(days) != 3:
            fail("%d day(s), want 3" % len(days))
        for d in days:
            for side in ("original", "copy"):
                s = d.get(side) or {}
                if not isinstance(s.get("read"), bool) or (s["read"] and (not isinstance(s.get("rows"), int) or not str(s.get("last_modified") or "").strip())) \
                        or (not s["read"] and not str(s.get("reason") or "").strip()):
                    fail("day %r, %s: read, rows and last_modified (or a reason) are required" % (d.get("day"), side))
            if d.get("rows_equal") not in (True, False, "NOT_ESTABLISHED"):
                fail("day %r rows_equal %r" % (d.get("day"), d.get("rows_equal")))
        if r.get("original_rewritten_after_copy") not in (True, False, "NOT_ESTABLISHED") or not str(r.get("rewritten_reason") or "").strip():
            fail("original_rewritten_after_copy %r or no reason" % r.get("original_rewritten_after_copy"))
        fs = r.get("figure_sources") or []
        if len(fs) != 42:
            fail("%d figure source(s), want the 42 of DB-b-145's list" % len(fs))
        for f in fs:
            if not str(f.get("record") or "").strip() or not str(f.get("figure") or "").strip() or f.get("store") not in STORES:
                fail("a figure lacks its record, its text or a store from the set: %r" % f.get("store"))
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: 3 days compared by metadata and row count; the original rewritten after the copy: %s; 42 of 42 figures name their store"
              % r["original_rewritten_after_copy"])
    elif cid == "DB79-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~104/UNEXPLAINED_244.json")
        withdrawn(r, 2)
        cl = r.get("classes") or []
        rem = (r.get("remainder") or {}).get("count")
        if r.get("denominator") != 244 or not isinstance(rem, int) or sum(c.get("count", 0) for c in cl) + rem != 244:
            fail("the record no longer states 244 with its classes and remainder summing to it")
        print("OK: 2 figures marked withdrawn in the 244 record; its classes and remainder still sum to 244")
    elif cid == "DB79-3-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~113/UNREPRODUCED_18.json")
        withdrawn(r, 1)
        if r.get("denominator") != 18:
            fail("the record no longer states its denominator 18")
        print("OK: 1 figure marked withdrawn in the 18 record; its denominator stands")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
