"""IRPT_BCKEND workstream ~PM round 18 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the Cottonwood retained-key release (the directory wedge fix, the runner rule and the refresh Lambda rule) under the signed pair (packet blob 51c382f112, CTO half @1087ec58ec, msg 11103).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBCW6  IB-cw-6  the runner bundle, the refresh Lambda zip and the directory-root apply, read back
    AC1  the gates: the CTO half reads SIGNED at the packet blob, the COO half is present, one change at a time, the ledger opened before the first write, both Branch B versions named before any write, the time outside the fire band and the gateway window, the pre-mint tests printed
    AC2  the legs: the bundle minted through safe-deploy with every member equal to HEAD, the zip digest equal to the pin, the plan 0 add 1 change 0 destroy at the named address, applied through safe-apply, a clean re-plan, the function's CodeSha256 read back equal to the pin
    AC3  the after-reads: no Lambda invoke, no fire by hand, nothing written outside the two artifacts, the rollback versions recorded, no long digit run
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IBcw6_apply_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_COTTONWOOD_RETAINED_KEY_PAIR_PACKET_AND_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_RETAINED_KEY_CTO_HALF.md"
BLOB = "51c382f11213b8003b122fea6262f09c7bda0b54"
REFRESH_BLOB = "304eb35580ee108f0884477894ba7eb2808e09bb"
RUNNER_BLOB = "f2d2329d39a11c4f0209e36df429a27390560c6c"
ZIP_PIN = "3YK/4/pGsXjLNoYWmG2mqrps8y+t2QUiLiPt6osNT5g="
BUNDLE_BEFORE = "7ywFHFyMHW5JcS7hjeGIIAWsNyyOOVMB"
ZIP_BEFORE_SHA = "I7T8wRYmv11nytYpD7i+4XCwwvy6JUaB3fdsgtHyXmA="
CHANGES = ["module.irpt_directory_refresh.aws_lambda_function.this"]
fail, load = P6.fail, P6.load


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def ac1(r):
    t = text(CTO_HALF)
    if BLOB[:10] not in t or "SIGNED" not in t.upper():
        fail("the CTO half must read SIGNED at packet blob %s: %s" % (BLOB[:10], CTO_HALF))
    if "SIGNED" not in text(PACKET).upper():
        fail("the COO half must read SIGNED: %s" % PACKET)
    g = r.get("gates") or {}
    if g.get("packet_blob") != BLOB or g.get("both_halves_signed") is not True:
        fail("gates.packet_blob must be %s and both_halves_signed true" % BLOB)
    pins = g.get("pins_equal_head") or {}
    if pins.get("refresh_py") != REFRESH_BLOB[:12] or pins.get("directory_runner_py") != RUNNER_BLOB[:12]:
        fail("gates.pins_equal_head must read refresh_py %s and directory_runner_py %s (the blobs re-hashed at HEAD)" % (REFRESH_BLOB[:12], RUNNER_BLOB[:12]))
    for k in ("one_change_at_a_time", "hm5_exempt_by_ruling_msg_11137", "hm5_members_equal_head", "ledger_opened_before_first_write", "outside_the_fire_band", "outside_the_gateway_window", "not_alongside_another_ib2_act"):
        if g.get(k) is not True:
            fail("gates.%s must be true" % k)
    b = g.get("branch_b_versions_named_before_write") or {}
    if b.get("bundle") != BUNDLE_BEFORE or b.get("zip_codesha256") != ZIP_BEFORE_SHA or b.get("zip_prior_s3_version_found") is not True:
        fail("gates.branch_b_versions_named_before_write must name the bundle version %s, the zip CodeSha256 %s and zip_prior_s3_version_found true" % (BUNDLE_BEFORE, ZIP_BEFORE_SHA))
    t = g.get("pre_mint_tests") or {}
    if not isinstance(t.get("passed"), int) or t["passed"] < 22 or t.get("failed") != 0:
        fail("gates.pre_mint_tests must read passed at least 22 (the 8 + 8 + 6 named tests) and failed 0, printed before the mint")
    print("OK: CTO half signed at the packet blob; pins re-hashed; one change at a time; ledger first; Branch B versions named; outside the band and the gateway window; tests printed")


def ac2(r):
    b = r.get("bundle") or {}
    n, e = b.get("members"), b.get("members_equal_head")
    if b.get("minted_through") != "safe-deploy" or not isinstance(n, int) or n < 1 or e != n:
        fail("bundle must read minted_through safe-deploy and members_equal_head equal to members (at least 1)")
    if b.get("version_before") != BUNDLE_BEFORE or not b.get("version_after") or b.get("version_after") == BUNDLE_BEFORE:
        fail("bundle.version_before must be %s and version_after a different non-empty id" % BUNDLE_BEFORE)
    z = r.get("zip") or {}
    if z.get("built_sha256_b64") != ZIP_PIN or z.get("equals_pin") is not True or z.get("head_object_verified") is not True:
        fail("zip must read built_sha256_b64 %s, equals_pin true and head_object_verified true" % ZIP_PIN)
    t = r.get("terraform") or {}
    p = t.get("plan") or {}
    if (p.get("add"), p.get("change"), p.get("destroy")) != (0, 1, 0) or p.get("addresses_changed") != CHANGES:
        fail("terraform.plan must read add 0, change 1 at %s, destroy 0" % CHANGES)
    if t.get("applied_through") != "safe-apply" or t.get("replan_no_changes") is not True:
        fail("terraform must read applied_through safe-apply and replan_no_changes true")
    if t.get("function_codesha256_after") != ZIP_PIN:
        fail("terraform.function_codesha256_after must equal the zip pin %s (the function now runs the pinned zip)" % ZIP_PIN)
    print("OK: bundle members all equal HEAD; zip digest equals the pin; plan 0/1/0 at the named address; safe-apply; clean re-plan; CodeSha256 equals the pin")


def ac3(r):
    k = r.get("counters") or {}
    want = {"lambda_invokes": 0, "fires_started_by_hand": 0, "other_iam_changes": 0, "keys_written_outside_the_two_artifacts": 0, "ssm_commands_sent": 0}
    for key, v in want.items():
        if k.get(key) != v:
            fail("counters.%s must read %s, read %r" % (key, v, k.get(key)))
    rb = r.get("rollback") or {}
    if not rb.get("bundle_version_to_restore") or rb.get("bundle_version_to_restore") != BUNDLE_BEFORE or not rb.get("zip_s3_version_to_restore"):
        fail("rollback must record bundle_version_to_restore %s and a zip_s3_version_to_restore" % BUNDLE_BEFORE)
    if rb.get("used") is not False:
        fail("rollback.used must be false (or the record belongs to a Branch B report, not this check)")
    if re.search(r"(?<![0-9A-Za-z])\d{9,}(?![0-9A-Za-z])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: no invoke, no fire by hand, nothing written outside the two artifacts, rollback versions recorded")


CHECKS = {"IBCW6-AC1": ac1, "IBCW6-AC2": ac2, "IBCW6-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p262_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
