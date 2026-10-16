"""Positive control and negatives for p243_cells.py (run by the issuer at the cut). Usage: python control243.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r243/p243_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p243_cells as P  # noqa: E402

GOOD = {
    "gates": {"pair_sha256": P.PAIR_SHA256, "addendum_blob": P.ADD_BLOB, "both_halves_signed": True, "one_change_at_a_time": True},
    "start_read": {"code_sha256": P.LIVE},
    "branch_b_version_id": "v1",
    "siblings": {s: {"code_sha256_before": "AAAA" + s[:4], "code_sha256_after": "AAAA" + s[:4]} for s in P.SIBLINGS},
    "source_map_rows": {"committed": True, "function": P.FN, "rows_changed": 2, "siblings_changed": 0},
    "apply": {"build_real_map_code_sha256": P.CAND, "built_code_sha256": P.CAND, "plan": {"add": 0, "change": 1, "destroy": 0}, "safe_apply_rc": 0,
              "path": "terraform-safe-apply"},
    "ledger": {"entry": "org/critical_paths/change_management/x.md", "opened_before_the_apply": True},
    "after": {"code_sha256": P.CAND, "replan_changes": 0, "changed_members": list(P.MEMBERS)},
    "health_proof": {"window_minutes": 12, "invocations": 3, "errors": 0, "throttles_429": 0},
    "deployed_handler_date_line_present": True,
    "first_scheduled_run": {"fire_utc_stated_before_apply": "2026-10-16T22:00:00Z", "manifest_split_adjust_declared": True, "securities_ratio_absent": 0,
                            "days_ratio_absent": 0, "unkeyed_split_rows": 0, "run_ok": True},
    "rollback_performed": False,
    "act2_started": False,
    "counters": {"artifact_uploads": 1, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "served_keys_written_by_me": 0,
                 "files_deleted": 0, "markers_closed": 0},
}


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, cto="SIGNED %s %s\n" % (P.PAIR_SHA256[:12], P.ADD_BLOB[:12]), alter_pair=False):
    root = Path(tempfile.mkdtemp(prefix="c243_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in (P.COO_HALF, P.COO_ADD):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        b = (REAL / rel).read_bytes()
        f.write_bytes(b + b"x" if alter_pair and rel == P.COO_HALF else b)
    for rel in (P.CTO_HALF, P.CTO_ADD):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(cto, encoding="utf-8")
    rec = copy.deepcopy(GOOD)
    if mut:
        mut(rec)
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
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
    print("%s %-12s %-32s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


def put(path, value):
    def fn(r):
        d = r
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return fn


NEGS = [
    ("pair_hash_in_record_wrong", "AC1", put(["gates", "pair_sha256"], "0" * 64)),
    ("addendum_blob_wrong", "AC1", put(["gates", "addendum_blob"], "0" * 40)),
    ("open_ledger_or_marker", "AC1", put(["gates", "one_change_at_a_time"], False)),
    ("live_digest_moved", "AC1", put(["start_read", "code_sha256"], "o9UugRAV" + "X" * 36)),
    ("no_branch_b", "AC1", put(["branch_b_version_id"], "")),
    ("sibling_before_missing", "AC1", lambda r: r["siblings"][P.SIBLINGS[0]].pop("code_sha256_before")),
    ("map_rows_three", "AC2", put(["source_map_rows", "rows_changed"], 3)),
    ("sibling_row_changed", "AC2", put(["source_map_rows", "siblings_changed"], 1)),
    ("real_map_build_differs", "AC2", put(["apply", "build_real_map_code_sha256"], "fvmE5j1hkNA16csMEtB3/WydmovkAucF/AmBxLCIqEg=")),
    ("plan_two_changes", "AC2", put(["apply", "plan"], {"add": 0, "change": 2, "destroy": 0})),
    ("not_safe_apply", "AC2", put(["apply", "path"], "update-function-code")),
    ("ledger_after_apply", "AC2", put(["ledger", "opened_before_the_apply"], False)),
    ("replan_nonzero", "AC2", put(["after", "replan_changes"], 1)),
    ("third_member_moved", "AC2", put(["after", "changed_members"], list(P.MEMBERS) + ["handler.py"])),
    ("sibling_moved", "AC2", lambda r: r["siblings"][P.SIBLINGS[1]].update(code_sha256_after="BBBB")),
    ("health_too_short", "AC3", put(["health_proof", "window_minutes"], 5)),
    ("health_errors", "AC3", put(["health_proof", "errors"], 1)),
    ("throttled", "AC3", put(["health_proof", "throttles_429"], 1)),
    ("handler_line_absent", "AC3", put(["deployed_handler_date_line_present"], False)),
    ("run_not_declared", "AC3", put(["first_scheduled_run", "manifest_split_adjust_declared"], False)),
    ("run_not_ok", "AC3", put(["first_scheduled_run", "run_ok"], False)),
    ("rollback", "AC3", put(["rollback_performed"], True)),
    ("act2_started", "AC3", put(["act2_started"], True)),
    ("backfill_counter", "AC3", put(["counters", "backfills"], 1)),
    ("invoke_counter", "AC3", put(["counters", "lambda_invokes"], 1)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB243-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB243-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(alter_pair=True)
expect("pair_bytes_changed", "IB243-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
root = build(cto="UNSIGNED draft %s %s\n" % (P.PAIR_SHA256[:12], P.ADD_BLOB[:12]))
expect("cto_half_not_signed", "IB243-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
