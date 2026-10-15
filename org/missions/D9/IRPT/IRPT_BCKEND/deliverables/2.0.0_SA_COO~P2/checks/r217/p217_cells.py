"""IRPT_BCKEND workstream ~PI round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB217-1  IB-pr-579  the APPLY of the signed pair IB-pr-456 (+ ADDENDUM 1, reworded BEFORE record): irpt-ycharts-generate moved to the signed candidate by its Terraform path, with the applier's two refused bodies and one accepted request read before and after
    AC1  the gates: both halves signed, the packet sha256, no open marker or ledger naming the function, the start read equal to the signed live digest, the ledger entry naming the Branch B version, the BEFORE record
    AC2  the apply: the rebuilt digest equals the signed one, plan 1 change 0 destroy by safe-apply, the live function afterwards equals the built digest, re-plan 0, exactly the four members changed, the source-map rows of this function only, no rollback
    AC3  the after-read: import census clean, the AFTER refusal differs from the BEFORE one, the accepted request unchanged, the composition test, the health proof, the bound counters
"""
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
REC = D + "0.7.0_AE_CloudOps~IB2/IB217-1_apply_record.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_456_COMMENTARY_REQUESTED_ENDPOINT_READ_AND_COO_HALF.md"
COO_ADD = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_456_ADDENDUM_1_COMPOSITION_ADMISSION_COO_HALF.md"
CTO_ADD = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_456_ADDENDUM_1_COMPOSITION_ADMISSION_CTO_HALF.md"
PACKET_SHA = "2920ef90fa0640ee3f5f8ddbb52c8f52ef8556cd108bb5313644b8cdbed97700"
LIVE_B64 = "5TRFZf6Grgd9V9jWBVu2QDPRVbgfWBjsuuw8rtf8hRA="
BUILT_B64 = "3+fMEJhQ8enneLH30XiiV5VYEC4kk0+hZl0SFFsyM4k="
FN = "irpt-ycharts-generate"
MEMBERS = {"submission.py": "18aba4f0792f1f16c4ba14972b830fe670d4e91edef7f6c804a8fdb967d8b4cb",
           "acceptance.py": "abbdab4935097ea5d595c0e4abcde9cea977b12b15440b0ee70caa9eeb22895d",
           "contracts/AnalysisSubmissionRequest.schema.json": "1052343f111b70a9297fdfb14fc9c88894793ade68fd2d23b4076def968b1a7d",
           "composition_admission.py": "8d9b7aadc7c4db0b078737b155b4ec999d245d20c8bee83515c628639d0f64fd"}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB217"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def text(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def ac1(r):
    coo, add, cto = text(COO_HALF), text(COO_ADD), text(CTO_ADD)
    if "SIGNED for the blast radius" not in coo or "COO half" not in add:
        fail("the COO half and its addendum must read signed")
    if "SIGNED** on blob" not in cto and "SIGNED" not in cto:
        fail("the CTO addendum half must read SIGNED")
    g = r.get("gates") or {}
    if g.get("packet_sha256") != PACKET_SHA or g.get("both_halves_signed") is not True:
        fail("gates.packet_sha256 must equal the packet sha256 %s (re-hashed at the start) and both_halves_signed true" % PACKET_SHA)
    m = g.get("open_markers") or {}
    if not (is_int(m.get("worktrees_read")) and m["worktrees_read"] >= 1 and is_int(m.get("marker_files_read")) and m["marker_files_read"] >= 1
            and m.get("naming_the_function_with_open_trunk_ledger") == 0 and is_int(m.get("stale_views_naming_the_function"))):
        fail("gates.open_markers needs worktrees_read >= 1, marker_files_read >= 1, naming_the_function_with_open_trunk_ledger == 0 and an integer stale_views_naming_the_function")
    lg = g.get("open_ledgers") or {}
    if not (is_int(lg.get("ledger_files_read")) and lg["ledger_files_read"] >= 1 and lg.get("open_naming_the_function") == 0):
        fail("gates.open_ledgers needs ledger_files_read >= 1 and open_naming_the_function == 0")
    if (r.get("start_read") or {}).get("code_sha256") != LIVE_B64:
        fail("start_read.code_sha256 must equal the signed live digest %s" % LIVE_B64)
    led = str(r.get("ledger_entry", ""))
    if not led.startswith("org/critical_paths/change_management/") or not (ROOT / led).is_file():
        fail("ledger_entry must be an existing file under org/critical_paths/change_management/")
    bv = str(r.get("branch_b_version_id", "")).strip()
    if not bv or bv not in (ROOT / led).read_text(encoding="utf-8"):
        fail("branch_b_version_id must be named and written in the ledger entry")
    b = r.get("before") or {}
    if b.get("refusal_code") != "UNKNOWN_OR_SERVER_OWNED_FIELD" or b.get("twin_discriminates") is not True:
        fail("before.refusal_code must read UNKNOWN_OR_SERVER_OWNED_FIELD and before.twin_discriminates true (the body reached validation before authorization; otherwise STOP)")
    if not re.fullmatch(r"[0-9a-f]{64}", str(b.get("accepted_request_item_sha256", ""))):
        fail("before.accepted_request_item_sha256 must be 64-hex (the sha256 of the item read, never its content)")
    print("OK: gates and BEFORE record met; ledger %s" % led)


