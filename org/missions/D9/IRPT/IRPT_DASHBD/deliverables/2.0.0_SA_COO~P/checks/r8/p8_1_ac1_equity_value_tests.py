"""DB8-1-AC1 -- CTO batch 193: C-VALUE is the account's EQUITY, net_mv_plus_cash + margin_balance, one rule for every account, a new
method_version.

Runs data/assets/scripts/gold/irpt_reporting/tests/test_account_equity_value.py (bounded at 110 s). Grades: the file names "equity",
"margin_balance" and "method_version"; at least 4 tests pass, 0 failed or errored. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_equity_value.py"


def fail(msg):
    print("FAIL: " + msg)
    print("DB8-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("equity", "margin_balance", "method_version"):
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
    if not passed or int(passed.group(1)) < 4:
        fail("fewer than 4 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed" % passed.group(0))
    print("DB8-1-AC1 PASS")


if __name__ == "__main__":
    main()
