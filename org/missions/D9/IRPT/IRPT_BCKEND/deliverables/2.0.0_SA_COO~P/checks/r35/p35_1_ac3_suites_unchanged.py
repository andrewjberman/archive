"""IB35-1-AC3 -- the performance adapter and the build tooling are shared: their suites pass unchanged.

Runs each in its OWN pytest process, bounded at 110 s, with --color=no -rf. Baselines at CLOUD 2026-10-02 ~17:3xZ: performance/tests 237
passed, export/tests 168 passed, infra/aws/lambda/ci/test_render_ports_packaging.py 3 passed, 0 failed each. Grades: 0 failed or
errored in each, and at least the baseline count passing. Base: PASS (a regression guard). Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
SUITES = ((B + "performance/tests", 237), (B + "export/tests", 168), ("infra/aws/lambda/ci/test_render_ports_packaging.py", 3))


def fail(msg):
    print("FAIL: " + msg)
    print("IB35-1-AC3 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    lines = []
    for suite, floor in SUITES:
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", suite],
                               cwd=str(root), capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            fail("%s exceeded 110 s" % suite)
        out = (r.stdout or "") + (r.stderr or "")
        bad = re.search(r"(\d+) (failed|error)", out)
        passed = re.search(r"(\d+) passed", out)
        if bad:
            fail("%s: %s" % (suite, bad.group(0)))
        n = int(passed.group(1)) if passed else 0
        if n < floor:
            fail("%s passed %d, below its baseline %d" % (suite, n, floor))
        lines.append("%s %d passed" % (suite.split("/")[-1] if suite.endswith(".py") else suite.split("/")[-2], n))
    print("OK: " + "; ".join(lines))
    print("IB35-1-AC3 PASS")


if __name__ == "__main__":
    main()
