"""IRPT_BCKEND round 79 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-366 (E5 of the CTO analysis ADDENDUM 2
@b227133904: the live guard resolves an on-behalf owner for an OPAL_GLOBAL filer's CREATE).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Each pytest file runs in its OWN process: the suites below collide on a
double import of uploads.UploadRefused when collected together (7 false failures measured at base 5ff7717f66), never alone.

  IB79-1-AC1  the test file T imports `served` (the real guarded entry) and `pytest -k served_admits_listed_firm` on T collects >= 1
              test and passes. Base: FAIL (no file).
  IB79-1-AC2  `pytest -k served_refuses` on T collects the eight named negative arms (unlisted_firm, all, non_internal,
              owner_opal_capital; AMENDMENT 1: advisor_email_absent, advisor_profile_absent, advisor_profile_disabled,
              advisor_of_other_firm) and passes. Base: FAIL (no file).
  IB79-1-AC3  each existing guard / scope / uploads suite in SUITES passes, each in its own process. Base: PASS (the
              no-regression arm; 10 + 77 tests across the files, read 2026-10-08 ~18:1xZ).
"""
import re
import subprocess
import sys
from pathlib import Path

LAMBDA = "infra/aws/lambda/investor-reporting"
T = "_authz/tests/test_served_on_behalf_create.py"
# AMENDMENT 1 (CTO ruling msg 1402, row D2-W174-S1): four more arms on the advisor-email lookup key.
NEG = ("served_refuses_unlisted_firm", "served_refuses_all", "served_refuses_non_internal", "served_refuses_owner_opal_capital",
       "served_refuses_advisor_email_absent", "served_refuses_advisor_profile_absent",
       "served_refuses_advisor_profile_disabled", "served_refuses_advisor_of_other_firm")
SUITES = ("_authz/tests/test_guarded_entries.py", "_scope/tests/test_interactive_access.py",
          "_scope/tests/test_interactive_access_on_behalf.py", "intake/tests/test_uploads.py",
          "intake/tests/test_uploads_on_behalf.py", "intake/tests/test_upload_door_reads_allowed_firms.py")


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    last = [ln for ln in re.sub(r"\x1b\[[0-9;]*m", "", out).splitlines() if ln.strip()]
    return p.returncode, out, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    lam = root / LAMBDA

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB79-1"))
        sys.exit(1)

    if cid in ("IB79-1-AC1", "IB79-1-AC2"):
        f = lam / T
        if not f.is_file():
            fail("no %s/%s" % (LAMBDA, T))
        src = f.read_text(encoding="utf-8")
        if not re.search(r"^\s*import served\b|^\s*from served import", src, re.M):
            fail("%s does not import served (the real guarded entry)" % T)
        if cid == "IB79-1-AC1":
            rc, out, last = pytest(lam, T, "-k", "served_admits_listed_firm")
            if rc != 0 or not re.search(r"\b[1-9]\d* passed", last):
                fail("admit arm rc %d: %s" % (rc, last))
            print("OK: admit arm through served: %s" % last)
        else:
            missing = [n for n in NEG if not re.search(r"def test_%s\b" % n, src)]
            if missing:
                fail("negative arms not defined: %s" % missing)
            rc, out, last = pytest(lam, T, "-k", "served_refuses")
            m = re.search(r"\b(\d+) passed", last)
            if rc != 0 or not m or int(m.group(1)) < len(NEG):
                fail("negative arms rc %d: %s" % (rc, last))
            print("OK: %d negative arms through served: %s" % (len(NEG), last))
    elif cid == "IB79-1-AC3":
        lines = []
        for s in SUITES:
            rc, out, last = pytest(lam, s)
            if rc != 0:
                fail("%s rc %d: %s" % (s, rc, last))
            lines.append("%s: %s" % (s, last))
        print("OK: %d of %d suites pass, each in its own process" % (len(SUITES), len(SUITES)))
        for ln in lines:
            print("  " + ln)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