def ac2(r):
    a = r.get("apply") or {}
    if a.get("built_code_sha256") != BUILT_B64:
        fail("apply.built_code_sha256 must equal the signed candidate digest %s" % BUILT_B64)
    pl = a.get("plan") or {}
    if not (pl.get("change") == 1 and pl.get("destroy") == 0 and pl.get("add") == 0):
        fail("apply.plan must read add 0, change 1, destroy 0: %s" % pl)
    if a.get("safe_apply_rc") != 0 or a.get("path") != "terraform-safe-apply":
        fail("apply.path must be terraform-safe-apply with safe_apply_rc 0")
    af = r.get("after") or {}
    if af.get("code_sha256") != BUILT_B64 or af.get("replan_changes") != 0:
        fail("after.code_sha256 must equal the built digest and after.replan_changes must be 0")
    if sorted(af.get("changed_members") or []) != sorted(MEMBERS):
        fail("after.changed_members must be exactly %s: %s" % (sorted(MEMBERS), af.get("changed_members")))
    sm = r.get("source_map_rows") or {}
    if not (sm.get("committed") is True and sm.get("function") == FN and sm.get("siblings_changed") == 0 and is_int(sm.get("rows_changed")) and sm["rows_changed"] >= 1):
        fail("source_map_rows must read committed true, function %s, rows_changed >= 1 and siblings_changed 0" % FN)
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed apply (a Branch B restore is reported, not graded as a pass)")
    print("OK: the function moved to the signed candidate; re-plan 0; source-map rows of this function only")


def ac3(r):
    af = r.get("after") or {}
    if af.get("import_census_failed") != {}:
        fail("after.import_census_failed must be {} (the import census answered failed: {})")
    b = r.get("before") or {}
    if af.get("refusal_code") != "COMMENTARY_REQUESTED" or af.get("refusal_code") == b.get("refusal_code"):
        fail("after.refusal_code must read COMMENTARY_REQUESTED and differ from the BEFORE refusal (the release took)")
    if af.get("accepted_request_item_sha256") != b.get("accepted_request_item_sha256"):
        fail("the accepted request must read back unchanged: after.accepted_request_item_sha256 must equal the BEFORE value")
    ct = af.get("composition_test") or {}
    if not (is_int(ct.get("passed")) and ct["passed"] >= 6 and ct.get("failed") == 0):
        fail("after.composition_test must read passed >= 6 and failed 0 (tests/test_composition_refusal_cause.py on the candidate source)")
    if "UNEXERCISED LIVE" not in str(r.get("unexercised_live", "")):
        fail("unexercised_live must say, in words, that the released function accepting a submission is UNEXERCISED LIVE until the DEV FWD-1 run")
    h = r.get("health_proof") or {}
    if (h.get("deployed_member_sha256") or {}) != MEMBERS:
        fail("health_proof.deployed_member_sha256 must equal the built members %s" % MEMBERS)
    if not (str(h.get("window_start_utc", "")).strip() and str(h.get("window_end_utc", "")).strip() and str(h["window_end_utc"]) > str(h["window_start_utc"])):
        fail("health_proof needs a window with window_end_utc later than window_start_utc")
    if not (is_int(h.get("invocations_in_window")) and h["invocations_in_window"] >= 0 and h.get("errors_in_window") == 0):
        fail("health_proof.invocations_in_window must be an integer and errors_in_window must be 0")
    c = r.get("counters") or {}
    want = {"function_updates": 1, "lambda_invokes": 3, "iam_changes": 0, "route_changes": 0, "env_changes": 0, "table_writes": 0, "figures_written": 0,
            "files_deleted": 0, "sibling_functions_moved": 0, "vendor_requests_sent": 0, "jobs_queued": 0}
    for k, v in want.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: after-read, health proof and counters")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    arm = {"IB217-1-AC1": ac1, "IB217-1-AC2": ac2, "IB217-1-AC3": ac3}.get(CID)
    if arm is None:
        fail("unknown criterion %r" % CID)
    arm(load(REC))
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
