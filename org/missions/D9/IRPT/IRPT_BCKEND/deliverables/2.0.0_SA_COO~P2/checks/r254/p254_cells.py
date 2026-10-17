"""IRPT_BCKEND workstream ~PM round 12 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the served account-id HMAC list producer's legs in the `directory` root (pair packet blob e6d82eb3, ADDENDUM 1 blob cbcf940f).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM5  IB-hm-5  the bundle, the zip, the directory-root apply, the secret put and one QA run, read back
    AC1  the gates: both halves of the packet and of the addendum signed at their blobs, one change at a time, the ledger opened before the first write, both Branch B versions named before any write, outside the fire window
    AC2  the legs: the bundle minted through safe-deploy with 12 of 12 members equal to HEAD, the zip digest equal to the pin, the plan 3 add 1 change 0 destroy at the named addresses, applied through safe-apply, a clean re-plan, the three environment keys present
    AC3  the after-reads: the simulation arms, the secret put once and never printed, ONE QA run read as PASS or FAIL per check, the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IBhm5_apply_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_HMAC_LIST_PRODUCER_PAIR_PACKET_AND_COO_HALF.md"
COO_ADD = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_HMAC_LIST_PRODUCER_PAIR_ADDENDUM_1_PINS_ORDER_AND_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HMAC_LIST_PRODUCER_CTO_HALF.md"
CTO_ADD = CTO_HALF  # the CTO signed ADDENDUM 1 in the same half file (msg 10358)
BLOB = "e6d82eb31f2c84f0d3935846c4d2f3e6ddd7bf0d"
ADD_BLOB = "cbcf940fbc93deb8a67d9805a6eba5d290f8726f"
ZIP_PIN = "I7T8wRYmv11nytYpD7i+4XCwwvy6JUaB3fdsgtHyXmA="
BUNDLE_BEFORE = "W2WragrP52i8M7MfL22oXVPuHsTjyVLO"
ADDS = ["aws_iam_role.irpt_hmac_list_stage", "aws_iam_role_policy.irpt_hmac_list_stage", "aws_secretsmanager_secret.irpt_hmac_list"]
CHANGES = ["module.irpt_directory_refresh.aws_lambda_function.this"]
ENV_KEYS = ["IRPT_HMAC_LIST_URI_MAP", "IRPT_HMAC_ROLE_ARN", "IRPT_HMAC_SECRET_ID"]
ALLOWED = ("get_the_one_secret", "put_each_of_the_three_list_keys")
DENIED = ("get_object_on_a_list_key", "list_bucket_on_the_list_prefix", "delete_object_on_a_list_key", "put_on_a_neighbouring_key", "get_any_other_secret")
QA = ("list_key_exists_and_fresh", "line_count_equals_the_session_count", "no_plain_sha256_of_a_known_fake_id", "directory_output_byte_unchanged")
fail, load = P6.fail, P6.load


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def ac1(r):
    for rel, blob in ((CTO_HALF, BLOB), (CTO_ADD, ADD_BLOB)):
        t = text(rel)
        if blob[:8] not in t or "SIGNED" not in t.upper():
            fail("the CTO half must read SIGNED at blob %s: %s" % (blob[:8], rel))
    for rel in (PACKET, COO_ADD):
        if "SIGNED" not in text(rel).upper():
            fail("the COO half must read SIGNED: %s" % rel)
    g = r.get("gates") or {}
    if g.get("packet_blob") != BLOB or g.get("addendum_blob") != ADD_BLOB or g.get("both_halves_signed") is not True:
        fail("gates.packet_blob must be %s, gates.addendum_blob %s and both_halves_signed true" % (BLOB, ADD_BLOB))
    for k in ("one_change_at_a_time", "ledger_opened_before_first_write", "outside_the_fire_window", "trading_calendar_tests_printed_before_mint"):
        if g.get(k) is not True:
            fail("gates.%s must be true" % k)
    b = g.get("branch_b_versions_named_before_write") or {}
    if b.get("bundle") != BUNDLE_BEFORE or b.get("zip") is not True:
        fail("gates.branch_b_versions_named_before_write must name the bundle version %s and zip true" % BUNDLE_BEFORE)
    print("OK: halves signed at both blobs; one change at a time; ledger first; Branch B versions named; outside the fire window")


def ac2(r):
    b = r.get("bundle") or {}
    if b.get("minted_through") != "safe-deploy" or b.get("members") != 12 or b.get("members_equal_head") != 12:
        fail("bundle must read minted_through safe-deploy, members 12 and members_equal_head 12")
    if b.get("version_before") != BUNDLE_BEFORE or not b.get("version_after") or b.get("version_after") == BUNDLE_BEFORE:
        fail("bundle.version_before must be %s and version_after a different non-empty id" % BUNDLE_BEFORE)
    z = r.get("zip") or {}
    if z.get("built_sha256_b64") != ZIP_PIN or z.get("equals_pin") is not True or z.get("head_object_verified") is not True:
        fail("zip must read built_sha256_b64 %s, equals_pin true and head_object_verified true" % ZIP_PIN)
    t = r.get("terraform") or {}
    p = t.get("plan") or {}
    if (p.get("add"), p.get("change"), p.get("destroy")) != (3, 1, 0) or sorted(p.get("addresses_added") or []) != ADDS or p.get("addresses_changed") != CHANGES:
        fail("terraform.plan must read add 3 at %s, change 1 at %s, destroy 0" % (ADDS, CHANGES))
    if t.get("applied_through") != "safe-apply" or t.get("replan_no_changes") is not True:
        fail("terraform must read applied_through safe-apply and replan_no_changes true")
    if sorted(t.get("env_keys_present") or []) != ENV_KEYS:
        fail("terraform.env_keys_present must be exactly %s (names only)" % ENV_KEYS)
    print("OK: bundle 12 of 12 equal HEAD; zip digest equals the pin; plan 3/1/0 at the named addresses; safe-apply; clean re-plan")


def ac3(r):
    s = r.get("simulation") or {}
    al, de = s.get("allowed") or {}, s.get("denied") or {}
    for k in ALLOWED:
        if al.get(k) != "allowed":
            fail("simulation.allowed.%s must read allowed" % k)
    for k in DENIED:
        if de.get(k) not in ("implicitDeny", "explicitDeny"):
            fail("simulation.denied.%s must read implicitDeny or explicitDeny (an allow is Branch B the same turn)" % k)
    sec = r.get("secret") or {}
    if sec.get("value_put_count") != 1 or sec.get("version_count") != 1 or sec.get("value_printed") is not False:
        fail("secret must read value_put_count 1, version_count 1 and value_printed false")
    q = r.get("qa") or {}
    if q.get("runs") != 1:
        fail("qa.runs must be 1")
    for k in QA:
        if q.get(k) != "PASS":
            fail("qa.%s must read PASS" % k)
    if not isinstance(q.get("assume_succeeded_before_mdpf_leg"), bool):
        fail("qa.assume_succeeded_before_mdpf_leg must be recorded as a true/false fact")
    k = r.get("counters") or {}
    want = {"other_lambda_invokes": 0, "other_iam_changes": 0, "keys_written_outside_the_three": 0, "existing_keys_changed": 0, "secrets_printed": 0, "per_firm_numbers_recorded": 0}
    for key, v in want.items():
        if k.get(key) != v:
            fail("counters.%s must read %s, read %r" % (key, v, k.get(key)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: simulation arms; secret put once and never printed; one QA run all PASS; counters 0")


CHECKS = {"IBHM5-AC1": ac1, "IBHM5-AC2": ac2, "IBHM5-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p254_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
