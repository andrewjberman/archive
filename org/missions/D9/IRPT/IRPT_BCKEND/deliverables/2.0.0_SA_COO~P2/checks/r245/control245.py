"""Positive control and negatives for p245_cells.py (run by the issuer at the cut). Usage: python control245.py <real_repo_root>"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r245/p245_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p245_cells as P  # noqa: E402

P6 = P.P6
P6.ROOT = REAL


def good():
    return {
        "gates": {"packet_blob": P.PACKET_BLOB, "both_halves_signed": True, "act_1_ledger_open": True, "function_code_sha256": P.CAND, "one_change_at_a_time": True},
        "change": {"files_changed": [P.LOCALS], "plan": {"add": 0, "change": 1, "destroy": 0, "resources": [P.POLICY]},
                   "path": "terraform-safe-apply", "safe_apply_rc": 0, "replan_changes": 0},
        "simulate_before": {"allowed_arms_implicit_deny": 2, "denied_arms_implicit_deny": 8, "unchanged_arms_allowed": 4},
        "simulate_after": {"allowed_arms_allowed": 2, "denied_arms_implicit_deny": 8, "unchanged_arms_allowed": 4},
        "recovery": {"invokes": 1, "event": dict(P.SCHEDULE_INPUT), "status_code": 200, "function_error_absent": True,
                     "manifest_split_adjust_declared": True, "run_ok": True, "days_written": 1, "next_scheduled_fire_utc": "2026-10-19T11:30:00Z"},
        "rollback_performed": False, "act2_started": False, "ledger_closed_by_applier": False,
        "counters": {"lambda_invokes": 1, "iam_changes": 1, "artifact_uploads": 0, "schedule_changes": 0, "files_deleted": 0, "markers_closed": 0,
                     "served_keys_written_by_me": 0},
    }


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, cto_ok=True, alter_packet=False, no_cto=False):
    root = Path(tempfile.mkdtemp(prefix="c245_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    f = root / P.PACKET
    f.parent.mkdir(parents=True, exist_ok=True)
    b = (REAL / P.PACKET).read_bytes()
    f.write_bytes(b + b"x" if alter_packet else b)
    if not no_cto:
        g = root / P.CTO_DIR / "NEVER_WIDEN_49F_PERF_ROLE_TRANSACTIONS_READ_IAM_PAIR_CTO_HALF.md"
        g.parent.mkdir(parents=True, exist_ok=True)
        g.write_text(("SIGNED " if cto_ok else "UNSIGNED draft ") + P.PACKET_BLOB[:10] + "\n", encoding="utf-8")
    rec = good()
    if mut:
        mut(rec)
    h = root / P.REC
    h.parent.mkdir(parents=True, exist_ok=True)
    h.write_text(json.dumps(rec), encoding="utf-8")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-34s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


def put(path, value):
    def fn(r):
        d = r
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return fn


NEGS = [
    ("packet_blob_wrong", "AC1", put(["gates", "packet_blob"], "0" * 40)),
    ("halves_not_signed", "AC1", put(["gates", "both_halves_signed"], False)),
    ("act_1_ledger_closed", "AC1", put(["gates", "act_1_ledger_open"], False)),
    ("function_off_candidate", "AC1", put(["gates", "function_code_sha256"], "o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok=")),
    ("not_one_change", "AC1", put(["gates", "one_change_at_a_time"], False)),
    ("two_files_edited", "AC2", put(["change", "files_changed"], [P.LOCALS, "infra/aws/terraform/investor-reporting/holdings-performance/iam.tf"])),
    ("plan_two_changes", "AC2", put(["change", "plan", "change"], 2)),
    ("plan_has_destroy", "AC2", put(["change", "plan", "destroy"], 1)),
    ("plan_other_resource", "AC2", put(["change", "plan", "resources"], [P.POLICY, "aws_iam_role.irpt_holdings_performance"])),
    ("not_safe_apply", "AC2", put(["change", "path"], "console")),
    ("replan_nonzero", "AC2", put(["change", "replan_changes"], 1)),
    ("before_gap_not_shown", "AC2", put(["simulate_before", "allowed_arms_implicit_deny"], 0)),
    ("denied_arm_allowed_after", "AC2", put(["simulate_after", "denied_arms_implicit_deny"], 7)),
    ("allowed_arm_still_denied", "AC2", put(["simulate_after", "allowed_arms_allowed"], 1)),
    ("unchanged_arm_lost", "AC2", put(["simulate_after", "unchanged_arms_allowed"], 3)),
    ("two_invokes", "AC3", put(["recovery", "invokes"], 2)),
    ("event_has_date", "AC3", lambda r: r["recovery"]["event"].update(date="2026-10-16")),
    ("function_error", "AC3", put(["recovery", "function_error_absent"], False)),
    ("split_adjust_undeclared", "AC3", put(["recovery", "manifest_split_adjust_declared"], False)),
    ("run_not_ok", "AC3", put(["recovery", "run_ok"], False)),
    ("no_days_written", "AC3", put(["recovery", "days_written"], 0)),
    ("next_fire_wrong", "AC3", put(["recovery", "next_scheduled_fire_utc"], "2026-10-19T12:00:00Z")),
    ("rollback", "AC3", put(["rollback_performed"], True)),
    ("act2_started", "AC3", put(["act2_started"], True)),
    ("applier_closed_ledger", "AC3", put(["ledger_closed_by_applier"], True)),
    ("schedule_changed", "AC3", put(["counters", "schedule_changes"], 1)),
    ("file_deleted", "AC3", put(["counters", "files_deleted"], 1)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB245-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB245-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
for label, kw in (("packet_bytes_changed", {"alter_packet": True}), ("cto_half_not_signed", {"cto_ok": False}), ("cto_half_absent", {"no_cto": True})):
    root = build(**kw)
    expect(label, "IB245-1-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
