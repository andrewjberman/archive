"""Positive control and negatives for p254_cells.py (run by the issuer at the cut). Usage: python control254.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r254/p254_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p254_cells as P  # noqa: E402

GOOD = {
    "gates": {"packet_blob": P.BLOB, "addendum_blob": P.ADD_BLOB, "both_halves_signed": True, "one_change_at_a_time": True,
              "ledger_opened_before_first_write": True, "outside_the_fire_window": True, "trading_calendar_tests_printed_before_mint": True,
              "branch_b_versions_named_before_write": {"bundle": P.BUNDLE_BEFORE, "zip": True}},
    "bundle": {"minted_through": "safe-deploy", "members": 12, "members_equal_head": 12, "version_before": P.BUNDLE_BEFORE, "version_after": "NEWVERSIONID0000000000000000000A"},
    "zip": {"built_sha256_b64": P.ZIP_PIN, "equals_pin": True, "head_object_verified": True},
    "terraform": {"plan": {"add": 3, "change": 1, "destroy": 0, "addresses_added": list(P.ADDS), "addresses_changed": list(P.CHANGES)},
                  "applied_through": "safe-apply", "replan_no_changes": True, "env_keys_present": list(P.ENV_KEYS)},
    "simulation": {"allowed": {k: "allowed" for k in P.ALLOWED}, "denied": {k: "implicitDeny" for k in P.DENIED}},
    "secret": {"value_put_count": 1, "version_count": 1, "value_printed": False},
    "qa": dict({k: "PASS" for k in P.QA}, runs=1, assume_succeeded_before_mdpf_leg=False),
    "counters": {"other_lambda_invokes": 0, "other_iam_changes": 0, "keys_written_outside_the_three": 0, "existing_keys_changed": 0, "secrets_printed": 0, "per_firm_numbers_recorded": 0},
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
    ("wrong_addendum_blob", "AC1", mut(["gates", "addendum_blob"], "0" * 40)),
    ("halves_not_signed", "AC1", mut(["gates", "both_halves_signed"], False)),
    ("not_one_change_at_a_time", "AC1", mut(["gates", "one_change_at_a_time"], False)),
    ("ledger_not_first", "AC1", mut(["gates", "ledger_opened_before_first_write"], False)),
    ("inside_fire_window", "AC1", mut(["gates", "outside_the_fire_window"], False)),
    ("trading_calendar_tests_not_printed", "AC1", mut(["gates", "trading_calendar_tests_printed_before_mint"], False)),
    ("branch_b_bundle_not_named", "AC1", mut(["gates", "branch_b_versions_named_before_write", "bundle"], "WRONG")),
    ("branch_b_zip_not_named", "AC1", mut(["gates", "branch_b_versions_named_before_write", "zip"], False)),
    ("bundle_not_via_safe_deploy", "AC2", mut(["bundle", "minted_through"], "aws s3 cp")),
    ("bundle_member_differs", "AC2", mut(["bundle", "members_equal_head"], 11)),
    ("bundle_version_unchanged", "AC2", mut(["bundle", "version_after"], P.BUNDLE_BEFORE)),
    ("zip_digest_differs", "AC2", mut(["zip", "built_sha256_b64"], "AAAA")),
    ("zip_not_verified", "AC2", mut(["zip", "head_object_verified"], False)),
    ("plan_adds_four", "AC2", mut(["terraform", "plan", "add"], 4)),
    ("plan_destroys_one", "AC2", mut(["terraform", "plan", "destroy"], 1)),
    ("plan_changes_other_address", "AC2", mut(["terraform", "plan", "addresses_changed"], ["aws_iam_role.other"])),
    ("not_safe_apply", "AC2", mut(["terraform", "applied_through"], "terraform apply")),
    ("replan_dirty", "AC2", mut(["terraform", "replan_no_changes"], False)),
    ("env_key_missing", "AC2", mut(["terraform", "env_keys_present"], ["IRPT_HMAC_ROLE_ARN", "IRPT_HMAC_SECRET_ID"])),
    ("get_secret_not_allowed", "AC3", mut(["simulation", "allowed", "get_the_one_secret"], "implicitDeny")),
    ("delete_allowed", "AC3", mut(["simulation", "denied", "delete_object_on_a_list_key"], "allowed")),
    ("other_secret_allowed", "AC3", mut(["simulation", "denied", "get_any_other_secret"], "allowed")),
    ("secret_put_twice", "AC3", mut(["secret", "value_put_count"], 2)),
    ("secret_printed", "AC3", mut(["secret", "value_printed"], True)),
    ("two_qa_runs", "AC3", mut(["qa", "runs"], 2)),
    ("qa_directory_changed", "AC3", mut(["qa", "directory_output_byte_unchanged"], "FAIL")),
    ("qa_plain_sha256_found", "AC3", mut(["qa", "no_plain_sha256_of_a_known_fake_id"], "FAIL")),
    ("assume_fact_missing", "AC3", mut(["qa", "assume_succeeded_before_mdpf_leg"], "unknown")),
    ("key_written_outside_three", "AC3", mut(["counters", "keys_written_outside_the_three"], 1)),
    ("per_firm_number_recorded", "AC3", mut(["counters", "per_firm_numbers_recorded"], 1)),
    ("long_digit_run", "AC3", mut(["qa", "note"], "count 1234567890123")),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c254_"))
    for rel, txt in ((P.CTO_HALF, "SIGNED blob " + P.BLOB[:8] + " ADDENDUM 1 SIGNED blob " + P.ADD_BLOB[:8]), (P.PACKET, "COO half SIGNED"), (P.COO_ADD, "COO half SIGNED")):
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
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHM5-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
TRUE = copy.deepcopy(GOOD)
TRUE["qa"]["assume_succeeded_before_mdpf_leg"] = True
root = build(TRUE)
expect("assume_fact_true", "IBHM5-AC3", root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IBHM5-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c254_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IBHM5-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
