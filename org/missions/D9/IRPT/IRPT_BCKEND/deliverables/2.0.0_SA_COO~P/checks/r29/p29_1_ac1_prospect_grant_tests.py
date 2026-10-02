"""IB29-1-AC1 -- a render grant for a prospect-owned report names exactly the report's own artifacts, and nothing else.

Runs infra/aws/lambda/investor-reporting/_render_identity/tests/test_grant_prospect.py with pytest (bounded at 110 s) and grades:
the file exists and names both branches ("prospect" and "account"); at least 5 tests passed, 0 failed or errored.
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/_render_identity/tests/test_grant_prospect.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8").lower()
    for word in ("prospect", "account"):
        if word not in src:
            fail("the test file never names %r" % word)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < 5:
        fail("fewer than 5 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed" % passed.group(0))
    print("IB29-1-AC1 PASS")


if __name__ == "__main__":
    main()
