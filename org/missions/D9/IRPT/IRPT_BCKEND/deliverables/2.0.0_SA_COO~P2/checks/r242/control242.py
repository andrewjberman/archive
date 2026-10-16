"""Positive control and negatives for p242_cells.py (run by the issuer at the cut). Usage: python control242.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r242/p242_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p242_cells as P  # noqa: E402

COO_TXT = "COO half revision 3: SIGNED for the candidate 61537d6d9fac83e6.\n"
CTO_TXT = "CTO half: SIGNED at the candidate 61537d6d9fac83e6.\n"

GOOD = {
    "gates": {"addendum_blob": "", "both_halves_signed": True, "one_change_at_a_time": True, "exemption_pair_applied_and_ledger_closed": True},
    "branch_b_reread": {"bundle_version_id": "v1", "manifest_anchor_at_mint": "m1", "live_bundle_sha256": "d2eaf3056c1d" + "0" * 52},
    "digest_gate": {"built_bundle_sha256": P.DIGEST, "changed_members": list(P.MEMBERS), "publication_equal_live": True, "allow_older_date_count": 0,
                    "cusip_lines": 12, "cusip_lines_live": 12},
    "remeasure": {"verdict": "REFUSED_NO_NODE_MOVES", "node_set_unchanged": True},
    "window": {"last_fire_all_success_utc": "2026-10-16T14:30:00Z", "mint_start_utc": "2026-10-16T15:00:00Z", "mint_end_utc": "2026-10-16T15:10:00Z",
               "next_fire_utc": "2026-10-19T14:15:00Z", "minutes_before_next_fire": 4000},
    "ledger": {"entry": "org/critical_paths/change_management/x.md", "opened_before_the_mint": True},
    "mint": {"before_version_id": "v1", "after_version_id": "v2", "after_sha256_equals_built": True},
    "business_date_statement": {"stated_at_utc": "2026-10-16T15:11:00Z", "fire_utc": "2026-10-19T14:15:00Z", "t_minus_1": "2026-10-16"},
    "after_read": {"outcome": "STAMPED_T_MINUS_1", "t1_partition_under_it": True,
                   "node_set_diff": {"nodes_added_vs_signed_bundle": 0, "nodes_removed": 0, "nodes_changed": 0},
                   "evidence": {"listed_accounts": 3, "values": {"smartx_map_present": 1, "smartx_map_absent": 1, "unread": 1}, "missing_or_second_key": 0},
                   "no_closed_name_in_manifest": True, "amount_shown_for_listed": False},
    "rollback_performed": False,
    "counters": {"bundles_minted": 1, "other_bucket_writes": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0,
                 "files_deleted": 0, "markers_closed": 0},
}


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, coo=COO_TXT):
    root = Path(tempfile.mkdtemp(prefix="c242_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel, txt in ((P.COO_HALF, coo), (P.CTO_HALF, CTO_TXT)):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(txt.encode("utf-8"))
    rec = copy.deepcopy(GOOD)
    rec["gates"]["addendum_blob"] = subprocess.run(["git", "hash-object", "--stdin"], input=coo.encode("utf-8"), capture_output=True).stdout.decode().strip()
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
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


def put(path, value):
    def fn(r):
        d = r
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return fn


NEGS = [
    ("wrong_blob", "AC1", put(["gates", "addendum_blob"], "0" * 40)),
    ("exemption_not_applied", "AC1", put(["gates", "exemption_pair_applied_and_ledger_closed"], False)),
    ("live_not_signed_bundle", "AC1", put(["branch_b_reread", "live_bundle_sha256"], "bce6e936c274" + "0" * 52)),
    ("digest_differs", "AC1", put(["digest_gate", "built_bundle_sha256"], "7" * 64)),
    ("third_member", "AC1", put(["digest_gate", "changed_members"], list(P.MEMBERS) + ["lib/opal_naming.py"])),
    ("publication_moved", "AC1", put(["digest_gate", "publication_equal_live"], False)),
    ("bypass_present", "AC1", put(["digest_gate", "allow_older_date_count"], 1)),
    ("cusip_reversal", "AC1", put(["digest_gate", "cusip_lines"], 0)),
    ("node_set_moved_at_remeasure", "AC1", put(["remeasure", "node_set_unchanged"], False)),
    ("mint_before_the_fires", "AC2", put(["window", "mint_start_utc"], "2026-10-16T13:00:00Z")),
    ("mint_too_close_to_fire", "AC2", put(["window", "minutes_before_next_fire"], 10)),
    ("ledger_after_mint", "AC2", put(["ledger", "opened_before_the_mint"], False)),
    ("mint_did_not_move", "AC2", put(["mint", "after_version_id"], "v1")),
    ("landed_bytes_differ", "AC2", put(["mint", "after_sha256_equals_built"], False)),
    ("statement_after_fire", "AC2", put(["business_date_statement", "stated_at_utc"], "2026-10-19T14:20:00Z")),
    ("node_added", "AC3", put(["after_read", "node_set_diff", "nodes_added_vs_signed_bundle"], 1)),
    ("evidence_missing", "AC3", put(["after_read", "evidence", "missing_or_second_key"], 1)),
    ("evidence_sum_wrong", "AC3", put(["after_read", "evidence", "listed_accounts"], 5)),
    ("stamp_no_partition", "AC3", put(["after_read", "t1_partition_under_it"], False)),
    ("amount_shown", "AC3", put(["after_read", "amount_shown_for_listed"], True)),
    ("rollback", "AC3", put(["rollback_performed"], True)),
    ("counter_nonzero", "AC3", put(["counters", "iam_changes"], 1)),
    ("wrong_minted_count", "AC3", put(["counters", "bundles_minted"], 2)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB242-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB242-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(coo="COO half: SIGNED for the candidate deadbeef.\n")
expect("half_names_another_digest", "IB242-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
