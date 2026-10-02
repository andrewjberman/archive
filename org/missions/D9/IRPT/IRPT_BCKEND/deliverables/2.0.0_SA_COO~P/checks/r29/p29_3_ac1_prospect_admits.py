"""IB29-3-AC1 -- (a) the Enforcer admits a prospect render for each of the four pinned keys and refuses a foreign artifact,
another report's key and an account object.

Runs infra/aws/lambda/investor-reporting/_authz/tests/test_enforce_prospect_admit.py with pytest (bounded at 110 s). Grades: the
file exists and names the four roles (report, sections, composition, vendor_pdf) and "foreign"; at least 7 tests passed (4 admits
and 3 refusals), 0 failed or errored. Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/_authz/tests/test_enforce_prospect_admit.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-3-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("report", "sections", "composition", "vendor_pdf", "foreign"):
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
    if not passed or int(passed.group(1)) < 7:
        fail("fewer than 7 tests passed: %s" % (passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s, 0 failed" % passed.group(0))
    print("IB29-3-AC1 PASS")


if __name__ == "__main__":
    main()
