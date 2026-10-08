"""IRPT_BCKEND round 75 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-361 (row S388, ~P's share: the portal wire
types for ExportBundle, ExportReceipt and the route-derived responses/index were never regenerated after ~P's own contract changes,
IB-pr-336 custody_report_ref, IB-pr-343 covered_account_ids, IB-pr-355 the custody route).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB75-1-AC1  in portal/: one run of the wire-regen test leaves ~P's FOUR files (ExportBundle.ts, ExportReceipt.ts, responses.ts,
              index.ts) byte-unchanged -- they equal the generator's output; every other wire file the run rewrites is restored by
              this check and is NOT graded (AnalysisReport is IRPT_YCDGEN's, HoldingsSnapshot MDPF_SECCLASS's); and the branch's
              diff against portal DEV under contracts/wire names only those four. Base (portal DEV): FAIL (the run changes all four).
  IB75-1-AC2  in portal/: tsc -b --noEmit exits 0. Base: PASS (a control).
  IB75-G-169  A GUARD: worker ~169's workspace commits touch only its grant, never the portal gitlink. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "4022181507"
DEV = "d1b21c97"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
WIRE = "src/pages/InvestorReporting/contracts/wire"
MINE = [WIRE + "/ExportBundle.ts", WIRE + "/ExportReceipt.ts", WIRE + "/responses.ts", WIRE + "/index.ts"]
REGEN = "src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-26.wire-regen.test.ts"
GRANT = (P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-361.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~169/")


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def _changed(portal, paths):
    _, out = _run(["git", "diff", "--numstat", "--", *paths], portal)
    return [ln.split("\t")[-1] for ln in out.splitlines() if ln.strip() and not ln.startswith("warning")
            and (lambda a: a[0] != "0" or a[1] != "0")(ln.split("\t"))]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    portal = root / "portal"

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB75"))
        sys.exit(1)

    if cid == "IB75-1-AC1":
        if _changed(portal, [WIRE]):
            fail("contracts/wire has uncommitted content changes before the run; commit or restore first")
        _run(["bun", "--no-install", "test", REGEN], portal, timeout=115)
        drifted = _changed(portal, MINE)
        _run(["git", "checkout", "--", WIRE], portal)
        if drifted:
            fail("one regeneration changes ~P's file(s): %s" % drifted)
        _, names = _run(["git", "diff", "--name-only", DEV, "HEAD", "--", WIRE], portal)
        touched = sorted(n for n in names.splitlines() if n.strip() and not n.startswith("warning"))
        extra = [n for n in touched if n not in MINE]
        if extra:
            fail("the branch changes wire files outside ~P's four: %s" % extra)
        print("OK: ~P's 4 wire files equal the generator's output; branch touches %d of 4 under contracts/wire" % len(touched))
    elif cid == "IB75-1-AC2":
        rc, out = _run(["node", "node_modules/typescript/bin/tsc", "-b", "--noEmit"], portal, timeout=115)
        if rc:
            fail("tsc -b --noEmit rc %d: %s" % (rc, _last(out)))
        print("OK: tsc -b --noEmit rc 0")
    elif cid == "IB75-G-169":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~169", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT) or c == "portal"]
        if bad:
            fail("out-of-grant changes (the portal gitlink is never committed): %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~169's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
