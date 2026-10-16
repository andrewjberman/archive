#!/usr/bin/env python3
"""AR-y-378 AC1: run the new test file and the TicketCenter folder in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when the new file passes all of its
seven cases with 0 failures and the folder has 0 failed; otherwise PORTAL-TESTS-BAD <why> and exit 1.
"""
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-170/portal"
NEW_FILE = "src/pages/TicketCenter/__tests__/advisor-email.test.tsx"
FOLDER = "src/pages/TicketCenter"
NEW_CASES = 7
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run(target):
    binary = shutil.which("bun") or "bun"
    proc = subprocess.run([binary, "test", target], cwd=PORTAL, capture_output=True, text=True, timeout=300)
    out = ANSI.sub("", (proc.stdout or "") + (proc.stderr or ""))
    passed = re.findall(r"^\s*(\d+) pass\s*$", out, re.M)
    failed = re.findall(r"^\s*(\d+) fail\s*$", out, re.M)
    return proc.returncode, (int(passed[-1]) if passed else None), (int(failed[-1]) if failed else None), out


def main():
    try:
        rc_new, pass_new, fail_new, _ = run(NEW_FILE)
        rc_dir, pass_dir, fail_dir, _ = run(FOLDER)
    except subprocess.TimeoutExpired:
        print("PORTAL-TESTS-BAD bun test timed out (300 s)")
        return 1
    if pass_new is None or fail_new is None:
        print("PORTAL-TESTS-BAD the new file printed no pass/fail summary (rc=%s)" % rc_new)
        return 1
    if rc_new != 0 or fail_new != 0 or pass_new != NEW_CASES:
        print("PORTAL-TESTS-BAD new file: rc=%s pass=%s fail=%s, expected %d pass 0 fail" % (rc_new, pass_new, fail_new, NEW_CASES))
        return 1
    if pass_dir is None or fail_dir is None:
        print("PORTAL-TESTS-BAD the folder printed no pass/fail summary (rc=%s)" % rc_dir)
        return 1
    if rc_dir != 0 or fail_dir != 0:
        print("PORTAL-TESTS-BAD folder %s: rc=%s fail=%s" % (FOLDER, rc_dir, fail_dir))
        return 1
    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (pass_new, pass_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
