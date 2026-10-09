"""IRPT_DASHBD round 54 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's containment ruling @0e8209c33c (msgs 3643, 3696; AMENDMENT 2): the
project's 14 code files that carry real 49F client account numbers are repaired in ONE cell: every literal account number is replaced by its
acct#<first 8 hex of sha256("49financial:<account>")> token, and any code that needs the real id reads it at run time from a file outside the
repo named by the environment variable IRPT_PRIVATE_EVIDENCE_DIR -- never a typed id, never a device path.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB54-1-AC1  each of the 14 files listed in ~83/CODE_REDACTION.json `files` exists at HEAD, carries no 10-digit zero-led token and no
              11-digit zero-led token, py_compiles, and the record's `files` is exactly the 14 paths below; tokens_replaced > 0.
"""
import json
import py_compile
import re
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~83/CODE_REDACTION.json"
B = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
FILES = sorted(B + p for p in (
    "0.9.0_WK_IRPT_DASHBD~1/bd_likeday_pull_r4.py", "0.9.0_WK_IRPT_DASHBD~1/decompose_three_pairs_r6.py",
    "0.9.0_WK_IRPT_DASHBD~1/remeasure_three_pairs_r6.py", "0.9.0_WK_IRPT_DASHBD~2/build_tieout_r8.py",
    "0.9.0_WK_IRPT_DASHBD~2/remeasure_fourteen_pairs_r8.py", "0.9.0_WK_IRPT_DASHBD~21/gap_diagnosis_e1.py",
    "2.0.0_SA_COO~P/checks/r1/p1_1_ac1_gold_under_contract.py", "2.0.0_SA_COO~P/checks/r1/p1_2_ac1_series_manifest.py",
    "2.0.0_SA_COO~P/checks/r1/p1_4_ac1_read_route_local.py", "2.0.0_SA_COO~P/checks/r2/p2_6_ac1_flow_residual_record.py",
    "2.0.0_SA_COO~P/checks/r4/p4_1_ac1_one_pull_in_scope.py", "2.0.0_SA_COO~P/checks/r6/p6_1_ac2_three_pairs_dispositioned.py",
    "2.0.0_SA_COO~P/checks/r8/p8_1_ac2_fourteen_pairs_population_guard.py", "2.0.0_SA_COO~P/p2_window/p2_backfill_driver.py"))
ACCT = re.compile(r"(?<![0-9A-Za-z])0\d{9,10}(?![0-9A-Za-z])")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB54"))
        sys.exit(1)

    if cid != "DB54-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    if sorted(r.get("files") or []) != FILES:
        fail("record files are not exactly the 14 paths")
    if not isinstance(r.get("tokens_replaced"), int) or r["tokens_replaced"] <= 0:
        fail("tokens_replaced %r" % r.get("tokens_replaced"))
    for f in FILES:
        fp = root / f
        if not fp.is_file():
            fail("missing %s" % f)
        if ACCT.search(fp.read_text(encoding="utf-8")):
            fail("%s still carries a zero-led 10/11-digit token" % f)
        try:
            py_compile.compile(str(fp), doraise=True)
        except py_compile.PyCompileError as e:
            fail("%s does not compile: %s" % (f, e))
    print("OK: 14 files carry no account token and compile; %d tokens replaced" % r["tokens_replaced"])
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
