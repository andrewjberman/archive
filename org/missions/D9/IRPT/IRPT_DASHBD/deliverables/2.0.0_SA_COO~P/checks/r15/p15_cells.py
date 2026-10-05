"""IRPT_DASHBD round 15 (workstream B, issuer 2.0.0_SA_COO~P) -- the CTO's round-15 enrichment list
(org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_IRPT_DASHBD_ROUNDS_12_14_B_20261005.md @b09cafb7a4), items E3 and E4.

Usage: python <this file> <repo_root> <criterion_id>
  DB15-1-AC1  routes.json declares both live reporting routes (a route_key containing `/reporting/{account_id}/{which}` and
              one containing `/reporting/client/{client_id}/summary`), each with handler irpt-49f-reporting-read-lambda, and
              its `_denominator` names the new route count. Base: FAIL.
  DB15-1-AC2  the census that reads the file, investor-reporting _authz/tests/test_unguarded_census.py, passes with 0 failed.
              Base: PASS (regression).
  DB15-1-AC3  (amendment 1) the two reporting routes carry status ROUTED_ELSEWHERE with a non-empty `routed_by` (so the api root's
              routes.tf, which routes only status DECLARED, never sees them), and _contracts/tests/test_seam_paired.py passes with 0
              failed. Base: FAIL.
  DB15-2-AC1  E3_SHAPE_RULING.json and BD_POPULATION_PULL_E3.json are TRACKED in the DB-b-20 folder, parse as JSON, and the
              ruling names batches 248 and 249 and no longer says the bearer is minted once. Base: FAIL (untracked).
  DB-GUARD    the commits of 0.9.0_WK_IRPT_DASHBD~9 and ~10 since base touch only their grants. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "53acc6abb8"
ROUTES = "docs/contracts/investor-reporting/v1/routes.json"
IR = "infra/aws/lambda/investor-reporting"
B20 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/"
GRANTS = {
    "0.9.0_WK_IRPT_DASHBD~9": (ROUTES, IR + "/_authz/tests/test_unguarded_census.py", "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~9/",
                               "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md",
                               "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-23."),
    "0.9.0_WK_IRPT_DASHBD~10": (B20 + "E3_SHAPE_RULING.json", B20 + "BD_POPULATION_PULL_E3.json",
                                "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~10/",
                                "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md",
                                "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-24."),
}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB15"))
        sys.exit(1)

    if cid == "DB15-1-AC1":
        d = json.loads((root / ROUTES).read_bytes().decode("utf-8"))
        routes = d.get("routes") or []
        want = ("/reporting/{account_id}/{which}", "/reporting/client/{client_id}/summary")
        for w in want:
            hit = [r for r in routes if w in str(r.get("route_key", ""))]
            if not hit:
                fail("no route_key containing %s" % w)
            if not any(r.get("handler") == "irpt-49f-reporting-read-lambda" for r in hit):
                fail("%s is not handled by irpt-49f-reporting-read-lambda" % w)
        if str(len(routes)) not in json.dumps(d.get("_denominator")):
            fail("_denominator does not name the route count %d" % len(routes))
        print("OK: both reporting routes declared; %d routes" % len(routes))
    elif cid == "DB15-1-AC2":
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "_authz/tests/test_unguarded_census.py"],
                           cwd=str(root / IR), capture_output=True, text=True, timeout=900)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        last = ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]
        if r.returncode or re.search(r"\d+ (failed|error)", last):
            fail("census: %s" % last)
        print("OK: census %s" % last)
    elif cid == "DB15-1-AC3":
        d = json.loads((root / ROUTES).read_bytes().decode("utf-8"))
        rep = [r for r in d.get("routes") or [] if "/reporting/" in str(r.get("route_key", ""))]
        if len(rep) < 2:
            fail("fewer than 2 reporting routes declared")
        for r in rep:
            if r.get("status") != "ROUTED_ELSEWHERE" or not r.get("routed_by"):
                fail("%s: status %r routed_by %r" % (r.get("route_key"), r.get("status"), r.get("routed_by")))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "_contracts/tests/test_seam_paired.py"],
                           cwd=str(root / IR), capture_output=True, text=True, timeout=900)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
        last = ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]
        if r.returncode or re.search(r"\d+ (failed|error)", last):
            fail("seam test: %s" % last)
        print("OK: both reporting routes ROUTED_ELSEWHERE; seam %s" % last)
    elif cid == "DB15-2-AC1":
        tracked = subprocess.run(["git", "ls-files", B20], cwd=str(root), capture_output=True).stdout.decode("utf-8").split()
        for name in ("E3_SHAPE_RULING.json", "BD_POPULATION_PULL_E3.json"):
            if B20 + name not in tracked:
                fail("%s is not tracked" % name)
            json.loads((root / B20 / name).read_bytes().decode("utf-8"))
        rul = (root / B20 / "E3_SHAPE_RULING.json").read_bytes().decode("utf-8")
        if "248" not in rul or "249" not in rul or re.search(r"minted once", rul, re.I):
            fail("the ruling does not name batches 248 and 249, or still says minted once")
        print("OK: both files tracked; ruling names batches 248 and 249")
    elif cid == "DB-GUARD":
        bad = []
        for author, grant in GRANTS.items():
            r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % author, "--name-only", "--format="],
                               cwd=str(root), capture_output=True)
            changed = set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip())
            bad += ["%s:%s" % (author, c) for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: all worker paths inside their grants")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
