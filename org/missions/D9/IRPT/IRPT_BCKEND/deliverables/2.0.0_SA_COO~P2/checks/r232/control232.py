"""Positive control and negatives for p232_cells.py (run by the issuer at the cut). Usage: python control232.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r232/p232_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p232_cells as P  # noqa: E402

H64 = "ab" * 32
GOOD = {
    "gates": {"packet_blob": P.BLOB, "addendum_blob": P.ADD_BLOB, "both_halves_signed": True, "text_equals_committed": True, "inline_policy_names_printed": True,
              "plan": {"add": 1, "change": 0, "destroy": 0, "addresses": [P.ADDRESS]},
              "arns": {"prefixes_printed": True, "equal_address_output": True},
              "one_change_at_a_time": True, "ledger_opened_before_apply": True},
    "apply": {"through": "safe-apply", "added": 1, "changed": 0, "destroyed": 0, "replan_no_changes": True,
              "policy_readback": {"statement_count": 2, "delete_action_present": False, "kms_action_present": False, "policy_sha256": H64},
              "rollback_performed": False},
    "simulation": {"allowed": {k: "allowed" for k in P.ALLOWED}, "denied": {k: "implicitDeny" for k in P.DENIED},
                   "controls": {"inf_bucket_allowed": True, "unrelated_bucket_denied": True}},
    "exists_read": {"ran_on_runner": True, "key_was_known_absent": True, "answer": "ABSENT"},
    "counters": {"function_updates": 0, "lambda_invokes": 0, "other_iam_changes": 0, "schedule_changes": 0, "keys_written": 0,
                 "existing_keys_changed": 0, "secrets_printed": 0},
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
    ("wrong_blob", "AC1", mut(["gates", "packet_blob"], "0" * 40)),
    ("wrong_addendum_blob", "AC1", mut(["gates", "addendum_blob"], "0" * 40)),
    ("text_not_committed", "AC1", mut(["gates", "text_equals_committed"], False)),
    ("names_not_printed", "AC1", mut(["gates", "inline_policy_names_printed"], False)),
    ("plan_two_added", "AC1", mut(["gates", "plan", "add"], 2)),
    ("plan_other_address", "AC1", mut(["gates", "plan", "addresses"], [P.ADDRESS, "aws_iam_role_policy.other"])),
    ("arns_not_equal", "AC1", mut(["gates", "arns", "equal_address_output"], False)),
    ("ledger_not_first", "AC1", mut(["gates", "ledger_opened_before_apply"], False)),
    ("not_safe_apply", "AC2", mut(["apply", "through"], "terraform apply")),
    ("replan_dirty", "AC2", mut(["apply", "replan_no_changes"], False)),
    ("delete_in_policy", "AC2", mut(["apply", "policy_readback", "delete_action_present"], True)),
    ("kms_in_policy", "AC2", mut(["apply", "policy_readback", "kms_action_present"], True)),
    ("sibling_put_allowed", "AC3", mut(["simulation", "denied", "put_sibling_fact_positions_key"], "allowed")),
    ("delete_allowed", "AC3", mut(["simulation", "denied", "delete_feed_key"], "allowed")),
    ("put_not_allowed", "AC3", mut(["simulation", "allowed", "put_silver_feed_key"], "implicitDeny")),
    ("exists_403", "AC3", mut(["exists_read", "answer"], "403")),
    ("exists_not_on_runner", "AC3", mut(["exists_read", "ran_on_runner"], False)),
    ("key_written", "AC3", mut(["counters", "keys_written"], 1)),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c232_"))
    for rel, txt in ((P.COO_HALF, "GIVEN blob " + P.BLOB[:10]), (P.CTO_HALF, "SIGNED blob " + P.BLOB[:10]), (P.PACKET, "packet"), (P.ADD_COO, "GIVEN blob " + P.ADD_BLOB[:10]), (P.ADD_CTO, "SIGNED blob " + P.ADD_BLOB[:10])):
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
    print("%s %-12s %-26s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB232-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IB232-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c232_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IB232-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
