"""IB35-1-AC2 -- row IRPT_BCKEND-S276: build-and-upload.sh never deletes a tracked source file.

Grades:
  1. infra/aws/lambda/ci/build-and-upload.sh's cleanup_staged no longer removes a staged name unconditionally: the function body
     names "ls-files" (it asks git whether the path is tracked) and restores a tracked path rather than deleting it.
  2. infra/aws/lambda/ci/test_build_staging_keeps_tracked.py names "tracked" and "cleanup_staged"; at least 2 tests pass, 0 failed
     or errored (bounded at 110 s): a tracked member survives staging and cleanup with its HEAD bytes, and an untracked staged
     member is removed.
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = "infra/aws/lambda/ci/build-and-upload.sh"
TEST = "infra/aws/lambda/ci/test_build_staging_keeps_tracked.py"


def fail(msg):
    print("FAIL: " + msg)
    print("IB35-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    s = (root / SCRIPT).read_text(encoding="utf-8")
    m = re.search(r"cleanup_staged\(\)\s*\{(.*?)\n\}", s, re.S)
    if not m:
        fail("no cleanup_staged() function in %s" % SCRIPT)
    body = m.group(1)
    if "ls-files" not in body:
        fail("cleanup_staged does not ask git whether a staged path is tracked")
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    tsrc = t.read_text(encoding="utf-8")
    for word in ("tracked", "cleanup_staged"):
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
    print("OK: cleanup_staged consults git ls-files; %s, 0 failed" % passed.group(0))
    print("IB35-1-AC2 PASS")


if __name__ == "__main__":
    main()
