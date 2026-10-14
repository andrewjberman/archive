#!/usr/bin/env python3
"""AR331-y-AC1 (TO-AR-y-331, AMENDED by AMENDMENT 2): the test checker for the commentary PDF route.

Runs, one pytest process per folder (the folders share the module name 'entry', so one process over several of them
collides), every test_*.py file under ops/tests/, reports/tests/, _authz/tests/ and _contracts/tests/ (the file list is
printed), and the cross-check file of case (g) under ycharts/research/tests/. Counts come from pytest's JUnit XML, never
from its summary line.

Verdict: TESTS-OK only when (1) every case of the NEW route file and of the cross-check file passes and (2) every failing
case name of the other files is a name recorded in r41/baseline_failures.json, the failing names of a clean FULL worktree
at the record's base commit. A baseline failure is not this order's to fix; a failing name the baseline does not hold is
this order's, and fails the check. Otherwise TESTS-BAD <why>, exit 1.

  python tests_check.py                      the check, on this worktree
  python tests_check.py --take-baseline <root> <out.json>
                                             the failing names of the four folders at <root> (a clean worktree of the
                                             base; the new files are absent there and are not run). Run ONCE.

ASCII only. The repository root is derived from this file's location (never typed); the baseline mode takes its root.
"""
import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[7]  # deliverables/<serial> -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> root
BASELINE = HERE / "r41" / "baseline_failures.json"
FOLDERS = ("ops/tests", "reports/tests", "_authz/tests", "_contracts/tests")
NEW_REL = "ops/tests/test_commentary_pdf_route.py"
CROSS_REL = "ycharts/research/tests/test_commentary_logical_id_matches_ops.py"
# Case (a) to (f) of the new file, and (g1), (g2) of the cross-check file, by the test name each one is written under.
NEW_CASES = {
    "(a)": "test_the_owner_gets_a_signed_link_to_the_retained_commentary_artifact",
    "(b)": "test_a_non_owner_is_refused_exactly_as_the_report_pdf_is",
    "(c)": "test_an_opal_global_viewer_meets_the_same_owner_gate_as_the_report_pdf",
    "(d)": "test_no_commentary_ref_or_no_retained_commentary_pdf_is_refused_by_name",
    "(e)": "test_the_route_is_registered_with_the_owned_record_mode_and_the_request_id_parameter",
    "(f)": "test_the_commentary_pdf_route_serves_the_commentary_artifact_never_the_reports_own_pdf",
    "(g1)": "test_commentary_logical_id_matches_the_producer_for_three_pairs",
    "(g2)": "test_commentary_family_matches_the_producer",
}


def folder_files(inv, rel):
    return sorted((inv / rel).glob("test_*.py"))


def groups(inv):
    """(label, files) per pytest process: the cross-check file alone, then each folder with its files."""
    out = []
    if (inv / CROSS_REL).is_file():
        out.append((CROSS_REL, [inv / CROSS_REL]))
    for rel in FOLDERS:
        out.append((rel, folder_files(inv, rel)))
    return out


