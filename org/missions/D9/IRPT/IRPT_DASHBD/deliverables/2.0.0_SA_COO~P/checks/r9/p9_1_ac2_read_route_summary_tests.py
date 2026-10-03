"""DB9-1-AC2 -- CTO batch 197 (b): the read route serves a client's summary ONLY when the scope enforcer covers every account the
summary names; partial coverage and another firm's client are refused.

Runs the read route's whole suite, infra/aws/lambda/investor-reporting/reporting/tests (bounded at 110 s). Grades:
  - tests/test_reporting_summary.py exists and names "summary", "OBJECT_NOT_COVERED", "partial" and "firm";
  - 0 failed or errored across the suite;
  - at least 14 tests pass (11 at the base, 2026-10-03, plus the three arms the ruling names).
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

SUITE = "infra/aws/lambda/investor-reporting/reporting/tests"
NEW = SUITE + "/test_reporting_summary.py"
FLOOR = 14


def fail(msg):
    print("FAIL: " + msg)
    print("DB9-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / NEW
    if not t.is_file():
        fail("no test file at %s" % NEW)
    src = t.read_text(encoding="utf-8")
    for word in ("summary", "OBJECT_NOT_COVERED", "partial", "firm"):
        if word not in src:
            fail("the summary tests never name %r" % word)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", SUITE],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < FLOOR:
        fail("fewer than %d tests passed: %s" % (FLOOR, passed.group(0) if passed else out.strip()[-200:]))
    print("OK: read route suite %s, 0 failed" % passed.group(0))
    print("DB9-1-AC2 PASS")


if __name__ == "__main__":
    main()
