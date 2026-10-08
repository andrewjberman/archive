"""IRPT_BCKEND round 90 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-378 (applied by 0.7.0_AE_CloudOps~DELL2:
IB-pr-376's function release of irpt-export-render at pin 49bc13131d, THEN the custody-report-persist route; COO half @66c617a5c7,
CTO half @b97fa248b2 with its sequencing ruling; IAM leg applied 22:47:14Z).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB90-1-AC1  the after-reads file A reads pin 49bc13131d; census members EXACTLY {custody_persist.py, custody_write.py};
              start_live_codesha rNjtTwcm...; built_sha 7T29wPhz... == live CodeSha256 (re-read live here); post-census 0;
              replan 0; replay identical with the negative control refused by both; rolled_back false. Base: FAIL (no file).
  IB90-1-AC2  the route POST /api/scoped/investor-reporting/custody-report is live on api 7k3ed8px20 (re-read live here, filtered),
              A records route_applied_after_function_live true and route_replan 0, and the ledger is closed. Base: FAIL.
"""
import json
import subprocess
import sys
from pathlib import Path

F = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~DELL2/IB90-1_pcs_release_after_reads.json"
PIN = "49bc13131d"
MEMBERS = {"custody_persist.py", "custody_write.py"}
START = "rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek="
BUILT = "7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns="
API_ID = "7k3ed8px20"
ROUTE = "POST /api/scoped/investor-reporting/custody-report"


def aws(root, *args):
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv
    p = subprocess.run(bash_argv(str(root / ".tools" / "aws"), *args), capture_output=True, timeout=60)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB90-1"))
        sys.exit(1)

    if cid not in ("IB90-1-AC1", "IB90-1-AC2"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r" % d.get("pin"))
    if cid == "IB90-1-AC1":
        if set(d.get("census_changed_members") or []) != MEMBERS:
            fail("census members %r" % d.get("census_changed_members"))
        if d.get("start_live_codesha") != START or d.get("built_sha") != BUILT:
            fail("start %r built %r" % (d.get("start_live_codesha"), d.get("built_sha")))
        for k, v in (("post_census_changed_members", 0), ("replan_changes", 0), ("rolled_back", False)):
            if d.get(k) != v:
                fail("%s is %r" % (k, d.get(k)))
        rp = d.get("replay") or {}
        if rp.get("identical") is not True or rp.get("negative_control_refused_by_both") is not True:
            fail("replay %r" % rp)
        rc, live = aws(root, "lambda", "get-function-configuration", "--function-name", "irpt-export-render",
                       "--query", "CodeSha256", "--output", "text")
        if rc or live != BUILT:
            fail("live CodeSha256 %r != built %s" % (live, BUILT))
        print("OK: pin %s, 2 members, live == built %s..., census 0, replan 0, replay identical" % (PIN, BUILT[:8]))
    else:
        if d.get("route_applied_after_function_live") is not True or d.get("route_replan") != 0:
            fail("route order %r replan %r" % (d.get("route_applied_after_function_live"), d.get("route_replan")))
        if d.get("ledger_closed") is not True:
            fail("ledger_closed %r" % d.get("ledger_closed"))
        rc, out = aws(root, "apigatewayv2", "get-routes", "--api-id", API_ID, "--query",
                      "Items[?RouteKey=='%s'].RouteKey" % ROUTE, "--output", "json")
        if rc or json.loads(out or "[]") != [ROUTE]:
            fail("route %r not live (rc %d, read %r)" % (ROUTE, rc, out))
        print("OK: route live after the function, route replan 0, ledger closed")
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
