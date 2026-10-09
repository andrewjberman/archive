"""IRPT_BCKEND round 95 cell IB-pr-385 (CTO ruling msg 2311 on ~K2 msg 2304/2305) -- verified_internal_subject admits ONE named,
firm-bound service subject, svc-custody-statement, on custody-report-persist, POST /analysis and POST /export.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB95-2-AC1  in _authz/tests, `-k svc_custody_statement` passes (>= 5): cottonwood (from the verified token claim) is admitted on each of
           the three routes; 49financial and inflection claims are refused; the subject never reaches the opal-capital any-firm
           selection or ALL; any other service subject is refused as today. Base: FAIL (no such tests).
  IB95-2-AC2  the whole _authz/tests suite passes. Base: PASS (268); must stay so with the change.
"""
import re
import subprocess
import sys
from pathlib import Path

AUTHZ = "infra/aws/lambda/investor-reporting/_authz"


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB95-2"))
        sys.exit(1)

    if cid == "IB95-2-AC1":
        rc, last = pytest(root / AUTHZ, "tests", "-k", "svc_custody_statement")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 5:
            fail("-k svc_custody_statement rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB95-2-AC2":
        rc, last = pytest(root / AUTHZ, "tests")
        if rc != 0:
            fail("_authz suite rc %d: %s" % (rc, last))
        print("OK: _authz suite %s" % last)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
