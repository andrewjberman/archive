"""IB32-1-AC2 -- client_id is still refused on every other issued owner read, one negative arm per operation, through served.Entry.

The other owner reads are the ones infra/aws/lambda/investor-reporting/ops/entry.py configures besides the history:
analysis-request-read, analysis-report, status-job (owner_read_modes, ops/entry.py:216-218). Runs
infra/aws/lambda/investor-reporting/_authz/tests/test_owner_read_client_refused.py (bounded at 110 s). Grades: the file names each of
the three operations and "client_id"; at least 3 tests pass, 0 failed or errored. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/_authz/tests/test_owner_read_client_refused.py"
OTHERS = ("analysis-request-read", "analysis-report", "status-job")


def fail(msg):
    print("FAIL: " + msg)
    print("IB32-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in OTHERS + ("client_id",):
        if word not in src:
            fail("the test file never names %r" % word)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < 3:
        fail("fewer than 3 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed; arms for %s" % (passed.group(0), ", ".join(OTHERS)))
    print("IB32-1-AC2 PASS")


if __name__ == "__main__":
    main()
