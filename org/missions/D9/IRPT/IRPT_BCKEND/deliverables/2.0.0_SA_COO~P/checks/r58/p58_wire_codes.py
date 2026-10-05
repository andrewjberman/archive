"""IRPT_BCKEND round 58 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the refusal classes reach the WIRE at the boundary's
enforcer_for call site (_authz/served.py:1050-1054): today it answers FIRM_BINDING for an AuthzError and UNEXPECTED for everything
else, so IB-pr-321/322's declared classes reach only the log record.

Usage: python <this file> <repo_root> <criterion_id>
  IB58-1-AC1  the new tests (TESTS) pass, at least 4, naming W, and pin the wire: an AuthzError still answers FIRM_BINDING; a
              BucketUnmapped answers FIRM_BINDING; a MaintainedSourceUnready answers NOT_READY; an unclassified exception answers
              UNEXPECTED. The _authz suite passes with 0 failed. Base: FAIL.
  IB58-1-AC2  a GUARD: the worker's own commits touch only _authz/served.py, _authz/tests/, its deliverables, the channel and its
              order. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "d228db29a9"
IR = "infra/aws/lambda/investor-reporting"
TESTS = IR + "/_authz/tests/test_wire_reason_codes.py"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~129"
GRANT = (IR + "/_authz/served.py", IR + "/_authz/tests/", "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~129/",
         "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-326.")


def _pytest(root, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root / IR),
                       capture_output=True, text=True, timeout=900)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
    return r.returncode, ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB58-1"))
        sys.exit(1)

    if cid == "IB58-1-AC1":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        for w in ("FIRM_BINDING", "NOT_READY", "UNEXPECTED", "AuthzError"):
            if w not in src:
                fail("tests never name %r" % w)
        rc, last = _pytest(root, "_authz/tests/test_wire_reason_codes.py")
        m = re.search(r"(\d+) passed", last)
        if rc or not m or int(m.group(1)) < 4 or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        rc, last2 = _pytest(root, "_authz/tests/")
        if rc or re.search(r"\d+ (failed|error)", last2):
            fail("_authz suite: %s" % last2)
        print("OK: new tests %s; _authz %s" % (last, last2))
    elif cid == "IB58-1-AC2":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
