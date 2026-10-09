"""IRPT_BCKEND round 96 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-387 (CTO msgs 2363 and 2368, on ~V2 msgs 2359
and 2366): the PROFILE-row allowedFirmIds narrowing at _authz/served.py ~:1134, today applied to service principals, extends to internal
callers, with the row found by the verified identity (the token carries no allowedFirmIds claim). A non-empty list narrows; no row or an
empty list is unchanged; a non-list value is REFUSED (fail closed); ALL never admits.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB96-1-AC1  in _authz/tests, `-k allowed_firm_ids` passes (>= 5): a listed firm is admitted; an unlisted firm is refused; no row or
              an empty list is unchanged from today; a non-list value is refused; ALL is refused with a non-empty list. Base: FAIL (no such tests).
  IB96-1-AC2  the whole _authz/tests suite passes, including IB-pr-385's svc_custody_statement tests. Base: PASS; must stay so.
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
        print("%s FAIL" % (cid or "IB96-1"))
        sys.exit(1)

    if cid == "IB96-1-AC1":
        rc, last = pytest(root / AUTHZ, "tests", "-k", "allowed_firm_ids")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 5:
            fail("-k allowed_firm_ids rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB96-1-AC2":
        rc, last = pytest(root / AUTHZ, "tests")
        if rc != 0:
            fail("_authz suite rc %d: %s" % (rc, last))
        print("OK: _authz suite %s" % last)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
