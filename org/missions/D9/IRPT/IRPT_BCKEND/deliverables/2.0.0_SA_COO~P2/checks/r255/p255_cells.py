"""IRPT_BCKEND workstream ~PM round 13 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the `mdpf-pipeline` leg of the served account-id HMAC list producer pair (the host role's IrptHmacListStageAssumeRole statement; packet blob e6d82eb3, ADDENDUM 1 blob cbcf940f, CTO half msg 10336 condition 1).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM11  IB-hm-11  one inline-policy change on the host role, read back
    AC1  the gates: both halves signed, the root's other writers counted (every live worktree read, denominator printed, no other ledger open on the root), the plan taken from a HEAD that holds both c5dd8b293a and 2d2c906b87, the ledger opened first
    AC2  the leg: the plan 0 add 1 change 0 destroy at the one address, applied through safe-apply, a clean re-plan, the policy read back with the new statement and the 49F statement unchanged
    AC3  the after-reads: the assume simulation arms with their controls, no manual QA run (deferred to the scheduled fire), the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IBhm11_apply_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_HMAC_LIST_PRODUCER_PAIR_PACKET_AND_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HMAC_LIST_PRODUCER_CTO_HALF.md"
BLOB = "e6d82eb31f2c84f0d3935846c4d2f3e6ddd7bf0d"
ADDRESS = "aws_iam_role_policy.mdpf_runner"
SID_NEW = "IrptHmacListStageAssumeRole"
SID_49F = "IrptDirectory49fAssumeSourcePrincipal"
ALLOWED = ("assume_the_stage_role",)
DENIED = ("assume_an_unrelated_role", "assume_the_stage_role_with_another_action_than_assume", "any_wildcard_resource_assume")
fail, load = P6.fail, P6.load


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def ac1(r):
    t = text(CTO_HALF)
    if BLOB[:8] not in t or "SIGNED" not in t.upper():
        fail("the CTO half must read SIGNED at blob %s" % BLOB[:8])
    if "SIGNED" not in text(PACKET).upper():
        fail("the COO half must read SIGNED")
    g = r.get("gates") or {}
    if g.get("packet_blob") != BLOB or g.get("both_halves_signed") is not True:
        fail("gates.packet_blob must be %s and both_halves_signed true" % BLOB)
    w = g.get("worktrees_read") or {}
    if not isinstance(w.get("count"), int) or w.get("count") < 1 or w.get("denominator_printed") is not True:
        fail("gates.worktrees_read must give an integer count of at least 1 and denominator_printed true")
    for k in ("no_other_ledger_open_on_the_root", "head_holds_c5dd8b293a", "head_holds_2d2c906b87", "ledger_opened_before_apply", "outside_the_fire_window"):
        if g.get(k) is not True:
            fail("gates.%s must be true" % k)
    print("OK: halves signed; the root's writers counted; HEAD holds both commits; ledger first")


def ac2(r):
    t = r.get("terraform") or {}
    p = t.get("plan") or {}
    if (p.get("add"), p.get("change"), p.get("destroy")) != (0, 1, 0) or p.get("addresses_changed") != [ADDRESS]:
        fail("terraform.plan must read add 0, change 1, destroy 0 at exactly [%s]" % ADDRESS)
    if t.get("applied_through") != "safe-apply" or t.get("replan_no_changes") is not True:
        fail("terraform must read applied_through safe-apply and replan_no_changes true")
    rb = r.get("policy_readback") or {}
    if rb.get("new_statement_sid") != SID_NEW or rb.get("new_statement_count") != 1:
        fail("policy_readback must read new_statement_sid %s and new_statement_count 1" % SID_NEW)
    if rb.get("statement_49f_unchanged") is not True or rb.get("other_statements_unchanged") is not True or rb.get("wildcard_in_new_statement") is not False:
        fail("policy_readback must read statement_49f_unchanged true, other_statements_unchanged true and wildcard_in_new_statement false")
    print("OK: 0/1/0 at the one address; safe-apply; clean re-plan; the new statement read back; the rest unchanged")


def ac3(r):
    s = r.get("simulation") or {}
    al, de = s.get("allowed") or {}, s.get("denied") or {}
    for k in ALLOWED:
        if al.get(k) != "allowed":
            fail("simulation.allowed.%s must read allowed" % k)
    for k in DENIED:
        if de.get(k) not in ("implicitDeny", "explicitDeny"):
            fail("simulation.denied.%s must read implicitDeny or explicitDeny (an allow is Branch B the same turn)" % k)
    q = r.get("qa") or {}
    if q.get("runs") != 0 or q.get("deferred_to_scheduled_fire") is not True:
        fail("qa must read runs 0 and deferred_to_scheduled_fire true (AMENDMENT 1: the refresh function has no one-firm payload, so no manual QA run is made; the next scheduled fire after the leg is read by the issuer)")
    k = r.get("counters") or {}
    want = {"other_iam_changes": 0, "other_terraform_roots_applied": 0, "lambda_invokes": 0, "secrets_printed": 0, "per_firm_numbers_recorded": 0}
    for key, v in want.items():
        if k.get(key) != v:
            fail("counters.%s must read %s, read %r" % (key, v, k.get(key)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the assume arm allowed and the three denied arms denied; no manual QA run; counters 0")


CHECKS = {"IBHM11-AC1": ac1, "IBHM11-AC2": ac2, "IBHM11-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p255_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
