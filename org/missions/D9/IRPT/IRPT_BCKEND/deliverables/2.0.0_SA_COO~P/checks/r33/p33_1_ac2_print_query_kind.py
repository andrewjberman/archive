"""IB33-1-AC2 -- print_query takes the resolved kind (row W101-S9): an ANALYSIS record prints as analysis even when it carries a
stray dates dict, and a PERFORMANCE print query is unchanged.

Runs infra/aws/lambda/investor-reporting/export/tests/test_print_query_kind.py (bounded at 110 s). Grades: the file names "ANALYSIS",
"PERFORMANCE" and "dates"; at least 2 tests pass, 0 failed or errored. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/export/tests/test_print_query_kind.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB33-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("ANALYSIS", "PERFORMANCE", "dates"):
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
    if not passed or int(passed.group(1)) < 2:
        fail("fewer than 2 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed" % passed.group(0))
    print("IB33-1-AC2 PASS")


if __name__ == "__main__":
    main()
