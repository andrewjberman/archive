"""IRPT_YCDGEN round 1 check l-1.AC1 (YCD-l-1). Run from the repository root. Prints 'l-1.AC1 RESULT: PASS|FAIL <why>'."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"


def verdict(ok, why):
    print("l-1.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


def pytest_count(test_file, minimum):
    path = RESEARCH / "tests" / test_file
    if not path.is_file():
        verdict(False, "absent: %s" % path.relative_to(ROOT).as_posix())
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(path)],
                         capture_output=True, text=True, timeout=110)
    tail = (out.stdout.strip().splitlines() or [""])[-1]
    passed = int((re.search(r"(\d+) passed", tail) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", tail) or [0, 0])[1]) + int((re.search(r"(\d+) error", tail) or [0, 0])[1])
    verdict(out.returncode == 0 and failed == 0 and passed >= minimum, "%d passed, %d failed (need >= %d): %s" % (
        passed, failed, minimum, tail[:160]))

pytest_count("test_layout_overview.py", 4)
