"""IB31-1-AC1 -- (a) serve_submit for an ANALYSIS request builds no narrative packet and stamps the report's own as-of, never
dates.actual_end; a client (PERFORMANCE) request's path is unchanged.

Runs infra/aws/lambda/investor-reporting/export/tests/test_serve_submit_analysis.py (bounded at 110 s), then the WHOLE export/tests
folder in its own process (bounded at 110 s). Grades: the new file names "analysis", "narrative" and "actual_end"; at least 3 of its
tests pass, 0 failed or errored; the whole export/tests folder fails 0 (139 passed at the base). Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/export/tests/"
TEST = B + "test_serve_submit_analysis.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB31-1-AC1 FAIL")
    sys.exit(1)


def pytest(root, target):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s on %s" % target)
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("%s: %s" % (target, bad.group(0)))
    return int(passed.group(1)) if passed else 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8").lower()
    for word in ("analysis", "narrative", "actual_end"):
        if word not in src:
            fail("the test file never names %r" % word)
    n = pytest(root, TEST)
    if n < 3:
        fail("fewer than 3 tests passed in the new file (%d)" % n)
    total = pytest(root, B)
    print("OK: new file %d passed; export/tests %d passed, 0 failed" % (n, total))
    print("IB31-1-AC1 PASS")


if __name__ == "__main__":
    main()
