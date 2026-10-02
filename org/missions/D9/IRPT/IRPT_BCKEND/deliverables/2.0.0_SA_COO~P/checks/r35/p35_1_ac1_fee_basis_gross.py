"""IB35-1-AC1 -- P-4 (CTO batch 178, row IRPT_BCKEND-S275): the holdings-gold Performance path says its figure is GROSS of fees.

Grades:
  1. infra/aws/lambda/investor-reporting/performance/holdings_gold.py assigns result.fee_basis "GROSS", and no line that assigns
     result.fee_basis carries "NET".
  2. infra/aws/lambda/investor-reporting/performance/tests/test_holdings_gold_fee_basis.py names "GROSS" and "fee_basis"; at least 2
     tests pass, 0 failed or errored (bounded at 110 s).
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

P = "infra/aws/lambda/investor-reporting/performance/"
TEST = P + "tests/test_holdings_gold_fee_basis.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB35-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    src = (root / P / "holdings_gold.py").read_text(encoding="utf-8").splitlines()
    lines = [ln for ln in src if "fee_basis" in ln and "=" in ln and "result" in ln]
    if not lines:
        fail("holdings_gold.py assigns no result.fee_basis")
    if any('"NET"' in ln for ln in lines):
        fail("holdings_gold.py still assigns NET: %s" % [ln.strip() for ln in lines if '"NET"' in ln][:1])
    if not any('"GROSS"' in ln for ln in lines):
        fail("holdings_gold.py does not assign GROSS")
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    tsrc = t.read_text(encoding="utf-8")
    for word in ("GROSS", "fee_basis"):
        if word not in tsrc:
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
    print("OK: holdings_gold.py assigns GROSS; %s, 0 failed" % passed.group(0))
    print("IB35-1-AC1 PASS")


if __name__ == "__main__":
    main()
