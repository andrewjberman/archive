"""AR365-y-AC1 -- run the new notice test file and the TicketCenter folder under bun test, in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when every new case (a)-(f) passes and the folder has
0 failed; otherwise PORTAL-TESTS-BAD <why>, exit 1.
"""
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-162/portal"
NEW_FILE = "src/pages/TicketCenter/__tests__/filing-notice.test.tsx"
FOLDER = "src/pages/TicketCenter"
NEW_CASES = 6
TIMEOUT_S = 480

ANSI = re.compile(r"\x1b\[[0-9;]*m")
SUMMARY = re.compile(r"^\s*(\d+)\s+(pass|fail)\s*$")
RAN = re.compile(r"Ran (\d+) tests? across (\d+) files?")


def bad(why):
    print("PORTAL-TESTS-BAD " + why)
    sys.exit(1)


def run_bun(target):
    bun = shutil.which("bun")
    if bun is None:
        bad("bun is not on PATH")
    try:
        p = subprocess.run([bun, "test", target], cwd=PORTAL, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        bad("timeout after %d s on %s" % (TIMEOUT_S, target))
    text = ANSI.sub("", p.stdout + p.stderr)
    passed = failed = None
    for line in text.splitlines():
        m = SUMMARY.match(line)
        if m:
            if m.group(2) == "pass":
                passed = int(m.group(1))
            else:
                failed = int(m.group(1))
    ran = RAN.search(text)
    return {
        "rc": p.returncode, "pass": passed, "fail": failed,
        "ran": int(ran.group(1)) if ran else None, "text": text,
    }


def main():
    with open(PORTAL + "/" + NEW_FILE, "r", encoding="utf-8") as fh:
        cases = len(re.findall(r"^\s*test\('\([a-f]\)", fh.read(), flags=re.MULTILINE))
    if cases != NEW_CASES:
        bad("new file carries %d lettered cases (a)-(f), expected %d" % (cases, NEW_CASES))

    new = run_bun(NEW_FILE)
    if new["rc"] != 0 or new["fail"] != 0 or new["pass"] is None:
        bad("new file rc=%s pass=%s fail=%s" % (new["rc"], new["pass"], new["fail"]))
    if new["ran"] != NEW_CASES or new["pass"] != NEW_CASES:
        bad("new file ran %s, passed %s; every case (a)-(f) must pass" % (new["ran"], new["pass"]))

    folder = run_bun(FOLDER)
    if folder["rc"] != 0 or folder["fail"] != 0 or folder["pass"] is None:
        bad("folder %s rc=%s pass=%s fail=%s" % (FOLDER, folder["rc"], folder["pass"], folder["fail"]))

    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (new["pass"], folder["pass"]))
    sys.exit(0)


if __name__ == "__main__":
    main()
