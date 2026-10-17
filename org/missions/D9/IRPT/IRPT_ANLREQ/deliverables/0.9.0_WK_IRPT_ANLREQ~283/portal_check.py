"""AR383-y-AC1: run bun test on the new test file and on src/pages/TicketCenter (portal worktree).

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when every new case passes and the
folder has 0 failed; otherwise PORTAL-TESTS-BAD <why>, exit 1.
"""
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-283/portal"
NEW_FILE = "src/pages/TicketCenter/__tests__/report-ref-revision-string.test.tsx"
FOLDER = "src/pages/TicketCenter"
TIMEOUT = 120

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
PASS_RE = re.compile(r"^\s*(\d+) pass\s*$", re.M)
FAIL_RE = re.compile(r"^\s*(\d+) fail\s*$", re.M)


def bun_path():
    found = shutil.which("bun")
    if not found:
        return None
    return found


def run_bun(target):
    exe = bun_path()
    if exe is None:
        return None, "bun not on PATH"
    try:
        proc = subprocess.run(
            [exe, "test", target], cwd=PORTAL, capture_output=True, timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None, "bun test %s timed out after %ss (rc 124)" % (target, TIMEOUT)
    text = ANSI.sub("", (proc.stdout + proc.stderr).decode("utf-8", errors="replace"))
    passes = PASS_RE.findall(text)
    fails = FAIL_RE.findall(text)
    if not passes or not fails:
        return None, "bun test %s printed no pass/fail summary (rc %s)" % (target, proc.returncode)
    return {"rc": proc.returncode, "pass": int(passes[-1]), "fail": int(fails[-1])}, None


def main():
    new, why = run_bun(NEW_FILE)
    if why:
        print("PORTAL-TESTS-BAD %s" % why)
        return 1
    if new["rc"] != 0 or new["fail"] != 0:
        print("PORTAL-TESTS-BAD new file rc=%s fail=%s pass=%s" % (new["rc"], new["fail"], new["pass"]))
        return 1
    if new["pass"] < 1:
        print("PORTAL-TESTS-BAD new file ran no passing case")
        return 1
    folder, why = run_bun(FOLDER)
    if why:
        print("PORTAL-TESTS-BAD %s" % why)
        return 1
    if folder["rc"] != 0 or folder["fail"] != 0:
        print("PORTAL-TESTS-BAD folder rc=%s fail=%s pass=%s" % (folder["rc"], folder["fail"], folder["pass"]))
        return 1
    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (new["pass"], folder["pass"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
