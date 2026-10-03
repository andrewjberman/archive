"""Round 38 (IRPT_BCKEND ~P, CTO batch 207) -- the gap's claim is "inferred", never a fifth value.

CLAUDE.md "A VALUE MUST CARRY ITS CLAIM": the vocabulary is measured / inferred / held / absent. Batch 207 re-cuts IB-pr-299's
claim "partial" to "inferred"; the PARTIAL absence naming the days stays.

Usage: python <this file> <repo_root> <criterion_id>
  IB38-1-AC1  infra/aws/lambda/investor-reporting/performance/holdings_gold.py, imported: every module constant named CLAIM_*
              is in {measured, inferred, held, absent}, one of them is "inferred", and the module source has no claim literal
              "partial" (the normalize.PARTIAL absence class is not a claim and is allowed); then the gap test file
              (performance/tests/test_holdings_gold_calendar_gap.py) names "inferred", never asserts a claim of "partial", and
              at least 7 of its tests pass, 0 failed.
  IB38-1-AC2  the whole performance suite: at least 246 pass, 0 failed (bounded at 110 s).
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

P = "infra/aws/lambda/investor-reporting/performance/"
VOCAB = {"measured", "inferred", "held", "absent"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB38"))
        sys.exit(1)

    def pytest(target, floor):
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                               cwd=str(root), capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("pytest exceeded 110 s on %s" % target)
        out = (r.stdout or "") + (r.stderr or "")
        bad = re.search(r"(\d+) (failed|error)", out)
        passed = re.search(r"(\d+) passed", out)
        if bad or not passed or int(passed.group(1)) < floor:
            fail("%s: %s (floor %d)" % (target, bad.group(0) if bad else (passed.group(0) if passed else out[-200:]), floor))
        return int(passed.group(1))

    if cid == "IB38-1-AC1":
        sys.path[:0] = [str(root / P), str(root), str(root / "lib")]
        import holdings_gold as hg  # noqa: E402
        claims = {k: getattr(hg, k) for k in dir(hg) if k.startswith("CLAIM_")}
        if not claims or not set(claims.values()) <= VOCAB or "inferred" not in claims.values():
            fail("claim constants %s are not inside %s with 'inferred' among them" % (claims, sorted(VOCAB)))
        src = (root / (P + "holdings_gold.py")).read_text(encoding="utf-8")
        if re.search(r'["\']partial["\']', src):
            fail("holdings_gold.py still carries a 'partial' literal")
        t = (root / (P + "tests/test_holdings_gold_calendar_gap.py")).read_text(encoding="utf-8")
        if "inferred" not in t:
            fail("the gap tests never name 'inferred'")
        if re.search(r'claim"\]\s*==\s*"partial"', t):
            fail("the gap tests still assert a claim of 'partial'")
        n = pytest(P + "tests/test_holdings_gold_calendar_gap.py", 7)
        print("OK: claims %s; gap tests %d passed" % (sorted(set(claims.values())), n))
    elif cid == "IB38-1-AC2":
        n = pytest(P + "tests", 246)
        print("OK: performance suite %d passed, 0 failed" % n)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
