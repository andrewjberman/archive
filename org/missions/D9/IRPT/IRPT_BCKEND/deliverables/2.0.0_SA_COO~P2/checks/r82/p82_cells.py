"""IRPT_BCKEND round 82 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-369 (E9 of the CTO analysis ADDENDUM 6:
ReportRepository retains each family under its own policy revision; CUSTODY_REPORT under irpt-custody-x10-v1).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Each pytest run is its own process.

  IB82-1-AC1  in T, `-k custody_under_custody_policy` passes (>= 1 test): a CUSTODY_REPORT is reserved and read back under
              irpt-custody-x10-v1 while PERFORMANCE and ANALYSIS stay under irpt-x10-v1. Base: FAIL (no file).
  IB82-1-AC2  in T, `-k x10_retained_reads_back_unchanged` passes (>= 1 test), AND reports/tests/test_repository.py,
              test_retained_repository.py and test_retention.py each pass alone (the regression arm); AMENDMENT 1: and
              `-k x10_composes_without_custody_row` passes (no custody row in the registry breaks no other family). Base: FAIL (no file;
              the three existing files pass at base: 24, 21 and test_retained_repository).
  IB82-1-AC3  in T, `-k unregistered_kind_refuses` passes (>= 1 test). Base: FAIL (no file).
"""
import re
import subprocess
import sys
from pathlib import Path

REPORTS = "infra/aws/lambda/investor-reporting/reports"
T = "tests/test_repository_family_revisions.py"
EXISTING = ("tests/test_repository.py", "tests/test_retained_repository.py", "tests/test_retention.py")
K = {"IB82-1-AC1": "custody_under_custody_policy", "IB82-1-AC2": "x10_retained_reads_back_unchanged",
     "IB82-1-AC3": "unregistered_kind_refuses"}


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    rep = root / REPORTS

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB82-1"))
        sys.exit(1)

    if cid not in K:
        fail("unknown criterion %r" % cid)
    if not (rep / T).is_file():
        fail("no %s/%s" % (REPORTS, T))
    rc, last = pytest(rep, T, "-k", K[cid])
    if rc != 0 or not re.search(r"\b[1-9]\d* passed", last):
        fail("-k %s rc %d: %s" % (K[cid], rc, last))
    print("OK: -k %s: %s" % (K[cid], last))
    if cid == "IB82-1-AC2":
        # AMENDMENT 1 (row D2-W177-S1): with no irpt-custody-x10-v1 row in the registry, PERFORMANCE/ANALYSIS still compose.
        rc, last2 = pytest(rep, T, "-k", "x10_composes_without_custody_row")
        if rc != 0 or not re.search(r"\b[1-9]\d* passed", last2):
            fail("-k x10_composes_without_custody_row rc %d: %s" % (rc, last2))
        print("  -k x10_composes_without_custody_row: %s" % last2)
        for e in EXISTING:
            rc, last = pytest(rep, e)
            if rc != 0:
                fail("%s rc %d: %s" % (e, rc, last))
            print("  %s: %s" % (e, last))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
