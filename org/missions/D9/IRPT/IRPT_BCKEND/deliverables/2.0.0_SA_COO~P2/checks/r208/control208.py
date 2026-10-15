"""Positive control and negatives for p208_cells.py (run by the issuer at the cut, never by the executing seat).

Usage: python control208.py <real_repo_root>
Builds a temp git tree holding the real lib/trading_calendar.py, two half files that carry the packet's sha256, a ledger entry and a commit, writes a clean synthetic
record, runs every criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp tree is removed.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r208/p208_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p208_cells as P  # noqa: E402

LEDGER = "org/critical_paths/change_management/20261015T1000Z_orion_backfill_33_days.md"


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build():
    root = Path(tempfile.mkdtemp(prefix="c208_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    for rel in (P.COO_HALF, P.CTO_HALF):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("# half bound to sha256 %s\n" % P.PACKET_SHA, encoding="utf-8")
    (root / LEDGER).parent.mkdir(parents=True, exist_ok=True)
    (root / LEDGER).write_text("# ledger\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "control result")
    return root, git(root, "rev-parse", "HEAD")


def day_row(feed, day, i):
    r = {"day": day, "absent_before": True, "outcome": "WRITTEN", "version_id": "v%dAbC%d" % (i, i), "content_length": 1000 + i, "row_count": 50 + i,
         "asof_day": day, "written_at_utc": "2026-10-15T10:%02d:00Z" % (10 + i % 40), "read_back_ok": True}
    if feed == "positions":
        r["parquet_key_present"] = True
    return r


def record(commit):
    days = {"positions": [day_row("positions", d, i) for i, d in enumerate(["2026-07-01", "2026-08-06", "2026-09-28", "2026-09-29"])],
            "transactions": [day_row("transactions", d, i) for i, d in enumerate(P.TXN)],
            "performance": [day_row("performance", d, i) for i, d in enumerate(P.PERF)]}
    return {"gates": {"packet_sha256": P.PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "no_open_ledger_or_marker": True, "one_change_at_a_time": True},
            "ledger": {"entry": LEDGER, "opened_before_first_write": True},
            "control": {"performed": True, "branch": "repo_script_matches", "committed_commit": commit, "committed_at_utc": "2026-10-15T09:55:00Z",
                        "byte_diff": {"repo_bytes": 29784, "chain_bytes": 29230, "differing_lines": 12}, "dry_run_compared_day": "2026-10-14", "shape_match": True},
            "days": days, "keys_written": 33, "requests_made": 14300,
            "counters": {k: 0 for k in P.COUNTERS},
            "notes": ["ran on the operator host with the pull code's own credential path; no secret printed", "objects touched: 33 flat keys, 33 head reads, 33 absent reads",
                      "not read: the vendor's rate limits beyond the scripts' limiter"],
            "stop": None}


def write(root, rec):
    p = root / P.REC
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def sp(d, path, v):
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = v


MUTS = [
    ("AC1", "stop_recorded", lambda r: sp(r, ["stop"], {"step": 4, "reason": "x"})),
    ("AC1", "wrong_packet_sha", lambda r: sp(r, ["gates", "packet_sha256"], "e" * 64)),
    ("AC1", "cto_half_unsigned_flag", lambda r: sp(r, ["gates", "cto_half_signed"], False)),
    ("AC1", "ledger_not_in_tree", lambda r: sp(r, ["ledger", "entry"], "org/critical_paths/change_management/none.md")),
    ("AC1", "ledger_after_first_write", lambda r: sp(r, ["ledger", "opened_before_first_write"], False)),
    ("AC1", "control_not_performed", lambda r: sp(r, ["control", "performed"], False)),
    ("AC1", "control_commit_unknown", lambda r: sp(r, ["control", "committed_commit"], "a" * 40)),
    ("AC1", "control_after_a_performance_write", lambda r: sp(r, ["control", "committed_at_utc"], "2026-10-15T23:00:00Z")),
    ("AC1", "branch_shape_mismatch", lambda r: sp(r, ["control", "shape_match"], False)),
    ("AC1", "code_object_changed_on_branch2", lambda r: (sp(r, ["control", "branch"], "chain_copy_runs_with_date"), sp(r, ["counters", "s3_code_objects_changed"], 1))),
    ("AC2", "short_positions", lambda r: r["days"]["positions"].pop()),
    ("AC2", "transactions_days_wrong", lambda r: sp(r, ["days", "transactions", 0, "day"], "2026-07-02")),
    ("AC2", "performance_days_wrong", lambda r: sp(r, ["days", "performance", 3, "day"], "2026-05-06")),
    ("AC2", "not_read_absent_first", lambda r: sp(r, ["days", "performance", 0, "absent_before"], False)),
    ("AC2", "positions_without_parquet", lambda r: sp(r, ["days", "positions", 0, "parquet_key_present"], False)),
    ("AC2", "empty_key_written", lambda r: sp(r, ["days", "transactions", 2, "row_count"], 0)),
    ("AC2", "absent_at_source_without_status", lambda r: (sp(r, ["days", "transactions", 1, "outcome"], "ABSENT_AT_SOURCE"), sp(r, ["days", "transactions", 1, "version_id"], None))),
    ("AC2", "day_not_dispositioned", lambda r: sp(r, ["days", "performance", 5, "outcome"], "PENDING")),
    ("AC3", "read_back_missing", lambda r: sp(r, ["days", "performance", 7, "read_back_ok"], False)),
    ("AC3", "keys_written_wrong", lambda r: sp(r, ["keys_written"], 30)),
    ("AC3", "requests_over_bound", lambda r: sp(r, ["requests_made"], 20000)),
    ("AC3", "a_delete_counted", lambda r: sp(r, ["counters", "files_deleted"], 1)),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
]

bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-34s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root, commit = build()
rec = record(commit)
write(root, rec)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB208-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB208-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
