#!/usr/bin/env python3
"""AR325-y-AC1 -- the new test file and the whole TicketCenter folder, run under bun test in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when every named case (a) to (f) of the
new file passes and the folder run has 0 failed. Otherwise prints PORTAL-TESTS-BAD <why> and exits 1.
Reads bun's JUnit report (bun test --reporter=junit), never its colour output. Read-only: runs tests, writes nothing
into the product tree (the report goes to the worker's .scratch).
"""
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

PORTAL = "C:/dev/wk-irpt-anlreq-133/portal"
SCRATCH = "C:/dev/wk-irpt-anlreq-133/.scratch"
NEW_FILE = "src/pages/TicketCenter/__tests__/internal-filer-chooses-firm.test.ts"
FOLDER = "src/pages/TicketCenter"
# One substring per named case of the new file; each must name a passing testcase.
CASES = [
    "(a) an Opal staff filer chooses the firm",
    "(b) a partner user files under exactly the firm it did before",
    "(c) the submit of an Opal staff filer is held",
    "(d) a staff filing posts the chosen firm",
    "(e) the Firm line is a control of the served firms",
    "an Opal staff filer chooses the firm; a partner user's firm is never a choice",
]


def run_junit(bun, targets, label):
    os.makedirs(SCRATCH, exist_ok=True)
    out = os.path.join(SCRATCH, "portal_check_%s.xml" % label)
    if os.path.exists(out):
        os.remove(out)
    cmd = [bun, "test", *targets, "--reporter=junit", "--reporter-outfile=" + out]
    proc = subprocess.run(cmd, cwd=PORTAL, capture_output=True, text=True, timeout=280)
    if not os.path.exists(out):
        return proc.returncode, None
    cases = []
    for tc in ET.parse(out).iter("testcase"):
        failed = any(ch.tag in ("failure", "error") for ch in tc)
        cases.append((tc.get("name", ""), failed))
    return proc.returncode, cases


def main():
    bun = shutil.which("bun")
    if not bun:
        print("PORTAL-TESTS-BAD bun is not on PATH")
        return 1
    if not os.path.isdir(os.path.join(PORTAL, "src", "pages", "TicketCenter")):
        print("PORTAL-TESTS-BAD the portal worktree does not carry src/pages/TicketCenter: %s" % PORTAL)
        return 1
    rc_new, new_cases = run_junit(bun, [NEW_FILE], "new")
    if new_cases is None:
        print("PORTAL-TESTS-BAD bun wrote no report for the new file (rc=%s)" % rc_new)
        return 1
    missing = [c for c in CASES if not any(c in name for name, _ in new_cases)]
    if missing:
        print("PORTAL-TESTS-BAD named case(s) absent from the new file: %s" % "; ".join(missing))
        return 1
    not_passing = [name for name, failed in new_cases if failed]
    if not_passing:
        print("PORTAL-TESTS-BAD new-file case(s) failing: %s" % "; ".join(not_passing))
        return 1
    new_passed = sum(1 for _, failed in new_cases if not failed)

    rc_fold, fold_cases = run_junit(bun, [FOLDER], "folder")
    if fold_cases is None:
        print("PORTAL-TESTS-BAD bun wrote no report for the folder (rc=%s)" % rc_fold)
        return 1
    folder_failed = [name for name, failed in fold_cases if failed]
    if folder_failed:
        print("PORTAL-TESTS-BAD folder has %d failing case(s): %s" % (len(folder_failed), "; ".join(folder_failed[:5])))
        return 1
    folder_passed = sum(1 for _, failed in fold_cases if not failed)
    if rc_fold != 0 or rc_new != 0:
        print("PORTAL-TESTS-BAD bun exit codes new=%s folder=%s with no failing testcase" % (rc_new, rc_fold))
        return 1
    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (new_passed, folder_passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
