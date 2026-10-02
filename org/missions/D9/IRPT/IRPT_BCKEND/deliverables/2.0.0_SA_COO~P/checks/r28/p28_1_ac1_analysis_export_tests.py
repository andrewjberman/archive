"""IB28-1-AC1 -- the retained-export path admits a retained ANALYSIS report and still refuses what it refused.

Runs the worker's test file infra/aws/lambda/investor-reporting/export/tests/test_retained_export_analysis.py with pytest (bounded
at 110 s) and grades: the file exists and names both report kinds (ANALYSIS and PERFORMANCE, so the Performance arm is re-proved
beside the new one); at least 5 tests passed and 0 failed or errored. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/export/tests/test_retained_export_analysis.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB28-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for kind in ("ANALYSIS", "PERFORMANCE"):
        if kind not in src:
            fail("the test file never names %s" % kind)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    passed = re.search(r"(\d+) passed", out)
    bad = re.search(r"(\d+) (failed|error)", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < 5:
        fail("fewer than 5 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed, both kinds named" % passed.group(0))
    print("IB28-1-AC1 PASS")


if __name__ == "__main__":
    main()
