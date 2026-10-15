"""AR-y-354 criterion AR354-y-AC1: run the Keep test file and the whole TicketCenter folder in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when every case of the keep file passes
(the file declares NEW_CASES tests, all passing, none failing) and the folder has 0 failed. Otherwise PORTAL-TESTS-BAD <why>, exit 1.
ASCII output only.
"""
import os
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-154/portal"
KEEP_FILE = "src/pages/TicketCenter/__tests__/filing-hint-keep.test.tsx"
FOLDER = "src/pages/TicketCenter"
NEW_CASES = 7  # cases (a) to (g) of the cell, one test() each
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def bun_path():
    found = shutil.which("bun")
    if found:
        return found
    fallback = ("C:/Users/Test/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_Microsoft.Winget.Source_8wekyb3d8bbwe/"
                "bun-windows-x64/bun.exe")
    return fallback if os.path.exists(fallback) else None


def run_tests(bun, target):
    proc = subprocess.run([bun, "test", target], cwd=PORTAL, capture_output=True, text=True, timeout=300)
    text = ANSI.sub("", proc.stdout + proc.stderr)
    passed = [int(m) for m in re.findall(r"^\s*(\d+) pass\s*$", text, re.M)]
    failed = [int(m) for m in re.findall(r"^\s*(\d+) fail\s*$", text, re.M)]
    return proc.returncode, (passed[-1] if passed else None), (failed[-1] if failed else None), text


def bad(why):
    print("PORTAL-TESTS-BAD " + why)
    sys.exit(1)


def main():
    bun = bun_path()
    if bun is None:
        bad("bun not found on PATH or at the WinGet path")
    with open(os.path.join(PORTAL, KEEP_FILE), encoding="utf-8") as fh:
        declared = len(re.findall(r"^\s*test\(", fh.read(), re.M))
    if declared != NEW_CASES:
        bad("keep file declares %d test cases, expected %d" % (declared, NEW_CASES))

    rc_new, new_pass, new_fail, new_text = run_tests(bun, KEEP_FILE)
    if new_pass is None or new_fail is None:
        bad("keep file: could not parse the bun test counts")
    if rc_new != 0 or new_fail != 0 or new_pass != NEW_CASES:
        bad("keep file: rc=%d pass=%s fail=%s, need pass=%d fail=0" % (rc_new, new_pass, new_fail, NEW_CASES))

    rc_folder, folder_pass, folder_fail, folder_text = run_tests(bun, FOLDER)
    if folder_pass is None or folder_fail is None:
        bad("folder: could not parse the bun test counts")
    if rc_folder != 0 or folder_fail != 0:
        bad("folder: rc=%d pass=%s fail=%s" % (rc_folder, folder_pass, folder_fail))

    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (new_pass, folder_pass))
    sys.exit(0)


if __name__ == "__main__":
    main()
