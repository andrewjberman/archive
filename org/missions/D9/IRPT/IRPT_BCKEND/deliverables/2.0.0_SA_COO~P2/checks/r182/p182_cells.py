"""IRPT_BCKEND round 182 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB182-1  IB-pr-516  the APPLY of the signed irpt-directory-search pair (IB-pr-515): the one function moved by its digest-gated Terraform path, then one synthetic tail search
    AC1  the gates: both halves signed at the packet sha256, step 0 MATCH, no open marker on any live worktree, the start read equals the signed live digest, the ledger entry, the Branch B version named
    AC2  the apply: the rebuilt digest equals the signed one, the plan is 1 change and 0 destroy, the live function after equals the built digest, the re-plan is 0 changes, handler.py is the only changed member
    AC3  the direct proof (one synthetic tail search and its resolve, both reads) and the bound counters
"""
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
REC = D + "0.7.0_AE_CloudOps~IB2/IB182-1_apply_record.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~365/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-515.md"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_515_DIRECTORY_SEARCH_REFRESHED_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_515_DIRECTORY_SEARCH_REFRESHED_CTO_HALF.md"
PACKET_SHA = "3c369b9086b3453fdb40efcc94655eb17933d2c65c35f248dd6255cb21db6888"
LIVE_B64 = "tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w="
BUILT_B64 = "rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw="
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB182"))
    sys.exit(1)


def read_text(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def load(rel):
    try:
        return json.loads(read_text(rel))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB182-1" or arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    r = load(REC)
    if arm == "AC1":
        coo, cto = read_text(COO_HALF), read_text(CTO_HALF)
        if PACKET_SHA[:12] not in coo or "Signed: `2.0.0_SA_COO~P2` at" not in coo:
            fail("the COO half must carry the packet sha256 and the line 'Signed: `2.0.0_SA_COO~P2` at'")
        if PACKET_SHA[:12] not in cto or "SIGNED** at packet sha256" not in cto:
            fail("the CTO half must read SIGNED at the packet sha256")
        g = r.get("gates") or {}
        if g.get("packet_sha256") != PACKET_SHA:
            fail("gates.packet_sha256 must equal the signed packet sha256 (re-hashed at the start of the apply)")
        if g.get("both_halves_signed") is not True or g.get("step0_match") is not True:
            fail("gates.both_halves_signed and gates.step0_match must be true")
        m = g.get("open_markers") or {}
        if not (is_int(m.get("worktrees_read")) and m["worktrees_read"] >= 1 and is_int(m.get("marker_files_read")) and m["marker_files_read"] >= 1 and m.get("naming_the_function") == 0):
            fail("gates.open_markers needs worktrees_read >= 1, marker_files_read >= 1 and naming_the_function == 0 (a count over every live worktree with its denominator)")
        if r.get("start_read", {}).get("code_sha256") != LIVE_B64:
            fail("start_read.code_sha256 must equal the signed live digest %s" % LIVE_B64)
        led = str(r.get("ledger_entry", ""))
        if not led.startswith("org/critical_paths/change_management/") or not (ROOT / led).is_file():
            fail("ledger_entry must be an existing file under org/critical_paths/change_management/")
        bv = str(r.get("branch_b_version_id", "")).strip()
        if not bv or bv not in (ROOT / led).read_text(encoding="utf-8"):
            fail("branch_b_version_id (the S3 version of the live zip) must be named and written in the ledger entry")
        print("OK: gates read met; ledger %s" % led)
    elif arm == "AC2":
        a = r.get("apply") or {}
        if a.get("built_code_sha256") != BUILT_B64:
            fail("apply.built_code_sha256 must equal the signed built digest %s (any other digest is never uploaded)" % BUILT_B64)
        pl = a.get("plan") or {}
        if not (pl.get("change") == 1 and pl.get("destroy") == 0 and pl.get("add") == 0):
            fail("apply.plan must read add 0, change 1, destroy 0: %s" % pl)
        if a.get("safe_apply_rc") != 0 or a.get("path") != "terraform-safe-apply":
            fail("apply.path must be terraform-safe-apply with safe_apply_rc 0")
        af = r.get("after") or {}
        if af.get("code_sha256") != BUILT_B64 or af.get("replan_changes") != 0:
            fail("after.code_sha256 must equal the built digest and after.replan_changes must be 0")
        if af.get("changed_members") != ["handler.py"]:
            fail("after.changed_members must be exactly ['handler.py']: %s" % af.get("changed_members"))
        if r.get("rollback_performed") is not False:
            fail("rollback_performed must be false for a landed apply (a Branch B restore is reported, not graded as a pass)")
        print("OK: the function moved to the signed digest; re-plan 0")
    else:
        p = r.get("direct_proof") or {}
        if p.get("operation") != "search" or p.get("directory") != "synthetic" or p.get("persisted") is not False:
            fail("direct_proof must be a synthetic-directory search that persisted nothing")
        if not (p.get("account_entries") == 1 and p.get("kind") == "ACCOUNT" and p.get("permitted_account_count") == 1):
            fail("direct_proof must read one ACCOUNT entry with permitted_account_count 1")
        if p.get("resolve_account_count") != 1:
            fail("the resolve of that entry must return exactly one account")
        if not re.fullmatch(r"[0-9a-f]{64}", str(p.get("response_sha256", ""))):
            fail("direct_proof.response_sha256 must be a 64-hex digest (the response itself is not recorded)")
        c = r.get("counters") or {}
        want = {"function_updates": 1, "lambda_invokes": 2, "iam_changes": 0, "route_changes": 0, "env_changes": 0,
                "table_writes": 0, "figures_written": 0, "files_deleted": 0, "sibling_functions_moved": 0}
        for k, v in want.items():
            if c.get(k) != v:
                fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
        blob = json.dumps(r)
        if re.search(r"\d{12,}", re.sub(r"[0-9a-f]{64}", "", blob)):
            fail("the record carries a long digit run (an account or client number)")
        print("OK: direct proof and counters")
    print("%s PASS" % CID)


main()
