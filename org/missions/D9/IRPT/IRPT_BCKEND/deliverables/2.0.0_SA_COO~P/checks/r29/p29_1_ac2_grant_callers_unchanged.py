"""IB29-1-AC2 -- every caller of the shared render grant is named, and the existing grant and export suites pass unchanged.

Reads deliverables/0.9.0_WK_IRPT_BCKEND~101/GRANT_CALLERS_R29.json:
  {"files_scanned": n, "callers": [{"path": "<repo-relative file>", "how": "<the call site>"}], "census_command": "<the command>"}
Grades: files_scanned > 0; at least one caller; every caller path exists and its text names "grant"; then runs, bounded at
110 s, the existing suites _render_identity/tests/test_grant.py, _render_identity/tests/test_carriage.py,
export/tests/test_retained_export.py and export/tests/test_retained_export_analysis.py: 0 failed or errored and at least 1 passed.
Usage: python <this file> <repo_root>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101/GRANT_CALLERS_R29.json"
BASE = "infra/aws/lambda/investor-reporting/"
SUITES = [BASE + "_render_identity/tests/test_grant.py", BASE + "_render_identity/tests/test_carriage.py",
          BASE + "export/tests/test_retained_export.py", BASE + "export/tests/test_retained_export_analysis.py"]


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    rp = root / REC
    if not rp.is_file():
        fail("no caller census at %s" % REC)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    if int(rec.get("files_scanned") or 0) <= 0:
        fail("files_scanned is not positive")
    callers = rec.get("callers") or []
    if not callers:
        fail("no caller listed")
    for c in callers:
        p = root / str(c.get("path", ""))
        if not p.is_file():
            fail("listed caller does not exist: %s" % c.get("path"))
        if "grant" not in p.read_text(encoding="utf-8", errors="replace"):
            fail("listed caller never names grant: %s" % c.get("path"))
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + SUITES,
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad or not passed:
        fail("existing suites: %s" % (bad.group(0) if bad else out.strip()[-200:]))
    print("OK: %d caller(s) of %d file(s) scanned; existing suites %s, 0 failed" % (
        len(callers), int(rec["files_scanned"]), passed.group(0)))
    print("IB29-1-AC2 PASS")


if __name__ == "__main__":
    main()
