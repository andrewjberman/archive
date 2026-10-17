"""Positive control and negatives for p255_cells.py (run by the issuer at the cut). Usage: python control255.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r255/p255_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p255_cells as P  # noqa: E402

GOOD = {
    "gates": {"packet_blob": P.BLOB, "both_halves_signed": True, "worktrees_read": {"count": 7, "denominator_printed": True},
              "no_other_ledger_open_on_the_root": True, "head_holds_c5dd8b293a": True, "head_holds_2d2c906b87": True,
              "ledger_opened_before_apply": True, "outside_the_fire_window": True},
    "terraform": {"plan": {"add": 0, "change": 1, "destroy": 0, "addresses_changed": [P.ADDRESS]}, "applied_through": "safe-apply", "replan_no_changes": True},
    "policy_readback": {"new_statement_sid": P.SID_NEW, "new_statement_count": 1, "statement_49f_unchanged": True, "other_statements_unchanged": True, "wildcard_in_new_statement": False},
    "simulation": {"allowed": {k: "allowed" for k in P.ALLOWED}, "denied": {k: "implicitDeny" for k in P.DENIED}},
    "qa": {"runs": 0, "deferred_to_scheduled_fire": True},
    "counters": {"other_iam_changes": 0, "other_terraform_roots_applied": 0, "lambda_invokes": 0, "secrets_printed": 0, "per_firm_numbers_recorded": 0},
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
    ("wrong_blob", "AC1", GOOD, mut(["gates", "packet_blob"], "0" * 40)),
    ("halves_not_signed", "AC1", GOOD, mut(["gates", "both_halves_signed"], False)),
    ("worktrees_zero", "AC1", GOOD, mut(["gates", "worktrees_read", "count"], 0)),
    ("denominator_not_printed", "AC1", GOOD, mut(["gates", "worktrees_read", "denominator_printed"], False)),
    ("other_ledger_open", "AC1", GOOD, mut(["gates", "no_other_ledger_open_on_the_root"], False)),
    ("head_lacks_c5dd", "AC1", GOOD, mut(["gates", "head_holds_c5dd8b293a"], False)),
    ("head_lacks_2d2c", "AC1", GOOD, mut(["gates", "head_holds_2d2c906b87"], False)),
    ("ledger_not_first", "AC1", GOOD, mut(["gates", "ledger_opened_before_apply"], False)),
    ("inside_fire_window", "AC1", GOOD, mut(["gates", "outside_the_fire_window"], False)),
    ("plan_two_changes", "AC2", GOOD, mut(["terraform", "plan", "change"], 2)),
    ("plan_an_add", "AC2", GOOD, mut(["terraform", "plan", "add"], 1)),
    ("plan_a_destroy", "AC2", GOOD, mut(["terraform", "plan", "destroy"], 1)),
    ("plan_other_address", "AC2", GOOD, mut(["terraform", "plan", "addresses_changed"], ["aws_iam_role_policy.other"])),
    ("not_safe_apply", "AC2", GOOD, mut(["terraform", "applied_through"], "terraform apply")),
    ("replan_dirty", "AC2", GOOD, mut(["terraform", "replan_no_changes"], False)),
    ("new_statement_missing", "AC2", GOOD, mut(["policy_readback", "new_statement_count"], 0)),
    ("statement_49f_changed", "AC2", GOOD, mut(["policy_readback", "statement_49f_unchanged"], False)),
    ("other_statements_changed", "AC2", GOOD, mut(["policy_readback", "other_statements_unchanged"], False)),
    ("wildcard_in_new_statement", "AC2", GOOD, mut(["policy_readback", "wildcard_in_new_statement"], True)),
    ("assume_not_allowed", "AC3", GOOD, mut(["simulation", "allowed", "assume_the_stage_role"], "implicitDeny")),
    ("unrelated_role_allowed", "AC3", GOOD, mut(["simulation", "denied", "assume_an_unrelated_role"], "allowed")),
    ("wildcard_assume_allowed", "AC3", GOOD, mut(["simulation", "denied", "any_wildcard_resource_assume"], "allowed")),
    ("one_qa_run", "AC3", GOOD, mut(["qa", "runs"], 1)),
    ("qa_not_deferred", "AC3", GOOD, mut(["qa", "deferred_to_scheduled_fire"], False)),
    ("a_lambda_invoke", "AC3", GOOD, mut(["counters", "lambda_invokes"], 1)),
    ("other_iam_change", "AC3", GOOD, mut(["counters", "other_iam_changes"], 1)),
    ("other_root_applied", "AC3", GOOD, mut(["counters", "other_terraform_roots_applied"], 1)),
    ("per_firm_number", "AC3", GOOD, mut(["counters", "per_firm_numbers_recorded"], 1)),
    ("long_digit_run", "AC3", GOOD, mut(["qa", "note"], "count 1234567890123")),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c255_"))
    for rel, txt in ((P.CTO_HALF, "SIGNED blob " + P.BLOB[:8]), (P.PACKET, "COO half SIGNED")):
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


for name, rec in (("clean", GOOD),):
    root = build(rec)
    for ac in ("AC1", "AC2", "AC3"):
        expect(name, "IBHM11-" + ac, root, True)
    shutil.rmtree(root, ignore_errors=True)
for label, ac, base, fn in NEGS:
    root = build(fn(base))
    expect(label, "IBHM11-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c255_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IBHM11-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
