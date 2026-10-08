"""IRPT_BCKEND round 77 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-364 (the custody release pair at pin
1e0cdaf90c: irpt-export-render code, then the one api-root route custody-report-read; packet blob 2af2b30af8, COO half at
deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_363_CUSTODY_RELEASE_COO_HALF.md, CTO half @652141d7cc).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Finishes inside 120 s (reads one file, one live CodeSha256, one route list).

  IB77-1-AC1  the committed IB77-1_release_after_reads.json reads: pin 1e0cdaf90c; census changed members EXACTLY entry.py,
              submit_async.py, custody_read.py; start_live_codesha equals the rollback target aRCgH9B0...; built_sha == live
              CodeSha256 (re-read live by this check); post_census_changed_members 0; replan_changes_export 0 and replan_changes_api 0;
              the custody-report route is live on api 7k3ed8px20 (re-read live by this check); ledger_closed true; rolled_back false.
              Base: FAIL (no file).
  IB77-1-AC2  the same file reads: other_firm_refused true with other_firm_code OBJECT_NOT_COVERED and other_firm_body_bytes 0;
              route_unauth_refused true; opal_by_ref true, or "OPEN-BY-DESIGN" with retained_custody_reports 0 and a non-empty
              open_leg_discharge. Base: FAIL (no file).
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/deliverables/0.9.0_WK_IRPT_BCKEND~172/IB77-1_release_after_reads.json"
PIN = "1e0cdaf90c"
THREE = {"entry.py", "submit_async.py", "custody_read.py"}
ROLLBACK_SHA = "aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw="
API_ID = "7k3ed8px20"
ROUTE = "GET /api/scoped/investor-reporting/custody-report/{reportId}"
OPEN = "OPEN-BY-DESIGN"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB77"))
        sys.exit(1)

    if cid not in ("IB77-1-AC1", "IB77-1-AC2"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    if not str(d.get("pin", "")).startswith(PIN):
        fail("pin %r is not %s" % (d.get("pin"), PIN))

    if cid == "IB77-1-AC2":
        if d.get("other_firm_refused") is not True or d.get("other_firm_code") != "OBJECT_NOT_COVERED":
            fail("other firm: refused %r code %r" % (d.get("other_firm_refused"), d.get("other_firm_code")))
        if d.get("other_firm_body_bytes") != 0:
            fail("other firm body bytes %r" % d.get("other_firm_body_bytes"))
        if d.get("route_unauth_refused") is not True:
            fail("route_unauth_refused is %r" % d.get("route_unauth_refused"))
        o = d.get("opal_by_ref")
        if o is True:
            pass
        elif o == OPEN:
            if d.get("retained_custody_reports") != 0:
                fail("opal_by_ref OPEN-BY-DESIGN but retained_custody_reports %r" % d.get("retained_custody_reports"))
            if not str(d.get("open_leg_discharge", "")).strip():
                fail("opal_by_ref OPEN-BY-DESIGN without open_leg_discharge")
        else:
            fail("opal_by_ref is %r" % o)
        print("OK: other firm refused OBJECT_NOT_COVERED with no body; unauthenticated refused; opal_by_ref %r" % o)
        print("%s PASS" % cid)
        return

    if set(d.get("census_changed_members") or []) != THREE:
        fail("census members %r != the three signed" % sorted(d.get("census_changed_members") or []))
    if d.get("start_live_codesha") != ROLLBACK_SHA:
        fail("start live CodeSha256 %r is not the signed rollback target" % d.get("start_live_codesha"))
    if d.get("rolled_back") is not False:
        fail("rolled_back is %r" % d.get("rolled_back"))
    if d.get("ledger_closed") is not True:
        fail("ledger_closed is %r" % d.get("ledger_closed"))
    for k in ("post_census_changed_members", "replan_changes_export", "replan_changes_api"):
        if d.get(k) != 0:
            fail("%s is %r" % (k, d.get(k)))
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv
    aws = str(root / ".tools" / "aws")
    r = subprocess.run(bash_argv(aws, "lambda", "get-function-configuration", "--function-name", "irpt-export-render", "--query",
                                 "CodeSha256", "--output", "text"), capture_output=True, timeout=60)
    live = r.stdout.decode("utf-8", "replace").strip()
    if r.returncode or not live:
        fail("live CodeSha256 unreadable rc %d" % r.returncode)
    built = str(d.get("built_sha", ""))
    if built not in (live, base64.b64decode(live).hex()):
        fail("built %r != live CodeSha256 %r" % (built, live))
    # AMENDMENT 2 (row D2-W172-S4): the unfiltered 6,368-byte route list crashes python -> bash .tools/aws -> aws.exe
    # (0xC0000005) on dell2; the query filters server-side to the one route key, and the total count is read separately.
    r = subprocess.run(bash_argv(aws, "apigatewayv2", "get-routes", "--api-id", API_ID, "--query",
                                 "Items[?RouteKey=='%s'].RouteKey" % ROUTE, "--output", "json"), capture_output=True, timeout=50)
    if r.returncode:
        fail("get-routes (filtered) rc %d" % r.returncode)
    keys = json.loads(r.stdout.decode("utf-8", "replace") or "[]")
    n = subprocess.run(bash_argv(aws, "apigatewayv2", "get-routes", "--api-id", API_ID, "--query", "length(Items)",
                                 "--output", "text"), capture_output=True, timeout=50)
    # length(Items) under the CLI's auto-pagination prints one count PER PAGE (rule 22a); the total is their sum.
    pages = n.stdout.decode("utf-8", "replace").split() if n.returncode == 0 else []
    total = str(sum(int(x) for x in pages)) if pages and all(x.isdigit() for x in pages) else "unread rc %d" % n.returncode
    if keys != [ROUTE]:
        fail("route %r not live (filtered read %r; %s routes on the api)" % (ROUTE, keys, total))
    print("OK: pin %s, 3 of 3 members, live CodeSha256 == built, route live (1 match of %s routes), replans 0, ledger closed" % (PIN, total))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
