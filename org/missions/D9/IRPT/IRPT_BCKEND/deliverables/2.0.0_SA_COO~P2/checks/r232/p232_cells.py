"""IRPT_BCKEND workstream ~PO round 7 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the Scope account feed's IAM pair.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB232-1  IB-pr-600  aws_iam_role_policy.inf_gold_layer_scope_feed is applied to the inf gold runner role, and its after-reads are read
    AC1  the gates: both halves signed at the packet blob, the plan shape 1/0/0 at the one address, the ARNs equal to address() output, one change at a time, the ledger opened first
    AC2  the apply: through safe-apply, 1 added 0 changed 0 destroyed, a re-plan with no changes, the policy read back from the role
    AC3  the after-reads: the four allowed and the four denied simulation arms, the exists() read on the runner reading ABSENT, the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB232-1_apply_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR.md"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_SCOPE_FEED_IAM_PAIR_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SCOPE_FEED_IAM_PAIR_CTO_HALF.md"
BLOB = "cea5395ee74000806a28ab8eca32156e0af94639"
ADDRESS = "aws_iam_role_policy.inf_gold_layer_scope_feed"
fail, load, is_int = P6.fail, P6.load, P6.is_int
ALLOWED = ("put_bronze_feed_key", "put_silver_feed_key", "get_feed_key", "list_with_feed_prefix")
DENIED = ("put_sibling_fact_positions_key", "delete_feed_key", "put_other_bucket", "list_sibling_prefix")


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def hex64(x, what):
    if not re.fullmatch(r"[0-9a-f]{64}", str(x)):
        fail("%s must be a 64-hex sha256" % what)


def ac1(r):
    for rel in (COO_HALF, CTO_HALF):
        t = text(rel)
        if BLOB[:10] not in t or "SIGNED" not in t.upper() and "GIVEN" not in t.upper():
            fail("both halves must read SIGNED or GIVEN at the packet blob %s: %s" % (BLOB[:10], rel))
    g = r.get("gates") or {}
    if g.get("packet_blob") != BLOB or g.get("both_halves_signed") is not True:
        fail("gates.packet_blob must be %s and both_halves_signed true" % BLOB)
    p = g.get("plan") or {}
    if (p.get("add"), p.get("change"), p.get("destroy")) != (1, 0, 0) or p.get("addresses") != [ADDRESS]:
        fail("gates.plan must read add 1, change 0, destroy 0 at exactly [%s]" % ADDRESS)
    a = g.get("arns") or {}
    if a.get("equal_address_output") is not True or a.get("prefixes_printed") is not True:
        fail("gates.arns must print the address() prefixes and read equal_address_output true (character for character)")
    if g.get("one_change_at_a_time") is not True:
        fail("gates.one_change_at_a_time must be true (no other open ledger or window on the inf-pipeline root)")
    if g.get("ledger_opened_before_apply") is not True:
        fail("gates.ledger_opened_before_apply must be true (NEVER-2)")
    print("OK: gates met; plan 1/0/0 at the one address")


def ac2(r):
    a = r.get("apply") or {}
    if a.get("through") != "safe-apply":
        fail("apply.through must read safe-apply")
    if (a.get("added"), a.get("changed"), a.get("destroyed")) != (1, 0, 0):
        fail("apply must read added 1, changed 0, destroyed 0")
    if a.get("replan_no_changes") is not True:
        fail("apply.replan_no_changes must be true")
    rb = a.get("policy_readback") or {}
    if rb.get("statement_count") != 2 or rb.get("delete_action_present") is not False or rb.get("kms_action_present") is not False:
        fail("policy_readback must read statement_count 2, delete_action_present false and kms_action_present false")
    hex64(rb.get("policy_sha256"), "policy_readback.policy_sha256")
    if a.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed apply (Branch B is reported, not graded as a pass)")
    print("OK: applied 1/0/0 through safe-apply; re-plan clean; policy read back")


def ac3(r):
    s = r.get("simulation") or {}
    al, de = s.get("allowed") or {}, s.get("denied") or {}
    for k in ALLOWED:
        if al.get(k) != "allowed":
            fail("simulation.allowed.%s must read allowed" % k)
    for k in DENIED:
        if de.get(k) not in ("implicitDeny", "explicitDeny"):
            fail("simulation.denied.%s must read implicitDeny or explicitDeny (an allow is Branch B the same turn)" % k)
    c = s.get("controls") or {}
    if c.get("inf_bucket_allowed") is not True or c.get("unrelated_bucket_denied") is not True:
        fail("simulation.controls must read inf_bucket_allowed true and unrelated_bucket_denied true")
    e = r.get("exists_read") or {}
    if e.get("ran_on_runner") is not True or e.get("key_was_known_absent") is not True or e.get("answer") != "ABSENT":
        fail("exists_read must read ran_on_runner true, key_was_known_absent true and answer ABSENT (CTO half condition 3: a 403 is a STOP and a row)")
    k = r.get("counters") or {}
    want = {"function_updates": 0, "lambda_invokes": 0, "other_iam_changes": 0, "schedule_changes": 0, "keys_written": 0, "existing_keys_changed": 0, "secrets_printed": 0}
    for key, v in want.items():
        if k.get(key) != v:
            fail("counters.%s must read %s, read %r" % (key, v, k.get(key)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: four allowed and four denied arms; exists() on the runner reads ABSENT; counters 0")


CHECKS = {"IB232-1-AC1": ac1, "IB232-1-AC2": ac2, "IB232-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p232_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
