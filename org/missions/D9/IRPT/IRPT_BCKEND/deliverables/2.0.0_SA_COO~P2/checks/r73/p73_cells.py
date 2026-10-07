"""IRPT_BCKEND round 73 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-359 (the portal conditions of CTO msg 1113 on
IB-pr-356: W165-S2 disarmed -- the wire-generator tests never write tracked contracts/wire -- and W165-S1 -- the custody read passes
a named envelope validation before it mounts).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB73-1-AC1  after `bun --no-install test` over the four wire-generator tests (iv-e-17.gen-oneof, iv-e-17.regenerated,
              iv-e-26.wire-regen, fe-s-25/generator), `git status --porcelain` on portal contracts/wire is EMPTY (no tracked file
              written). Base (b3fedfea, measured in a worktree): FAIL -- 25 tracked files rewritten, 4 with content diffs.
              The test outcome is reported, not graded here: IVE26-AC3 fails at base (generator output differs from 4 committed
              files); the worker names it.
  IB73-1-AC2  the ir-72 custody-print test passes with bun and names parseIrEnvelope or the named custody validation, and the
              custody read in api/endpoints/investor-reporting.ts calls that validation. Base: FAIL (the read sits outside it).
  IB73-G-167  A GUARD: worker ~167's workspace commits touch only its grant, never the portal gitlink. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "72208311d5"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
T = "src/pages/InvestorReporting/__tests__/"
WIRE = "src/pages/InvestorReporting/contracts/wire"
GEN_TESTS = [T + "dsgn-irptv1/iv-e-17.gen-oneof.test.ts", T + "dsgn-irptv1/iv-e-17.regenerated.test.ts",
             T + "dsgn-irptv1/iv-e-26.wire-regen.test.ts", T + "fe-s-25/generator.test.ts"]
GRANT = (P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-359.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~167/")


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
    portal = root / "portal"

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB73"))
        sys.exit(1)

    if cid == "IB73-1-AC1":
        _, before = _run(["git", "status", "--porcelain", WIRE], portal)
        if before.strip():
            fail("contracts/wire is already dirty before the run; restore it first: %s" % before.strip().splitlines()[0])
        rc, out = _run(["bun", "--no-install", "test", *GEN_TESTS], portal, timeout=115)
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        _, after = _run(["git", "status", "--porcelain", WIRE], portal)
        written = [ln for ln in after.splitlines() if ln.strip()]
        if written:
            _run(["git", "checkout", "--", WIRE], portal)
            fail("the generator tests wrote %d tracked contracts/wire file(s) (restored): %s" % (len(written), written[0]))
        print("OK: 0 tracked contracts/wire files written; tests %s pass, %s fail (reported, not graded)" % (
            m.group(1) if m else "?", f.group(1) if f else "0"))
    elif cid == "IB73-1-AC2":
        t = portal / T / "ir-72-custody-print/custody-print.test.tsx"
        api = portal / "src/api/endpoints/investor-reporting.ts"
        if not t.is_file() or not api.is_file():
            fail("the ir-72 test or the api endpoints file is absent")
        src, api_src = t.read_text(encoding="utf-8"), api.read_text(encoding="utf-8")
        named = re.search(r"parseIrEnvelope|validateCustodyReport|parseCustodyReport", src)
        if not named:
            fail("the test does not name parseIrEnvelope or a named custody validation")
        i = api_src.find("custody-report-read")
        window = api_src[i:i + 4000] if i >= 0 else ""
        if not re.search(r"parseIrEnvelope|validateCustodyReport|parseCustodyReport", window):
            fail("the custody read in api/endpoints/investor-reporting.ts does not call the named validation")
        rc, out = _run(["bun", "--no-install", "test", T + "ir-72-custody-print/"], portal)
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        if rc or not m or (f and int(f.group(1)) > 0):
            fail("bun test rc %d: %s" % (rc, _last(out)))
        print("OK: %s pass, %s fail; the read is validated by %s" % (m.group(1), f.group(1) if f else "0", named.group(0)))
    elif cid == "IB73-G-167":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~167", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT) or c == "portal"]
        if bad:
            fail("out-of-grant changes (the portal gitlink is never committed): %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~167's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
