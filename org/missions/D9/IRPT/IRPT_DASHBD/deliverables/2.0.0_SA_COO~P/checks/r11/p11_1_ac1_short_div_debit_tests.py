"""DB11-1-AC1 -- PRD v0.7 ruling 27 (row IRPT_DASHBD-W1-S17): a DIV debit on a short position is income, admitted only when the
declared dividend_interest_share_quantity is negative.

Runs the whole data/assets/scripts/gold/irpt_reporting/tests suite (bounded at 110 s). Grades: tests/test_short_div_debit.py
exists and names "DIV", "share_quantity" and "short"; 0 failed or errored across the suite; at least 17 pass (14 at the base,
2026-10-03, plus at least 3 new). Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

SUITE = "data/assets/scripts/gold/irpt_reporting/tests"
NEW = SUITE + "/test_short_div_debit.py"
FLOOR = 17


def fail(msg):
    print("FAIL: " + msg)
    print("DB11-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / NEW
    if not t.is_file():
        fail("no test file at %s" % NEW)
    src = t.read_text(encoding="utf-8")
    for word in ("DIV", "share_quantity", "short"):
        if word not in src:
            fail("the test file never names %r" % word)
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
    print("OK: irpt_reporting suite %s, 0 failed" % passed.group(0))
    print("DB11-1-AC1 PASS")


if __name__ == "__main__":
    main()