def run_group(inv, files, xml_path):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "--tb=no",
           "--junitxml=" + xml_path] + [str(p) for p in files]
    proc = subprocess.run(cmd, cwd=str(inv), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    return proc.returncode


def read_cases(xml_path):
    """(classname, name, status, errors) per testcase; status is pass, fail or skip."""
    out, errors = [], 0
    root = ET.parse(xml_path).getroot()
    for suite in root.iter("testsuite"):
        errors += int(suite.get("errors") or 0)
    for case in root.iter("testcase"):
        status = "pass"
        for child in case:
            if child.tag in ("failure", "error"):
                status = "fail"
            elif child.tag == "skipped" and status == "pass":
                status = "skip"
        out.append((case.get("classname") or "", case.get("name") or "", status))
    return out, errors


def run_all(inv):
    """Run every group under `inv`; return ({label: rows}, [collect errors per group])."""
    rows_by, errors_by = {}, {}
    with tempfile.TemporaryDirectory(prefix="tests_check_") as tmp:
        for index, (label, files) in enumerate(groups(inv)):
            if not files:
                rows_by[label], errors_by[label] = [], 0
                continue
            xml_path = os.path.join(tmp, "junit_%d.xml" % index)
            rc = run_group(inv, files, xml_path)
            if not os.path.exists(xml_path):
                raise RuntimeError("no junit report for %s (pytest rc=%d)" % (label, rc))
            rows_by[label], errors_by[label] = read_cases(xml_path)
    return rows_by, errors_by


def failing_key(row):
    return "%s::%s" % (row[0], row[1])


def take_baseline(root, out_path):
    inv = Path(root) / "infra" / "aws" / "lambda" / "investor-reporting"
    listed = {rel: [str(p.relative_to(inv)).replace(os.sep, "/") for p in folder_files(inv, rel)] for rel in FOLDERS}
    rows_by, errors_by = run_all(inv)
    rows = [r for label in rows_by for r in rows_by[label] if label != CROSS_REL]
    failing = sorted(set(failing_key(r) for r in rows if r[2] == "fail"))
    doc = {"method": "tests_check.py --take-baseline, one pytest process per folder over a clean worktree",
           "root_worktree": str(root), "base_commit": subprocess.run(
               ["git", "-C", str(root), "rev-parse", "HEAD"], stdout=subprocess.PIPE,
               stderr=subprocess.PIPE, timeout=60).stdout.decode("ascii", "replace").strip(),
           "files": listed,
           "counts": {"passed": sum(1 for r in rows if r[2] == "pass"),
                      "failed": sum(1 for r in rows if r[2] == "fail"),
                      "skipped": sum(1 for r in rows if r[2] == "skip"),
                      "collect_errors": sum(errors_by.values())},
           "failing": failing}
    Path(out_path).write_text(json.dumps(doc, indent=2) + "\n", encoding="ascii")
    print("BASELINE written: %s" % out_path)
    print("counts: %s" % json.dumps(doc["counts"]))
    print("failing names (%d):" % len(failing))
    for name in failing:
        print("  " + name)
    return 0


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--take-baseline":
        return take_baseline(sys.argv[2], sys.argv[3])
    inv = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
    print("LISTED FILES:")
    for label, files in groups(inv):
        print("  [%s] %d file(s)" % (label, len(files)))
        for path in files:
            print("    " + str(path.relative_to(inv)).replace(os.sep, "/"))
    if not BASELINE.is_file():
        print("TESTS-BAD no baseline file at %s" % BASELINE)
        return 1
    baseline = set(json.loads(BASELINE.read_text(encoding="ascii"))["failing"])
    try:
        rows_by, errors_by = run_all(inv)
    except RuntimeError as exc:
        print("TESTS-BAD %s" % exc)
        return 1
    if sum(errors_by.values()):
        print("TESTS-BAD %d collection error(s) in the listed files" % sum(errors_by.values()))
        return 1
    new_rows = [r for r in rows_by.get(FOLDERS[0], []) if r[0].endswith(Path(NEW_REL).stem)]
    cross_rows = rows_by.get(CROSS_REL, [])
    new_rows_all = new_rows
    other_rows = [r for label in rows_by for r in rows_by[label]
                  if label != CROSS_REL and not r[0].endswith(Path(NEW_REL).stem)]
    # Case (a) to (f) and (g1), (g2): each named case must be present and pass.
    missing = []
    for label, name in sorted(NEW_CASES.items()):
        pool = cross_rows if label.startswith("(g") else new_rows
        hits = [r for r in pool if r[1] == name or r[1].startswith(name + "[")]
        if not hits or any(r[2] != "pass" for r in hits):
            missing.append("%s %s" % (label, name))
    if missing:
        print("TESTS-BAD cases not passing: " + "; ".join(missing))
        return 1
    not_passing = [r for r in new_rows_all + cross_rows if r[2] != "pass"]
    if not_passing:
        print("TESTS-BAD %d case(s) of the new files do not pass: %s"
              % (len(not_passing), "; ".join(failing_key(r) for r in not_passing)))
        return 1
    failing_other = set(failing_key(r) for r in other_rows if r[2] == "fail")
    new_failures = sorted(failing_other - baseline)
    unchanged = len(failing_other & baseline)
    fixed = len(baseline - failing_other)
    new_passed = sum(1 for r in new_rows_all + cross_rows if r[2] == "pass")
    other_passed = sum(1 for r in other_rows if r[2] == "pass")
    print("new files: %d passed (route file %d, cross-check %d); others: %d passed, %d skipped, %d failing, "
          "%d baseline failure(s) no longer failing"
          % (new_passed, len(new_rows_all), len(cross_rows), other_passed,
             sum(1 for r in other_rows if r[2] == "skip"), len(failing_other), fixed))
    if new_failures:
        print("TESTS-BAD %d failing case(s) not in the baseline: %s" % (len(new_failures), "; ".join(new_failures)))
        return 1
    if new_passed == 0 or other_passed == 0:
        print("TESTS-BAD an empty denominator (new=%d others=%d)" % (new_passed, other_passed))
        return 1
    print("TESTS-OK %d new, %d others, %d baseline failures unchanged, 0 new failures"
          % (new_passed, other_passed, unchanged))
    return 0


if __name__ == "__main__":
    sys.exit(main())
