"""IB29-2-AC1 -- the export submit path has an Analysis branch, and its Performance branch is unchanged.

Runs, bounded at 110 s, infra/aws/lambda/investor-reporting/export/tests/test_submit_analysis_branch.py together with the existing
export/tests/test_submit_service.py, test_retained_export.py and test_retained_export_analysis.py. Grades: the new file exists and
names ANALYSIS and PERFORMANCE; 0 failed or errored; at least 4 more tests passed than the existing three files pass alone.
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "infra/aws/lambda/investor-reporting/export/tests/"
NEW = BASE + "test_submit_analysis_branch.py"
OLD = [BASE + "test_submit_service.py", BASE + "test_retained_export.py", BASE + "test_retained_export_analysis.py"]


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-2-AC1 FAIL")
    sys.exit(1)


def run(root, files):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files,
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    m = re.search(r"(\d+) passed", out)
    return int(m.group(1)) if m else 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / NEW
    if not t.is_file():
        fail("no test file at %s" % NEW)
    src = t.read_text(encoding="utf-8")
    for kind in ("ANALYSIS", "PERFORMANCE"):
        if kind not in src:
            fail("the test file never names %s" % kind)
    old = run(root, OLD)
    both = run(root, OLD + [NEW])
    if both - old < 4:
        fail("only %d new test(s) passed beside the existing %d" % (both - old, old))
    print("OK: %d new + %d existing passed, 0 failed" % (both - old, old))
    print("IB29-2-AC1 PASS")


if __name__ == "__main__":
    main()
