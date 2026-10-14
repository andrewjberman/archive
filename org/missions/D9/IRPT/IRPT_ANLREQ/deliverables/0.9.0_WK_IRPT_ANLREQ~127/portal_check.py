"""AR317-y-AC1 -- portal tests for TO-AR-y-317 (worker 0.9.0_WK_IRPT_ANLREQ~127).

Runs `bun test` on the new test file and on the whole src/pages/TicketCenter folder in the portal worktree, parses the
counts, and prints PORTAL-TESTS-OK only when the new file has every case (a) to (g) passing and the folder has 0 failed.
Otherwise prints PORTAL-TESTS-BAD <why> and exits 1.
"""
import os
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-127/portal"
NEW_TEST = "src/pages/TicketCenter/__tests__/analysis-commentary-always-requested.test.ts"
FOLDER = "src/pages/TicketCenter"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
LABELS = set("abcdefg")


def run_bun(target):
    bun = shutil.which("bun")
    if bun is None:
        return None, "bun is not on PATH"
    try:
        proc = subprocess.run([bun, "test", target], cwd=PORTAL, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, "bun test timed out after 120 seconds on " + target
    text = ANSI.sub("", (proc.stdout + proc.stderr).decode("utf-8", errors="replace"))
    return (proc.returncode, text), None


def counts(text):
    p = re.findall(r"^\s*(\d+) pass\s*$", text, re.M)
    f = re.findall(r"^\s*(\d+) fail\s*$", text, re.M)
    if not p or not f:
        return None
    return int(p[-1]), int(f[-1])


def main():
    if not os.path.isfile(os.path.join(PORTAL, NEW_TEST)):
        print("PORTAL-TESTS-BAD new test file is missing: " + NEW_TEST)
        return 1
    with open(os.path.join(PORTAL, NEW_TEST), encoding="utf-8") as fh:
        src = fh.read()
    declared = len(re.findall(r"^\s*test\(", src, re.M))
    labels = set(re.findall(r"test\('\(([a-z])\)", src))
    if labels != LABELS:
        print("PORTAL-TESTS-BAD the new file does not name cases (a) to (g): found " + ",".join(sorted(labels)))
        return 1

    new_run, err = run_bun(NEW_TEST)
    if err:
        print("PORTAL-TESTS-BAD " + err)
        return 1
    rc, text = new_run
    c = counts(text)
    if c is None:
        print("PORTAL-TESTS-BAD could not parse the new-file summary (rc=%d)" % rc)
        return 1
    new_pass, new_fail = c
    if rc != 0 or new_fail != 0 or new_pass != declared:
        print("PORTAL-TESTS-BAD new file rc=%d pass=%d fail=%d declared=%d" % (rc, new_pass, new_fail, declared))
        return 1

    folder_run, err = run_bun(FOLDER)
    if err:
        print("PORTAL-TESTS-BAD " + err)
        return 1
    frc, ftext = folder_run
    fc = counts(ftext)
    if fc is None:
        print("PORTAL-TESTS-BAD could not parse the folder summary (rc=%d)" % frc)
        return 1
    folder_pass, folder_fail = fc
    if frc != 0 or folder_fail != 0:
        print("PORTAL-TESTS-BAD folder rc=%d pass=%d fail=%d" % (frc, folder_pass, folder_fail))
        return 1

    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (new_pass, folder_pass))
    return 0


if __name__ == "__main__":
    sys.exit(main())
