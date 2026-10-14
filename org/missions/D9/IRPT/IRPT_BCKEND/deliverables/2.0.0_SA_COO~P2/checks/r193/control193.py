"""Positive control and negatives for p193_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control193.py <real_repo_root>
Builds a temp root with synthetic records (and a stub producer package in a throwaway git repo for IB193-2), runs every
criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r193/p193_cells.py"
sys.path.insert(0, str(CHECK.parent))
import p193_cells as P  # noqa: E402

D = P.D
SHA = P.PACKET_SHA

APPLY = {
    "gates": {"packet_sha256": SHA, "coo_half_signed": True, "cto_half_signed": True, "holdings_snapshot_blob": P.BLOB},
    "remeasure": {"pins": P.PINS, "firms": {f: {"movers_canonical": v[0], "movers_fallback": v[1], "gate_before": v[2], "gate_after": v[3],
                                                 "lost_accounts_listed_after": v[4], "matches_packet": True} for f, v in P.PACKET_NUMBERS.items()}},
    "branch_b_reread": {f: {"bundle_version_id": P.BRANCH_B_BUNDLE[f], "manifest_version_id": P.BRANCH_B_MANIFEST[f],
                            "manifest_anchor_at_mint": ({"version_id": P.BRANCH_B_MANIFEST[f], "newer_versions": 0} if f == "cottonwood" else
                                                        {"version_id": "FIREWRITTEN_" + f, "newer_versions": 1, "written_by_scheduled_fire": True,
                                                         "fire_date": "2026-10-14", "published_date": "2026-10-13"})} for f in P.FIRMS},
    "digest_gate": {f: {"changed_members": ["holdings_snapshot.py", "SHA256SUMS"]} for f in P.FIRMS},
    "window": {"last_fire_all_success_utc": "2026-10-14T14:31:00Z", "mint_start_utc": "2026-10-14T15:10:00Z", "mint_end_utc": "2026-10-14T15:40:00Z",
               "next_fire_utc": "2026-10-15T14:15:00Z"},
    "ledger": {"entry": "org/critical_paths/change_management/20261014_holdings_release.md", "legs": 4, "opened_before_first_mint": True},
    "mints": {f: {"bundle": P.BUNDLES[f], "before_version_id": P.BRANCH_B_BUNDLE[f], "after_version_id": "NEWVERSION_" + f, "after_sha256_equals_built": True} for f in P.FIRMS},
    "business_date_statement": {"stated_at_utc": "2026-10-15T09:00:00Z", "fire_date": "2026-10-15", "t_minus_1": "2026-10-14",
                                "per_firm_expected": {f: "2026-10-14" for f in P.FIRMS}},
    "after_read": {
        "49financial": {"outcome": "STAMPED_T_MINUS_1", "stamp": "2026-10-14", "t1_partition_under_it": True},
        "cottonwood": {"outcome": "STAMPED_T_MINUS_1", "stamp": "2026-10-14", "t1_partition_under_it": True, "lost_accounts_listed": 1},
        "inflection": {"outcome": "HELD_NO_NEW_PUBLICATION", "absent_partition_named": "silver/positions snapshot_date=2026-10-14 absent",
                       "frontier_unchanged": True, "served_latest_date_before": "2026-10-13", "served_latest_date_after": "2026-10-13"}},
    "rule_after_read": {"cash_sub_read_cash": True},
    "gap_2026_10_08": {"unchanged": True},
    "kill_cause_memory_read": {"required_by_verdict": False, "memory_read_done": False},
    "rollback_performed": False, "stop": None,
    "counters": dict(P.APPLY_COUNTERS),
}
KILL = {
    "fire": {"fire_date": "2026-10-09", "response_code": 137, "plugin_seconds": 309.9},
    "verdict": "NOT_OOM", "verdict_basis": "the kernel log for the fire window holds no out-of-memory kill record and the memory metric stayed low",
    "reads": [{"source": "journalctl -k over the window", "result": "no oom lines"}],
    "memory_read_for_release_fire": False,
    "host_commands": [{"command": "journalctl -k --since '2026-10-09 14:15' --until '2026-10-09 14:25' | grep -ci oom", "read_only": True}],
    "host_commands_sent": 1, "notes": ["read from the host's own journal"],
    "functions_invoked": 0, "aws_writes_made": 0, "files_deleted": 0, "service_restarts": 0, "host_state_changes": 0,
}
STUB_SNAP = "def run_firm():\n    # BEGIN ONE-DATE-ASSERT\n    ASSERT = True\n    # END ONE-DATE-ASSERT\n    return ASSERT\n"
STUB_TEST_NEW = "import sys, pathlib\nsys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))\nimport holdings_snapshot as hs\n" + "".join(
    "def test_%d():\n    assert hs.run_firm() is True\n" % i for i in range(9)) + "def test_assert_present():\n    assert hasattr(hs, 'ASSERT') or True\n    src = open(hs.__file__).read()\n    assert 'ASSERT = True' in src\n"
STUB_TEST_OLD = "def test_old():\n    assert True\n"


def w(root, rel, obj):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(obj if isinstance(obj, str) else json.dumps(obj, indent=1), encoding="utf-8")


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def make_root(apply=None, kill=None, build_mut=None):
    root = Path(tempfile.mkdtemp(prefix="c193_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    w(root, P.APPLY_REC, apply or APPLY)
    w(root, "org/critical_paths/change_management/20261014_holdings_release.md", "ledger")
    w(root, P.KILL_REC, kill or KILL)
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    w(root, P.SNAP, "def run_firm():\n    return True\n")
    w(root, P.TEST_OLD, STUB_TEST_OLD)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    base = git(root, "rev-parse", "HEAD")
    snap = STUB_SNAP
    tnew = STUB_TEST_NEW
    changed = [P.SNAP, P.TEST_NEW]
    if build_mut == "no_block":
        snap = "def run_firm():\n    ASSERT = True\n    return ASSERT\n"
    if build_mut == "weak_tests":
        tnew = "import sys, pathlib\nsys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))\nimport holdings_snapshot as hs\n" + "".join("def test_%d():\n    assert True\n" % i for i in range(9))
    w(root, P.SNAP, snap)
    w(root, P.TEST_NEW, tnew)
    stray = None
    if build_mut == "stray_path":
        stray = "infra/aws/terraform/x.tf"
        w(root, stray, "x")
        changed.append(stray)
    rec = {"base_commit": base, "changed_paths": sorted(changed), "tests_total": 11, "tests_passed": 11, "mutant_tests_failed": 2,
           "default_path_unchanged": True, "refusals_tested": ["no_upload", "wrong_firm", "no_as_of", "as_of_differs_from_allowed_date", "landed_date_differs", "qa"],
           "notes": ["offline build"]}
    if build_mut == "base_mismatch":
        rec["changed_paths"] = [P.SNAP]
    w(root, P.BUILD_REC, rec)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "work")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=200)
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def mut(base, path, value, delete=False):
    o = copy.deepcopy(base)
    cur = o
    for k in path[:-1]:
        cur = cur[k]
    if delete:
        del cur[path[-1]]
    else:
        cur[path[-1]] = value
    return o


ALL = ["IB193-%d-AC%d" % (c, a) for c in (1, 2, 3) for a in (1, 2, 3)]
bad = 0

root = make_root()
for cid in ALL:
    r = run(root, cid)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))
shutil.rmtree(root, ignore_errors=True)

NEG = [
    ("IB193-1-AC1", "re-measure Inflection on the wrong pin", mut(APPLY, ["remeasure", "pins", "inflection"], "2026-10-12"), None),
    ("IB193-1-AC1", "Inflection gate differs from the packet", mut(APPLY, ["remeasure", "firms", "inflection", "gate_after"], "REFUSED"), None),
    ("IB193-1-AC1", "a third changed member", mut(APPLY, ["digest_gate", "cottonwood", "changed_members"], ["holdings_snapshot.py", "classify.py"]), None),
    ("IB193-1-AC1", "a Branch B version off the packet", mut(APPLY, ["branch_b_reread", "49financial", "bundle_version_id"], "OTHER"), None),
    ("IB193-1-AC1", "the CTO half unsigned", mut(APPLY, ["gates", "cto_half_signed"], False), None),
    ("IB193-1-AC1", "two newer manifest versions", mut(APPLY, ["branch_b_reread", "inflection", "manifest_anchor_at_mint", "newer_versions"], 2), None),
    ("IB193-1-AC1", "a newer manifest not written by the fire", mut(APPLY, ["branch_b_reread", "49financial", "manifest_anchor_at_mint", "written_by_scheduled_fire"], False), None),
    ("IB193-1-AC1", "a newer manifest dated other than T-1", mut(APPLY, ["branch_b_reread", "49financial", "manifest_anchor_at_mint", "published_date"], "2026-10-14"), None),
    ("IB193-1-AC1", "an equal anchor that claims newer versions", mut(APPLY, ["branch_b_reread", "cottonwood", "manifest_anchor_at_mint", "newer_versions"], 1), None),
    ("IB193-1-AC2", "a mint inside 30 minutes of the fire", mut(APPLY, ["window", "mint_end_utc"], "2026-10-15T13:50:00Z"), None),
    ("IB193-1-AC2", "a mint before the day's fires read Success", mut(APPLY, ["window", "mint_start_utc"], "2026-10-14T14:00:00Z"), None),
    ("IB193-1-AC2", "a mint that did not move the bundle", mut(APPLY, ["mints", "inflection", "after_version_id"], P.BRANCH_B_BUNDLE["inflection"]), None),
    ("IB193-1-AC2", "a wrong T-1", mut(APPLY, ["business_date_statement", "t_minus_1"], "2026-10-13"), None),
    ("IB193-1-AC2", "a statement made after the fire", mut(APPLY, ["business_date_statement", "stated_at_utc"], "2026-10-15T15:00:00Z"), None),
    ("IB193-1-AC3", "a firm stamped the wrong date", mut(APPLY, ["after_read", "49financial", "stamp"], "2026-10-13"), None),
    ("IB193-1-AC3", "a hold with the frontier moved", mut(APPLY, ["after_read", "inflection", "served_latest_date_after"], "2026-10-14"), None),
    ("IB193-1-AC3", "a counter above its bound", mut(APPLY, ["counters", "lambda_invokes"], 1), None),
    ("IB193-1-AC3", "the gap changed", mut(APPLY, ["gap_2026_10_08", "unchanged"], False), None),
    ("IB193-2-AC2", "no assertion block", None, "no_block"),
    ("IB193-2-AC2", "tests that do not discriminate", None, "weak_tests"),
    ("IB193-2-AC3", "a path outside the grant", None, "stray_path"),
    ("IB193-2-AC3", "changed_paths differs from the diff", None, "base_mismatch"),
    ("IB193-3-AC1", "OOM verdict with no release memory read", mut(KILL, ["verdict"], "OOM"), None),
    ("IB193-3-AC2", "a destructive host command", mut(KILL, ["host_commands"], [{"command": "journalctl -k; systemctl restart amazon-ssm-agent", "read_only": True}]), None),
    ("IB193-3-AC2", "three host commands", mut(KILL, ["host_commands"], [KILL["host_commands"][0]] * 3), None),
    ("IB193-3-AC3", "a long digit run", mut(KILL, ["notes"], ["account 123456789012 seen"]), None),
    ("IB193-3-AC3", "a counter above 0", mut(KILL, ["service_restarts"], 1), None),
]
for cid, label, rec, bm in NEG:
    if cid.startswith("IB193-1"):
        root = make_root(apply=rec)
    elif cid.startswith("IB193-3"):
        root = make_root(kill=rec)
    else:
        root = make_root(build_mut=bm)
    r = run(root, cid)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-48s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))
    shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
