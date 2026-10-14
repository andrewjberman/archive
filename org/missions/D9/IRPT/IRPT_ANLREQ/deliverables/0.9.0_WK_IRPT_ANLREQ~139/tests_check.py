#!/usr/bin/env python3
"""AR331-y-AC1 (TO-AR-y-331): the test checker for the commentary PDF route.

Runs the NEW route test file, the cross-check file (case g), and every test file under ops/tests/, reports/tests/ and
_authz/tests/ whose name contains pdf, route, entry, status, owned or operation (the file list is printed). Counts come
from pytest's JUnit XML, never from its summary line. Prints TESTS-OK only when every case (a) to (f) of the new file and
(g) of the cross-check file pass and no other listed file has a failure or an error; otherwise TESTS-BAD <why>, exit 1.
ASCII only. The repository root is derived from this file's location, never typed.
"""
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]  # deliverables/<serial> -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> root
INV = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
NEW = INV / "ops" / "tests" / "test_commentary_pdf_route.py"
CROSS = INV / "ycharts" / "research" / "tests" / "test_commentary_logical_id_matches_ops.py"
DIRS = ("ops/tests", "reports/tests", "_authz/tests")
NAME_PARTS = ("pdf", "route", "entry", "status", "owned", "operation")
# Case (a) to (f) of the new file, and (g) of the cross-check file, by the test name each one is written under.
NEW_CASES = {
    "(a)": ("test_the_owner_gets_a_signed_link_to_the_retained_commentary_artifact", NEW.stem),
    "(b)": ("test_a_non_owner_is_refused_exactly_as_the_report_pdf_is", NEW.stem),
    "(c)": ("test_an_opal_global_viewer_meets_the_same_owner_gate_as_the_report_pdf", NEW.stem),
    "(d)": ("test_no_commentary_ref_or_no_retained_commentary_pdf_is_refused_by_name", NEW.stem),
    "(e)": ("test_the_route_is_registered_with_the_owned_record_mode_and_the_request_id_parameter", NEW.stem),
    "(f)": ("test_the_commentary_pdf_route_serves_the_commentary_artifact_never_the_reports_own_pdf", NEW.stem),
    "(g1)": ("test_commentary_logical_id_matches_the_producer_for_three_pairs", CROSS.stem),
    "(g2)": ("test_commentary_family_matches_the_producer", CROSS.stem),
}


def listed_files():
    found = []
    for rel in DIRS:
        for path in sorted((INV / rel).glob("test_*.py")):
            if any(part in path.name for part in NAME_PARTS) and path != NEW:
                found.append(path)
    return found


def run_junit(files, xml_path):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "--tb=no",
           "--junitxml=" + xml_path] + [str(p) for p in files]
    proc = subprocess.run(cmd, cwd=str(INV), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    return proc.returncode


def cases(xml_path):
    """(classname, name, status) per testcase; status is pass, fail, skip."""
    out = []
    root = ET.parse(xml_path).getroot()
    for case in root.iter("testcase"):
        status = "pass"
        for child in case:
            if child.tag in ("failure", "error"):
                status = "fail"
            elif child.tag == "skipped":
                status = "skip"
        out.append((case.get("classname") or "", case.get("name") or "", status))
    collect_errors = sum(int(s.get("errors") or 0) for s in root.iter("testsuite"))
    return out, collect_errors


def main():
    files = listed_files()
    print("LISTED FILES (%d):" % len(files))
    for path in files:
        print("  " + str(path.relative_to(INV)).replace(os.sep, "/"))
    targets = [NEW, CROSS] + files
    with tempfile.TemporaryDirectory(prefix="tests_check_") as tmp:
        xml_path = os.path.join(tmp, "junit.xml")
        try:
            rc = run_junit(targets, xml_path)
        except subprocess.TimeoutExpired:
            print("TESTS-BAD pytest run exceeded its bound")
            return 1
        if not os.path.exists(xml_path):
            print("TESTS-BAD no junit report (pytest rc=%d)" % rc)
            return 1
        rows, collect_errors = cases(xml_path)
    if collect_errors:
        print("TESTS-BAD %d collection error(s) in the listed files" % collect_errors)
        return 1
    new_rows = [r for r in rows if r[0].endswith(NEW.stem)]
    cross_rows = [r for r in rows if r[0].endswith(CROSS.stem)]
    other_rows = [r for r in rows if not (r[0].endswith(NEW.stem) or r[0].endswith(CROSS.stem))]
    missing = []
    for label, (name, stem) in sorted(NEW_CASES.items()):
        pool = new_rows if stem == NEW.stem else cross_rows
        hits = [r for r in pool if r[1] == name or r[1].startswith(name + "[")]
        if not hits or any(r[2] != "pass" for r in hits):
            missing.append("%s %s" % (label, name))
    if missing:
        print("TESTS-BAD cases not passing: " + "; ".join(missing))
        return 1
    new_passed = sum(1 for r in new_rows if r[2] == "pass")
    other_passed = sum(1 for r in other_rows if r[2] == "pass")
    other_failed = sum(1 for r in other_rows if r[2] == "fail")
    print("new file %s: %d passed, %d failed; cross-check: %d passed"
          % (NEW.name, new_passed, sum(1 for r in new_rows if r[2] == "fail"),
             sum(1 for r in cross_rows if r[2] == "pass")))
    print("others: %d passed, %d skipped, %d failed" % (other_passed, sum(1 for r in other_rows if r[2] == "skip"),
                                                       other_failed))
    if other_failed:
        names = sorted("%s::%s" % (r[0], r[1]) for r in other_rows if r[2] == "fail")
        print("TESTS-BAD %d failing case(s) outside the new file: %s" % (other_failed, "; ".join(names)))
        return 1
    if new_passed == 0 or other_passed == 0:
        print("TESTS-BAD an empty denominator (new=%d others=%d)" % (new_passed, other_passed))
        return 1
    print("TESTS-OK %d new, %d others, 0 failed" % (new_passed, other_passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
