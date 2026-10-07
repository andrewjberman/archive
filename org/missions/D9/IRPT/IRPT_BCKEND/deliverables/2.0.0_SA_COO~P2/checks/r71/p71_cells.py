"""IRPT_BCKEND round 71 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of cell IB-pr-354 (InteractiveAccess.current() carries
allowedFirmIds for an OPAL_GLOBAL subject, so IB-yr-631's on-behalf upload admit is reachable; CTO ruling msg 945 on row W152-S1).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB71-1-AC1  _scope/tests/test_interactive_access_on_behalf.py exists and names allowedFirmIds, "ALL" and create; it passes together
              with _scope/tests/test_interactive_access.py and intake/tests/test_uploads_on_behalf.py. Base: FAIL (no test).
  IB71-G-163  A GUARD: worker ~163's commits touch only its grant. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "6115baf2e7"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
IR = "infra/aws/lambda/investor-reporting"
GRANT = (IR + "/_scope/interactive_access.py", IR + "/_scope/tests/test_interactive_access_on_behalf.py",
         P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-354.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~163/")


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB71"))
        sys.exit(1)

    if cid == "IB71-1-AC1":
        t = root / IR / "_scope/tests/test_interactive_access_on_behalf.py"
        if not t.is_file():
            fail("no %s/_scope/tests/test_interactive_access_on_behalf.py" % IR)
        src = t.read_text(encoding="utf-8")
        for need in ("allowedFirmIds", '"ALL"', "create"):
            if need not in src and need.replace('"', "'") not in src:
                fail("the test never names %s" % need)
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "_scope/tests/test_interactive_access_on_behalf.py", "_scope/tests/test_interactive_access.py",
                        "intake/tests/test_uploads_on_behalf.py"], root / IR)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("tests: %s" % last)
        print("OK: %s" % last)
    elif cid == "IB71-G-163":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~163", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~163's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
