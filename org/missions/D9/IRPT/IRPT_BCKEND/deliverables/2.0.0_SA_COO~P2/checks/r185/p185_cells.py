"""IRPT_BCKEND round 185 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB185-2  IB-pr-520  the APPLY of the signed pair IB-pr-518: irpt-ycharts-generate moved to the signed built digest by its Terraform path, then a health proof
    AC1  the gates: both halves signed at the packet sha256, no open marker or ledger naming the function, the start read equal to the signed live digest, the ledger entry naming the Branch B version
    AC2  the apply: the rebuilt digest equals the signed one, plan 1 change 0 destroy by safe-apply, the live function afterwards equals the built digest, re-plan 0, exactly the two members changed, the source-map row committed with the release
    AC3  the health proof: the deployed members equal the built ones, a metric and log read since the apply with zero errors, no invoke made, the bound counters
  IB185-1  IB-pr-519  irpt-export-render CENSUSED and rebuilt against its CURRENT live bytes with ONE staged contract re-pinned (ExportReceipt.schema.json, v1.2), BUILD ONLY, the stored-receipt census, and the never-widen packet
    AC1  the census: built twice identical, 0 signature mismatches, the live sha256 equals the source map's last deployed CodeSha256, the changed members exactly ExportReceipt.schema.json, the real source map restored, nothing uploaded
    AC2  the packet: Branch A, Branch B, the red list and its intersection, live and built sha256, both halves, rollback, the open-ledger sequencing, the CURRENT live CodeSha256, the two branches for receipts that lack the field, the receipt counts
    AC3  the arms, the receipt census and the ledgers: the v1.2 receipt refused by live and valid in the built, the receipt census (counts only, a read-only dry run), the branch consistent with the count, the bound counters
"""
import base64
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~368/IB185-1_release_census.json"
ARMS = D + "0.9.0_WK_IRPT_BCKEND~368/IB185-1_arms_receipts_ledgers.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~368/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-519.md"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-export-render"
MEMBERS = ["ExportReceipt.schema.json"]
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "receipts_written", "figures_written", "vendor_requests_sent")
BRANCHES = ("none_needed", "backfill_first", "optional_member")
REC2 = D + "0.7.0_AE_CloudOps~IB2/IB185-2_apply_record.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_518_CATALOGUE_FUNCTION_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_518_CATALOGUE_FUNCTION_CTO_HALF.md"
PACKET2_SHA = "7439728602c6b63b19e727ffacced7c57cb513c0abbd676febd1c778e4f7cd99"
LIVE2_B64 = "hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg="
BUILT2_B64 = "xP47NQDnZNZ8Lui1XQKUxUtTMTasR8Cj/A1sQnRDZYY="
MEMBER_SHAS = {"maintained_sources.py": "74c262b6db6d9d6c8c76b3668cad8d900f2977abe68325430836f26843ea2116",
               "templates.json": "87be046cf2bd0390a703d37be9e82a9037a3d867423e52e64a3db6415fe4728b"}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB185"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode()


