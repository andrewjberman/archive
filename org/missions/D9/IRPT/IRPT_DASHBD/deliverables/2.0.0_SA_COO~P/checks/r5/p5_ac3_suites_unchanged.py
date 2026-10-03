"""DB5-AC3 -- the reporting gold and publisher are served: their existing suites pass unchanged (shared by DB-b-11 and DB-b-12).

Runs each suite in its OWN pytest process, bounded at 110 s. Baselines: at CLOUD 2026-10-02 ~18:2xZ reporting-gold/tests 9 passed and
reporting-publish/tests 13; RAISED by the issuer at the DB-b-14 drain (@f26fa5fb4d, 2026-10-03) to 24 and 25, the counts every suite
passes there, so a deleted test cannot hide under a stale floor (DB-b-14's worker report). Grades: 0 failed or errored, and at least
the baseline count passing. Base: PASS (a regression guard). Usage: python <this file> <repo_root> [criterion id]
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
SUITES = ((B + "reporting-gold/tests", 24), (B + "reporting-publish/tests", 25))


def fail(msg, cid):
    print("FAIL: " + msg)
    print("%s FAIL" % cid)
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else "DB5-AC3"
    lines = []
    for suite, floor in SUITES:
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", suite],
                               cwd=str(root), capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("%s exceeded 110 s" % suite, cid)
        out = (r.stdout or "") + (r.stderr or "")
        bad = re.search(r"(\d+) (failed|error)", out)
        passed = re.search(r"(\d+) passed", out)
        if bad:
            fail("%s: %s" % (suite, bad.group(0)), cid)
        n = int(passed.group(1)) if passed else 0
        if n < floor:
            fail("%s passed %d, below its baseline %d" % (suite, n, floor), cid)
        lines.append("%s %d passed" % (suite.split("/")[-2], n))
    print("OK: " + "; ".join(lines))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
