"""IRPT_BCKEND round 95 cell IB-pr-384 (row D2-W189-S4; CTO msg 2151: yes, after the IB-pr-383 release) -- the directory runner REFUSES to land a build
that drops an entry the source still holds, so a build fault can never reach the served directory again.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB95-1-AC1  in the runner tests, `-k refuse_drop` passes (>= 3): an entry in the source but missing from the build refuses the landing
          with a named error and makes 0 S3 puts; a genuine source removal still lands (TERMINATED carry); unknown source keys refuse
          only when a previous client is missing. Base: FAIL (no such tests).
  IB95-1-AC2  the whole runner suite passes, excusing only the pre-existing red KNOWN_RED by exact node id. Base: PASS except KNOWN_RED;
          must stay so with the change.
"""
import re
import subprocess
import sys
from pathlib import Path

RUNNER = "data/assets/scripts/gold/investor_reporting"
KNOWN_RED = {"tests/test_holdings_rearm_trigger.py::test_rearm_trigger_live"}


def pytest(cwd, *args, failed=None):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    if failed is not None:
        failed.update(m.replace("\\", "/") for m in re.findall(r"^FAILED (\S+?)(?: - |$)", out, re.M))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB95-1"))
        sys.exit(1)

    if cid == "IB95-1-AC1":
        rc, last = pytest(root / RUNNER, "tests", "-k", "refuse_drop")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 3:
            fail("-k refuse_drop rc %d: %s" % (rc, last))
        print("OK: -k refuse_drop: %s" % last)
    elif cid == "IB95-1-AC2":
        red = set()
        rc, last = pytest(root / RUNNER, "tests", failed=red)
        if rc != 0 and not (red and red <= KNOWN_RED and re.search(r"\b%d failed" % len(red), last)):
            fail("runner suite rc %d: %s; failed %s" % (rc, last, sorted(red)))
        print("OK: runner suite %s; excused %s" % (last, sorted(red)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
