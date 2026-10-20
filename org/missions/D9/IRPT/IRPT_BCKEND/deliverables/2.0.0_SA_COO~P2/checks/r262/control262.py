"""Positive control and negatives for p262_cells.py (run by the issuer at the cut). Usage: python control262.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r262/p262_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p262_cells as P  # noqa: E402

GOOD = {
    "gates": {"packet_blob": P.BLOB, "both_halves_signed": True,
              "pins_equal_head": {"refresh_py": P.REFRESH_BLOB[:12], "directory_runner_py": P.RUNNER_BLOB[:12]},
              "one_change_at_a_time": True, "ledger_opened_before_first_write": True, "outside_the_fire_band": True,
              "outside_the_gateway_window": True, "not_alongside_another_ib2_act": True,
              "branch_b_versions_named_before_write": {"bundle": P.BUNDLE_BEFORE, "zip_codesha256": P.ZIP_BEFORE_SHA, "zip_prior_s3_version_found": True},
              "pre_mint_tests": {"passed": 22, "failed": 0}},
    "bundle": {"minted_through": "safe-deploy", "members": 13, "members_equal_head": 13, "version_before": P.BUNDLE_BEFORE, "version_after": "NEWVERSIONID0000000000000000000A"},
    "zip": {"built_sha256_b64": P.ZIP_PIN, "equals_pin": True, "head_object_verified": True},
    "terraform": {"plan": {"add": 0, "change": 1, "destroy": 0, "addresses_changed": list(P.CHANGES)},
                  "applied_through": "safe-apply", "replan_no_changes": True, "function_codesha256_after": P.ZIP_PIN},
    "counters": {"lambda_invokes": 0, "fires_started_by_hand": 0, "other_iam_changes": 0, "keys_written_outside_the_two_artifacts": 0, "ssm_commands_sent": 0},
    "rollback": {"bundle_version_to_restore": P.BUNDLE_BEFORE, "zip_s3_version_to_restore": "PRIORZIPVERSION0000000000000000", "used": False},
}


def mut(path, value):
    def f(r):
        r = copy.deepcopy(r)
        cur = r
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return r
    return f


NEGS = [
    ("wrong_packet_blob", "AC1", mut(["gates", "packet_blob"], "0" * 40)),
    ("halves_not_signed", "AC1", mut(["gates", "both_halves_signed"], False)),
    ("refresh_pin_differs", "AC1", mut(["gates", "pins_equal_head", "refresh_py"], "000000000000")),
    ("runner_pin_differs", "AC1", mut(["gates", "pins_equal_head", "directory_runner_py"], "000000000000")),
    ("not_one_change_at_a_time", "AC1", mut(["gates", "one_change_at_a_time"], False)),
    ("ledger_not_first", "AC1", mut(["gates", "ledger_opened_before_first_write"], False)),
    ("inside_fire_band", "AC1", mut(["gates", "outside_the_fire_band"], False)),
    ("inside_gateway_window", "AC1", mut(["gates", "outside_the_gateway_window"], False)),
    ("alongside_another_ib2_act", "AC1", mut(["gates", "not_alongside_another_ib2_act"], False)),
    ("branch_b_bundle_not_named", "AC1", mut(["gates", "branch_b_versions_named_before_write", "bundle"], "WRONG")),
    ("branch_b_zip_sha_not_named", "AC1", mut(["gates", "branch_b_versions_named_before_write", "zip_codesha256"], "WRONG")),
    ("branch_b_zip_version_not_found", "AC1", mut(["gates", "branch_b_versions_named_before_write", "zip_prior_s3_version_found"], False)),
    ("pre_mint_tests_failing", "AC1", mut(["gates", "pre_mint_tests", "failed"], 1)),
    ("pre_mint_tests_too_few", "AC1", mut(["gates", "pre_mint_tests", "passed"], 21)),
    ("bundle_not_via_safe_deploy", "AC2", mut(["bundle", "minted_through"], "aws s3 cp")),
    ("bundle_member_differs", "AC2", mut(["bundle", "members_equal_head"], 12)),
    ("bundle_no_members", "AC2", mut(["bundle", "members"], 0)),
    ("bundle_version_unchanged", "AC2", mut(["bundle", "version_after"], P.BUNDLE_BEFORE)),
    ("zip_digest_differs", "AC2", mut(["zip", "built_sha256_b64"], "AAAA")),
    ("zip_not_verified", "AC2", mut(["zip", "head_object_verified"], False)),
    ("plan_adds_one", "AC2", mut(["terraform", "plan", "add"], 1)),
    ("plan_destroys_one", "AC2", mut(["terraform", "plan", "destroy"], 1)),
    ("plan_changes_other_address", "AC2", mut(["terraform", "plan", "addresses_changed"], ["aws_iam_role.other"])),
    ("not_safe_apply", "AC2", mut(["terraform", "applied_through"], "terraform apply")),
    ("replan_dirty", "AC2", mut(["terraform", "replan_no_changes"], False)),
    ("function_not_on_the_pinned_zip", "AC2", mut(["terraform", "function_codesha256_after"], P.ZIP_BEFORE_SHA)),
    ("a_lambda_invoke", "AC3", mut(["counters", "lambda_invokes"], 1)),
    ("a_fire_by_hand", "AC3", mut(["counters", "fires_started_by_hand"], 1)),
    ("an_ssm_command", "AC3", mut(["counters", "ssm_commands_sent"], 1)),
    ("other_iam_change", "AC3", mut(["counters", "other_iam_changes"], 1)),
    ("key_written_outside", "AC3", mut(["counters", "keys_written_outside_the_two_artifacts"], 1)),
    ("rollback_bundle_wrong", "AC3", mut(["rollback", "bundle_version_to_restore"], "WRONG")),
    ("rollback_zip_missing", "AC3", mut(["rollback", "zip_s3_version_to_restore"], "")),
    ("rollback_used", "AC3", mut(["rollback", "used"], True)),
    ("long_digit_run", "AC3", mut(["rollback", "note"], "count 1234567890123")),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c262_"))
    for rel, txt in ((P.CTO_HALF, "SIGNED blob " + P.BLOB[:10]), (P.PACKET, "COO half SIGNED")):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=60, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-34s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBCW6-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IBCW6-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
# the CTO half unsigned or at another blob
for label, txt in (("cto_half_unsigned", "blob " + P.BLOB[:10] + " pending"), ("cto_half_other_blob", "SIGNED blob 0000000000")):
    root = build(GOOD)
    (root / P.CTO_HALF).write_text(txt, encoding="utf-8")
    expect(label, "IBCW6-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c262_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IBCW6-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
