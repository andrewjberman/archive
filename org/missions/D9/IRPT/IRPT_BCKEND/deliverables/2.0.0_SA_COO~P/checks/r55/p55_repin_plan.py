"""IRPT_BCKEND round 55 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the re-pin PLAN for the r54 code the census could not ship
(CTO msg 105217: "The re-pin cell for 317, 321, 322, S241 and S298 is yours to cut"). An analysis cell: it edits no source map.

Usage: python <this file> <repo_root> <criterion_id>
  IB55-1-AC1  PLAN exists and covers every (function, member) pair where a function in FUNCTIONS packages, via staged_from, a
              repo_path in TARGET_PATHS. Each pair carries function, member (repo_path), pin, target, commits (each with sha
              and subject) and verdict CLEAN or RIDER. A CLEAN pair's commits all name one of IB-pr-317, IB-pr-320, IB-pr-321 or
              IB-pr-322 in their subject. Base: FAIL (no plan).
  IB55-1-AC2  the plan's pair set equals the set this checker derives from lambda-source-map.json at HEAD (no pair missing,
              none invented). Base: FAIL.
  IB55-1-AC3  a GUARD: the worker's own commits touch only its deliverables folder, the channel and its order, and never
              lambda-source-map.json. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import subprocess
import sys
from pathlib import Path

BASE = "0642c9d004"
IR = "infra/aws/lambda/investor-reporting/"
FUNCTIONS = ("irpt-49f-reporting-read-lambda", "irpt-directory-search", "irpt-holdings", "irpt-status", "irpt-export-render",
             "irpt-performance-adapter", "irpt-narrative", "irpt-ycharts-generate")
TARGET_PATHS = (IR + "_authz/loaders.py", IR + "_authz/served.py", IR + "_scope/maintained_sources.py",
                IR + "_scope/canonical_profile_reads.py", IR + "_scope/retained_input_authorizer.py",
                IR + "performance/holdings_gold.py", IR + "_contracts/ExportBundle.schema.json", IR + "export/bundle.py",
                IR + "export/entry.py")
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~127/"
PLAN = W + "REPIN_PLAN_R55.json"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~127"
ORDERS = ("IB-pr-317", "IB-pr-320", "IB-pr-321", "IB-pr-322")


def derive_pairs(root):
    d = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_bytes().decode("utf-8"))["functions"]
    pairs = set()
    for fn in FUNCTIONS:
        for s in d.get(fn, {}).get("staged_from") or []:
            if s.get("repo_path") in TARGET_PATHS:
                pairs.add((fn, s["repo_path"]))
    return pairs


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB55-1"))
        sys.exit(1)

    if cid in ("IB55-1-AC1", "IB55-1-AC2"):
        p = root / PLAN
        if not p.is_file():
            fail("no %s" % PLAN)
        rows = json.loads(p.read_bytes().decode("utf-8")).get("pairs") or []
        if cid == "IB55-1-AC1":
            if not rows:
                fail("no pairs")
            for r in rows:
                for k in ("function", "member", "pin", "target", "commits", "verdict"):
                    if k not in r:
                        fail("pair lacks %r: %r" % (k, {x: r.get(x) for x in ("function", "member")}))
                if r["verdict"] not in ("CLEAN", "RIDER"):
                    fail("verdict %r" % r["verdict"])
                if r["verdict"] == "CLEAN":
                    bad = [c for c in r["commits"] if not any(o in str(c.get("subject", "")) for o in ORDERS)]
                    if bad:
                        fail("CLEAN pair %s %s has an unattributed commit %s" % (r["function"], r["member"], bad[0].get("sha")))
            n_clean = sum(1 for r in rows if r["verdict"] == "CLEAN")
            print("OK: %d pairs, %d CLEAN, %d RIDER" % (len(rows), n_clean, len(rows) - n_clean))
        else:
            got = {(r.get("function"), r.get("member")) for r in rows}
            want = derive_pairs(root)
            if got != want:
                fail("missing %s; invented %s" % (sorted(want - got)[:5], sorted(got - want)[:5]))
            print("OK: %d pairs equal the derived set" % len(want))
    elif cid == "IB55-1-AC3":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        grant = (W, "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
                 "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-324.")
        bad = [c for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
