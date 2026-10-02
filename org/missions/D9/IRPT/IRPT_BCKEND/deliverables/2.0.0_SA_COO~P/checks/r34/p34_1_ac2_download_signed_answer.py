"""IB34-1-AC2 -- G4 (CTO batch 175): the receipt's download route is the live route, and the live entry's export_download returns a
signed answer in hop 11's shape.

Grades:
  1. infra/aws/lambda/investor-reporting/export/receipt.py names "/api/scoped/investor-reporting/export/{" and no longer names
     "/api/scoped/exports/".
  2. infra/aws/lambda/investor-reporting/export/tests/test_download_signed_answer.py names "X-Amz-Algorithm", "300", "sha256",
     "byte_length" and "lambda_handler"; at least 4 tests pass, 0 failed or errored (bounded at 110 s).
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/export/"
TEST = B + "tests/test_download_signed_answer.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB34-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    rec = (root / B / "receipt.py").read_text(encoding="utf-8")
    if "/api/scoped/investor-reporting/export/{" not in rec:
        fail("receipt.py does not name the live route /api/scoped/investor-reporting/export/{...}/download")
    if "/api/scoped/exports/" in rec:
        fail("receipt.py still names /api/scoped/exports/")
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("X-Amz-Algorithm", "300", "sha256", "byte_length", "lambda_handler"):
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
    print("OK: receipt names the live route; %s, 0 failed" % passed.group(0))
    print("IB34-1-AC2 PASS")


if __name__ == "__main__":
    main()
