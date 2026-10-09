"""IRPT_DASHBD round 32 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's rounds 30-31 analysis @fe8e06016b (msg 2007) on
ADJUDICATION_v16: tieout_compound_v2.py (~35, DB-b-57) is the reader of record; the tie-out reader adopts flow-START (served values
unchanged); LARGE_FLOW_DAY is traced.

ISSUER RULING (code path): the project's tie-out code path is org/missions/D9/IRPT/IRPT_DASHBD/tieout/ -- project-owned, never served,
outside every deploy lane. The reader of record is READER below.

WRITER CENSUS: every *.py under org/missions/D9/IRPT/IRPT_DASHBD/ that DEFINES a daily-mean fee-base function (a `def` named in
FEE_BASE_NAMES) is a writer. Exactly one may exist, and it is READER.

Usage: python <this file> <repo_root> <criterion_id>
  DB32-1-AC1  READER exists and defines a FEE_BASE_NAMES function; the writer census over the project tree is exactly [READER]
              (printed with its denominator). Base: FAIL.
  DB32-1-AC2  REGRADE_E1.json: `segments` cover exactly round 18's 9,078 graded; within (abs_diff_pp <= 0.35) == 8,088 -- the
              reader of record reproduces round 31's figure; `reader_sha256` equals READER's bytes at HEAD. Base: FAIL.
  DB32-2-AC1  READER declares `FLOW_CONVENTION = "start"`; REGRADE_FLOWSTART_E2.json covers exactly the 9,078 with `within` ==
              the row tally and `reader_sha256` == READER's bytes at HEAD; the within count is printed (not graded against a
              floor). Base: FAIL.
  DB32-2-AC2  every segment WITHIN in REGRADE_E1.json and OUTSIDE in REGRADE_FLOWSTART_E2.json is listed in `in_to_out` with a
              non-empty `reason`, and nothing else is listed. Base: FAIL.
  DB32-3-AC1  LARGE_FLOW_E3.json: `rows` cover exactly the rows of DB-b-58's UNEXPLAINED_CLASSES_E2.json with cause_class
              LARGE_FLOW_DAY (170 at issue), each with a non-empty `sub_class`; `counts` equals the tally. Base: FAIL.
  DB32-3-AC2  every sub_class in `counts` has an entry in `dispositions` with `disposition` "fixed" or "named_cause" and a
              non-empty `cause`. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
READER = PROJ + "tieout/tieout_reader.py"
R18 = D + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
E2_R31 = D + "0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json"
REC1 = D + "0.9.0_WK_IRPT_DASHBD~38/REGRADE_E1.json"
REC2 = D + "0.9.0_WK_IRPT_DASHBD~38/REGRADE_FLOWSTART_E2.json"
REC3 = D + "0.9.0_WK_IRPT_DASHBD~39/LARGE_FLOW_E3.json"
FEE_BASE_NAMES = ("daily_mean_value", "mean_daily_value", "fee_addback_v2", "fee_base_gross", "fee_base_daily_mean")
TOL = 0.35
WITHIN_R31 = 8088


def key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB32"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def reader_sha():
        p = root / READER
        if not p.is_file():
            fail("no reader of record at %s" % READER)
        return hashlib.sha256(p.read_bytes()).hexdigest()

    def graded():
        return {key(s) for s in load(R18)["segments"] if s["verdict"] in ("WITHIN", "OUTSIDE")}

    def regrade(rel):
        r = load(rel)
        segs = r.get("segments") or []
        if {key(s) for s in segs} != graded() or len(segs) != 9078:
            fail("%s: %d segments; equal to round 18's 9,078 graded: %s" % (rel, len(segs), {key(s) for s in segs} == graded()))
        if [s for s in segs if not isinstance(s.get("abs_diff_pp"), (int, float))]:
            fail("%s: a segment without a numeric abs_diff_pp" % rel)
        if r.get("reader_sha256") != reader_sha():
            fail("%s: reader_sha256 differs from %s at HEAD" % (rel, READER))
        return r, segs

    if cid == "DB32-1-AC1":
        pat = re.compile(r"^\s*def\s+(%s)\s*\(" % "|".join(FEE_BASE_NAMES), re.M)
        files = sorted(p for p in (root / PROJ).rglob("*.py") if "__pycache__" not in p.parts)
        writers = [p.relative_to(root).as_posix() for p in files if pat.search(p.read_bytes().decode("utf-8", "replace"))]
        if writers != [READER]:
            fail("writer census over %d .py file(s): %r -- must be exactly [%s]" % (len(files), writers, READER))
        print("OK: writer census over %d .py file(s) under %s = 1 (%s)" % (len(files), PROJ, READER))
    elif cid == "DB32-1-AC2":
        r, segs = regrade(REC1)
        w = sum(1 for s in segs if s["abs_diff_pp"] <= TOL)
        if w != WITHIN_R31:
            fail("within %d on the reader of record; round 31 measured %d" % (w, WITHIN_R31))
        print("OK: reader of record re-grades 9,078: within %d (= round 31's %d); sha matches HEAD" % (w, WITHIN_R31))
    elif cid == "DB32-2-AC1":
        src = (root / READER).read_bytes().decode("utf-8") if (root / READER).is_file() else ""
        if not re.search(r'^FLOW_CONVENTION\s*=\s*["\']start["\']', src, re.M):
            fail('%s does not declare FLOW_CONVENTION = "start"' % READER)
        r, segs = regrade(REC2)
        w = sum(1 for s in segs if s["abs_diff_pp"] <= TOL)
        if r.get("within") != w:
            fail("within %r, the row tally %d" % (r.get("within"), w))
        print("OK: flow-start re-grade over 9,078: within %d (printed, not graded against a floor); sha matches HEAD" % w)
    elif cid == "DB32-2-AC2":
        _, a = regrade(REC1)
        r, b = regrade(REC2)
        bk = {key(s): s for s in b}
        want = {key(s) for s in a if s["abs_diff_pp"] <= TOL and bk[key(s)]["abs_diff_pp"] > TOL}
        got = r.get("in_to_out") or []
        if {key(x) for x in got} != want or len(got) != len(want):
            fail("in_to_out lists %d; the records give %d: equal %s" % (len(got), len(want), {key(x) for x in got} == want))
        if [x for x in got if not str(x.get("reason") or "").strip()]:
            fail("an in_to_out segment without a reason")
        print("OK: %d segment(s) IN->OUT under flow-start, every one named" % len(want))
    elif cid in ("DB32-3-AC1", "DB32-3-AC2"):
        pop = {key(x) for x in load(E2_R31)["rows"] if x.get("cause_class") == "LARGE_FLOW_DAY"}
        r = load(REC3)
        rows = r.get("rows") or []
        if {key(x) for x in rows} != pop or len(rows) != len(pop):
            fail("%d rows; equal to the %d LARGE_FLOW_DAY rows: %s" % (len(rows), len(pop), {key(x) for x in rows} == pop))
        if [x for x in rows if not str(x.get("sub_class") or "").strip()]:
            fail("a row without a sub_class")
        tally = {}
        for x in rows:
            tally[x["sub_class"]] = tally.get(x["sub_class"], 0) + 1
        if (r.get("counts") or {}) != tally:
            fail("counts %r, the tally %r" % (r.get("counts"), tally))
        if cid == "DB32-3-AC1":
            print("OK: %d of %d LARGE_FLOW_DAY traced into %d sub-class(es): %s" % (len(rows), len(pop), len(tally), tally))
        else:
            disp = r.get("dispositions") or {}
            bad = [k for k in tally if (disp.get(k) or {}).get("disposition") not in ("fixed", "named_cause")
                   or not str((disp.get(k) or {}).get("cause") or "").strip()]
            if bad:
                fail("sub-classes without a disposition (fixed/named_cause) and a cause: %r" % bad)
            print("OK: every sub-class dispositioned: %s" % {k: disp[k]["disposition"] for k in tally})
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
