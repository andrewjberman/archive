"""R18P2-AC1 -- runs the new trade-form upload test file and the whole TicketCenter test folder in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when the new file passes every named case and the
folder has 0 failed and 0 errors. Otherwise prints PORTAL-TESTS-BAD <why> and exits 1.
"""
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-tckt-vnext-42/portal"
NEW_FILE = "src/pages/TicketCenter/__tests__/trade-form-upload.test.tsx"
FOLDER = "src/pages/TicketCenter"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run_bun(target):
    bun = shutil.which("bun") or "bun"
    proc = subprocess.run([bun, "test", target], cwd=PORTAL, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=100)
    return proc.returncode, ANSI.sub("", (proc.stdout or "") + (proc.stderr or ""))


def count(out, label):
    found = re.findall(r"^\s*(\d+) %s\s*$" % label, out, re.M)
    return int(found[-1]) if found else None


def named_cases(path):
    with open(PORTAL + "/" + path, encoding="utf-8") as fh:
        return len(re.findall(r"^\s*test\(", fh.read(), re.M))


def bad(why):
    print("PORTAL-TESTS-BAD " + why)
    sys.exit(1)


def main():
    expected = named_cases(NEW_FILE)
    if expected == 0:
        bad("the new file names no test case")
    rc_new, out_new = run_bun(NEW_FILE)
    pass_new, fail_new, err_new = count(out_new, "pass"), count(out_new, "fail"), count(out_new, "error") or 0
    if pass_new is None or fail_new is None:
        bad("the new file's summary was not read (rc=%s)" % rc_new)
    if rc_new != 0 or fail_new != 0 or err_new != 0 or pass_new != expected:
        bad("new file: rc=%s pass=%s of %s fail=%s error=%s" % (rc_new, pass_new, expected, fail_new, err_new))
    rc_f, out_f = run_bun(FOLDER)
    pass_f, fail_f, err_f = count(out_f, "pass"), count(out_f, "fail"), count(out_f, "error") or 0
    if pass_f is None or fail_f is None:
        bad("the folder summary was not read (rc=%s)" % rc_f)
    if rc_f != 0 or fail_f != 0 or err_f != 0:
        bad("folder: rc=%s pass=%s fail=%s error=%s" % (rc_f, pass_f, fail_f, err_f))
    print("PORTAL-TESTS-OK %d new, %d folder, 0 failed" % (pass_new, pass_f))
    sys.exit(0)


if __name__ == "__main__":
    main()