def read_text_or_fail(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def apply_arms(arm):
    r = load(REC2)
    if arm == "AC1":
        coo = read_text_or_fail(COO_HALF)
        cto = read_text_or_fail(CTO_HALF)
        if PACKET2_SHA[:12] not in coo or "Signed: `2.0.0_SA_COO~P2` at" not in coo:
            fail("the COO half must carry the packet sha256 and its signed line")
        if PACKET2_SHA[:12] not in cto or "SIGNED** at packet sha256" not in cto:
            fail("the CTO half must read SIGNED at the packet sha256")
        g = r.get("gates") or {}
        if g.get("packet_sha256") != PACKET2_SHA or g.get("both_halves_signed") is not True:
            fail("gates.packet_sha256 must equal the signed packet sha256 (re-hashed at the start) and both_halves_signed true")
        m = g.get("open_markers") or {}
        if not (is_int(m.get("worktrees_read")) and m["worktrees_read"] >= 1 and is_int(m.get("marker_files_read")) and m["marker_files_read"] >= 1 and m.get("naming_the_function_with_open_trunk_ledger") == 0 and is_int(m.get("stale_views_naming_the_function")) and m["stale_views_naming_the_function"] >= 0):
            fail("gates.open_markers needs worktrees_read >= 1, marker_files_read >= 1, naming_the_function_with_open_trunk_ledger == 0 and an integer stale_views_naming_the_function (a marker OPEN at a stale worktree HEAD whose trunk ledger reads CLOSED is a stale view, counted and named, never acted on: NEVER-2)")
        lg = g.get("open_ledgers") or {}
        if not (is_int(lg.get("ledger_files_read")) and lg["ledger_files_read"] >= 1 and lg.get("open_naming_the_function") == 0):
            fail("gates.open_ledgers needs ledger_files_read >= 1 and open_naming_the_function == 0")
        if r.get("start_read", {}).get("code_sha256") != LIVE2_B64:
            fail("start_read.code_sha256 must equal the signed live digest %s" % LIVE2_B64)
        led = str(r.get("ledger_entry", ""))
        if not led.startswith("org/critical_paths/change_management/") or not (ROOT / led).is_file():
            fail("ledger_entry must be an existing file under org/critical_paths/change_management/")
        bv = str(r.get("branch_b_version_id", "")).strip()
        if not bv or bv not in (ROOT / led).read_text(encoding="utf-8"):
            fail("branch_b_version_id (the S3 version of the live zip) must be named and written in the ledger entry")
        print("OK: gates read met; ledger %s" % led)
    elif arm == "AC2":
        a = r.get("apply") or {}
        if a.get("built_code_sha256") != BUILT2_B64:
            fail("apply.built_code_sha256 must equal the signed built digest %s" % BUILT2_B64)
        pl = a.get("plan") or {}
        if not (pl.get("change") == 1 and pl.get("destroy") == 0 and pl.get("add") == 0):
            fail("apply.plan must read add 0, change 1, destroy 0: %s" % pl)
        if a.get("safe_apply_rc") != 0 or a.get("path") != "terraform-safe-apply":
            fail("apply.path must be terraform-safe-apply with safe_apply_rc 0")
        af = r.get("after") or {}
        if af.get("code_sha256") != BUILT2_B64 or af.get("replan_changes") != 0:
            fail("after.code_sha256 must equal the built digest and after.replan_changes must be 0")
        if sorted(af.get("changed_members") or []) != sorted(MEMBER_SHAS):
            fail("after.changed_members must be exactly %s: %s" % (sorted(MEMBER_SHAS), af.get("changed_members")))
        sm = r.get("source_map_row") or {}
        if not (sm.get("committed") is True and str(sm.get("pin", "")).startswith("0d0e9e1229") and sm.get("sha256") == MEMBER_SHAS["maintained_sources.py"]):
            fail("source_map_row must read committed true, pin 0d0e9e1229..., sha256 equal to the built maintained_sources.py member")
        if r.get("rollback_performed") is not False:
            fail("rollback_performed must be false for a landed apply (a Branch B restore is reported, not graded as a pass)")
        print("OK: the function moved to the signed digest; re-plan 0; source-map row committed")
    else:
        h = r.get("health_proof") or {}
        if (h.get("deployed_member_sha256") or {}) != MEMBER_SHAS:
            fail("health_proof.deployed_member_sha256 must equal the built members %s" % MEMBER_SHAS)
        if not (str(h.get("window_start_utc", "")).strip() and str(h.get("window_end_utc", "")).strip() and str(h["window_end_utc"]) > str(h["window_start_utc"])):
            fail("health_proof needs a window with window_end_utc later than window_start_utc")
        if not (is_int(h.get("invocations_in_window")) and h["invocations_in_window"] >= 0 and h.get("errors_in_window") == 0):
            fail("health_proof.invocations_in_window must be an integer and errors_in_window must be 0")
        c = r.get("counters") or {}
        want = {"function_updates": 1, "lambda_invokes": 0, "iam_changes": 0, "route_changes": 0, "env_changes": 0,
                "table_writes": 0, "figures_written": 0, "files_deleted": 0, "sibling_functions_moved": 0}
        for k, v in want.items():
            if c.get(k) != v:
                fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        print("OK: health proof and counters")
    print("%s PASS" % CID)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB185-2" and arm in ("AC1", "AC2", "AC3"):
        return apply_arms(arm)
    if cell != "IB185-1" or arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if arm == "AC1":
        rec = load(CENSUS)
        fn = rec.get("functions") or []
        if len(fn) != 1 or fn[0].get("function") != FN:
            fail("functions must hold exactly %s" % FN)
        f = fn[0]
        for k in ("built_sha256", "live_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(f.get(k, ""))):
                fail("%s must be 64-hex" % k)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256")
        if cur != b64_of_hex(f["live_sha256"]):
            fail("live_sha256 must equal the source map's last deployed CodeSha256 for %s (%s): the census is of a STALE live otherwise" % (FN, cur))
        if f.get("built_twice_identical") is not True or f.get("built_signature_mismatched") != 0 or f.get("live_signature_mismatched", 0) != 0:
            fail("built twice identical true and 0 signature mismatches on the built and live zips are required")
        bm, lm = f.get("built_attribute_mismatched"), f.get("live_attribute_mismatched")
        bl, ll = f.get("attribute_mismatch_lines_built"), f.get("attribute_mismatch_lines_live")
        if not is_int(bm) or not is_int(lm) or bm > lm or not isinstance(bl, list) or not isinstance(ll, list) or len(bl) != bm or len(ll) != lm or not set(bl) <= set(ll):
            fail("attribute mismatches: built must not exceed live and every built line must be a live line")
        cm = f.get("changed_members") or []
        names = sorted(str(m.get("name", "")).split("/")[-1] for m in cm)
        if names != MEMBERS:
            fail("the changed members must be exactly %s, read %s (any other member moving is a STOP, not a widening)" % (MEMBERS, names))
        for m in cm:
            if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
                fail("the built member's sha256 must equal the repo blob's at its pin")
        if rec.get("uploaded") is not False or not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
            fail("uploaded false and a pin_commit are required")
        sm = rec.get("source_map") or {}
        if not (sm.get("rows_edited_in_scratch_worktree") == 1 and sm.get("restored") is True and re.fullmatch(r"[0-9a-f]{64}", str(sm.get("sha256_before", ""))) and sm.get("sha256_before") == sm.get("sha256_after_restore")):
            fail("source_map: one staged_from row edited in the scratch worktree, then restored (sha256 before equals after restore)")
        print("OK: %s built twice identical against the CURRENT live; changed members %s; source map restored" % (FN, names))
    elif arm == "AC2":
        pk = ROOT / PACKET
        if not pk.is_file():
            fail("no %s" % PACKET)
        t = pk.read_text(encoding="utf-8", errors="replace")
        for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("the red list intersection stated", r"(?i)intersect"),
                          ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                          ("the COO half", r"(?i)COO half"), ("the CTO half", r"(?i)CTO half"), ("rollback", r"(?i)rollback|restore the live"),
                          ("the open-ledger sequencing", r"(?i)open (deploy )?ledger"),
                          ("the backfill branch", r"(?i)backfill"), ("the optional-member branch", r"(?i)optional"),
                          ("covered_account_ids", r"covered_account_ids"), ("never refuse a receipt that exists today", r"(?i)never refus")):
            if not re.search(pat, t):
                fail("the packet lacks: %s" % need)
        cur = (load(SRCMAP).get("functions") or {}).get(FN, {}).get("artifact_sha256", "")
        if cur[:12] not in t:
            fail("the packet must name the CURRENT live CodeSha256 (%s...)" % cur[:12])
        if len(t) < 3000:
            fail("the packet is shorter than 3000 characters")
        print("OK: the packet is complete and names the current live CodeSha256")
    else:
        r = load(ARMS)
        led = r.get("open_ledgers_naming_the_function")
        if not isinstance(led, list):
            fail("open_ledgers_naming_the_function must be a list (empty if none)")
        for x in led:
            if not x.get("ledger") or x.get("status") not in ("OPEN", "CLOSED", "SUPERSEDED", "HELD"):
                fail("each ledger needs a name and a status OPEN/CLOSED/SUPERSEDED/HELD")
        want = {"v12_receipt_on_live": "refused", "v12_receipt_on_built": "valid", "pre12_receipt_on_built": "refused", "pre12_receipt_on_live": "valid"}
        arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
        if arms != want:
            fail("arms must read %s, read %s" % (want, arms))
        rc = r.get("receipt_census") or {}
        for k in ("receipts_total", "receipts_with_field", "receipts_lacking_field", "unreadable_or_denied"):
            if not (is_int(rc.get(k)) and rc[k] >= 0):
                fail("receipt_census.%s must be an integer >= 0" % k)
        if rc["receipts_with_field"] + rc["receipts_lacking_field"] + rc["unreadable_or_denied"] != rc["receipts_total"]:
            fail("receipt_census: with + lacking + unreadable_or_denied must equal receipts_total")
        if rc.get("mode") != "dry_run_reads_only":
            fail("receipt_census.mode must be dry_run_reads_only (the backfill tool's default, no writes)")
        br = r.get("branch")
        if br not in BRANCHES:
            fail("branch must be one of %s" % (BRANCHES,))
        if (rc["receipts_lacking_field"] == 0 and rc["unreadable_or_denied"] == 0) != (br == "none_needed"):
            fail("branch none_needed if and only if no receipt lacks the field and none is unreadable (the CTO's rule: never refuse a receipt that exists today)")
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        for k in BOUND_ZERO:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: four arms, receipts %d total / %d lacking, branch %s, %d ledger(s), counters 0" % (rc["receipts_total"], rc["receipts_lacking_field"], br, len(led)))
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
