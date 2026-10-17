"""IRPT_BCKEND workstream ~PS round 7 (issuer 2.0.0_SA_COO~S2) -- the check of one APPLY order: IB-pr-551 hops 3 and 4 (the report route, the export bundle,
and the export role's read of the platinum filled object).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB247-1  IB-pr-616  APPLY hops 3 and 4 of the signed pair with its ADDENDUM 1 and 2: the report route on the reporting-read function, the export bundle, then the one IAM statement
    AC1  the gates: the pair's bytes, ADDENDUM 1 and 2 at their signed blobs with both halves SIGNED, hop 2's ledger closed, the BEFORE state equal to the order's, one change at a time
    AC2  hop 3 and hop 4a: each plan exactly as the order names, each function's CodeSha256 equal to its built zip, the report route present, no existing route changed
    AC3  hop 4b and the close: the fence row read back first, then exactly one statement added on the export role (two actions, one resource), the counters, no rollback, no long digit run
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC = D + "0.7.0_AE_CloudOps~IB2/IB247-1_release_record.json"
PAIR_COO = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_COO_HALF.md"
PAIR_CTO = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md"
A1_DRAFT = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_EXPORT_FILLED_READ_GRANT_DRAFT.md"
A1_COO = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_COO_HALF.md"
A2_COO = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_2_FENCE_ROW_COO_HALF.md"
A3_COO = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_3_GETOBJECT_ONLY_SHA256_REFUSAL_COO_HALF.md"
PACKET_SHA256_PREFIX = "7daa29f0fe10"
A1_DRAFT_BLOB = "9462b5ad35af646c96ede013f03d4449e8815033"
A1_COO_BLOB = "a09b331c4153cba7aea872001ed7998145d0e984"
A2_COO_BLOB = "b5c303ea69ffa4195ec441d455d9f1978c327678"
A3_COO_BLOB = "87a46d9cf370c293dae46a413cba213db721b5ef"
READ_FN, EXPORT_FN = "irpt-49f-reporting-read-lambda", "irpt-export-render"
READ_BEFORE = "WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0="
EXPORT_BEFORE = "5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4="
REPORT_ROUTE = "GET /api/scoped/investor-reporting/reporting/client/{client_id}/report"
STATEMENT_RESOURCE = "arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/client=*/filled_report.json"
STATEMENT_ACTIONS = ["s3:GetObject"]  # ADDENDUM 3: GetObjectVersion withdrawn (XA-20261017T010553Z-d493)
ROOT = Path(".")
CID = ""


def fail(msg):
    print("%s FAIL: %s" % (CID, msg))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no record at %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def text(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def blob(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return subprocess.run(["git", "hash-object", "--stdin"], input=f.read_bytes(), capture_output=True, timeout=60).stdout.decode().strip()


def plan_is(p, add, change, destroy):
    return isinstance(p, dict) and p.get("add") == add and p.get("change") == change and p.get("destroy") == destroy


def ac1(r):
    for rel, want in ((A1_DRAFT, A1_DRAFT_BLOB), (A1_COO, A1_COO_BLOB), (A2_COO, A2_COO_BLOB), (A3_COO, A3_COO_BLOB)):
        if blob(rel) != want:
            fail("%s must hold its signed blob %s" % (rel, want))
    if not text(PAIR_COO).strip():
        fail("the pair's COO half must be present")
    cto = text(PAIR_CTO)
    for key in (PACKET_SHA256_PREFIX, A1_DRAFT_BLOB[:10], A2_COO_BLOB[:10], A3_COO_BLOB[:10]):
        if key not in cto:
            fail("the CTO half must name the signed bytes %s" % key)
    if len(re.findall(r"(?<![A-Za-z])SIGNED", cto)) < 4:
        fail("the CTO half must read SIGNED for the pair and ADDENDUM 1, 2 and 3")
    g = r.get("gates") or {}
    if g.get("packet_sha256_prefix") != PACKET_SHA256_PREFIX or g.get("addendum_1_blob") != A1_DRAFT_BLOB or g.get("addendum_2_blob") != A2_COO_BLOB or g.get("addendum_3_blob") != A3_COO_BLOB:
        fail("gates must carry the packet prefix and the three addendum blobs")
    if g.get("all_halves_signed") is not True or g.get("hop2_ledger_closed") is not True:
        fail("gates.all_halves_signed and gates.hop2_ledger_closed must be true (hop 2 first, CTO msg 9614)")
    if g.get("one_change_at_a_time") is not True or not isinstance(g.get("open_deploys_worktrees_read"), int) or g["open_deploys_worktrees_read"] < 1:
        fail("gates.one_change_at_a_time must be true and the worktree union of .open_deploys must be printed with a denominator of 1 or more (CVO msg 8750)")
    if g.get("export_bundle_with_sha256_refusal_live_and_read_back") is not True:
        fail("gates.export_bundle_with_sha256_refusal_live_and_read_back must be true BEFORE the IAM statement (CTO half of ADDENDUM 3: otherwise the old code passes a VersionId the new grant no longer allows)")
    b = g.get("before") or {}
    if b.get("read_function_sha256") != READ_BEFORE or b.get("export_function_sha256") != EXPORT_BEFORE or b.get("report_route_absent") is not True:
        fail("gates.before must equal the order's BEFORE state (read %s, export %s, report route absent); a different value is a STOP and a re-cut" % (READ_BEFORE, EXPORT_BEFORE))
    print("OK: the gates: the pair and ADDENDUM 1 and 2 at their signed bytes, hop 2 closed, one change at a time, the BEFORE state equal")


def ac2(r):
    h3, h4 = r.get("h3") or {}, r.get("h4a") or {}
    if h3.get("function") != READ_FN or not h3.get("built_sha256") or h3.get("after_sha256") != h3.get("built_sha256"):
        fail("h3 must record the read function, the built zip's base64 sha256 and the live CodeSha256 equal to it")
    if h3.get("route") != REPORT_ROUTE or h3.get("route_present_after") is not True or h3.get("existing_routes_changed") != 0:
        fail("h3 must read the report route %s present after and 0 existing routes changed" % REPORT_ROUTE)
    p3 = h3.get("plan") or {}
    if p3.get("add", 0) != 1 or p3.get("destroy") != 0 or not (isinstance(p3.get("resources"), list) and p3["resources"]):
        fail("h3.plan must add exactly one resource (the route) with 0 destroy and name its resources")
    if h4.get("function") != EXPORT_FN or not h4.get("built_sha256") or h4.get("after_sha256") != h4.get("built_sha256"):
        fail("h4a must record the export function, the built zip's base64 sha256 and the live CodeSha256 equal to it")
    if h4.get("sha256_before") != EXPORT_BEFORE or h4.get("pass_switch_unchanged") is not True:
        fail("h4a must record the BEFORE sha and the filled-report switch left unchanged (it stays OFF here)")
    print("OK: hop 3 and hop 4a: each function at its built zip, the report route present, no existing route changed")


def ac3(r):
    h = r.get("h4b") or {}
    fence = h.get("fence_row") or {}
    if fence.get("second_row_present") is not True or fence.get("regenerated_and_read_back") is not True:
        fail("h4b.fence_row must read second_row_present true and regenerated_and_read_back true BEFORE the IAM statement (ADDENDUM 2, CTO msg 9576)")
    if h.get("role_statement_before") != "absent":
        fail("h4b.role_statement_before must read absent (STEP 0); a present grant voids ADDENDUM 1")
    if not plan_is(h.get("plan"), 0, 1, 0) or h.get("statements_added") != 1 or h.get("statements_removed") != 0:
        fail("h4b.plan must read exactly 0 add / 1 change / 0 destroy with 1 statement added and none removed")
    s = h.get("statement") or {}
    if s.get("resource") != STATEMENT_RESOURCE or sorted(s.get("actions") or []) != sorted(STATEMENT_ACTIONS) or s.get("effect") != "Allow":
        fail("h4b.statement must be Allow, the two read actions, on exactly %s" % STATEMENT_RESOURCE)
    if h.get("replan_changes") != 0:
        fail("h4b.replan_changes must read 0")
    c = r.get("counters") or {}
    for k in ("rollback_performed", "console_edits", "put_role_policy_calls", "switch_changes", "other_roles_changed", "second_firm_prefixes"):
        want = False if k == "rollback_performed" else 0
        if c.get(k) != want:
            fail("counters.%s must read %r, read %r" % (k, want, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the fence row read back first, exactly one statement added on the export role, the counters, no rollback")


CHECKS = {"IB247-1-AC1": ac1, "IB247-1-AC2": ac2, "IB247-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p247_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT, CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
