"""IRPT_BCKEND round 66 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-346 (the print page refuses a kind it does not
know; the PrintEntry custody-report candidate @cdda4378 is checked for DEV, CTO review msg 403).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s (tsc -b measured 39 s, eslint on one file 9 s).

  IB66-1-AC1  portal/src/pages/InvestorReporting/__tests__/ir-66-print-kind/print-kind.test.ts passes with bun (0 fail): it names
              custody-report and asserts 0 requests, and an unknown kind is refused. Base: FAIL (no test).
  IB66-1-AC2  in portal/: tsc -b --noEmit exits 0, and eslint on render/PrintEntry.tsx exits 0. Base (portal DEV 8ddfe409): PASS;
              graded on the worker's portal branch.
  IB66-G-147  A GUARD: worker ~147's workspace commits touch only its grant. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "fd0c709235"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
TEST = "src/pages/InvestorReporting/__tests__/ir-66-print-kind/print-kind.test.ts"
GRANT = ("portal", P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-346.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~147/")


def _run(cmd, cwd, timeout=115):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    portal = root / "portal"

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB66"))
        sys.exit(1)

    if cid == "IB66-1-AC1":
        t = portal / TEST
        if not t.is_file():
            fail("no portal/%s" % TEST)
        src = t.read_text(encoding="utf-8")
        if "custody-report" not in src or not re.search(r"\b0\b", src):
            fail("the test does not name custody-report and a zero request count")
        rc, out = _run(["bun", "test", TEST], portal)
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        if rc or not m or (f and int(f.group(1)) > 0):
            fail("bun test rc %d: %s" % (rc, _last(out)))
        print("OK: %s pass, %s fail" % (m.group(1), f.group(1) if f else "0"))
    elif cid == "IB66-1-AC2":
        rc, out = _run(["node", "node_modules/typescript/bin/tsc", "-b", "--noEmit"], portal)
        if rc:
            fail("tsc -b --noEmit rc %d: %s" % (rc, _last(out)))
        rc, out = _run(["node", "node_modules/eslint/bin/eslint.js", "src/pages/InvestorReporting/render/PrintEntry.tsx"], portal)
        if rc:
            fail("eslint PrintEntry.tsx rc %d: %s" % (rc, _last(out)))
        print("OK: tsc -b --noEmit rc 0; eslint PrintEntry.tsx rc 0")
    elif cid == "IB66-G-147":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~147", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT) or c == "portal"]
        if bad:
            fail("out-of-grant changes (the portal gitlink is never committed): %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~147's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
