"""Positive control and negatives for p236_cells.py (run by the issuer at the cut). Usage: python control236.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r236/p236_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p236_cells as P  # noqa: E402

H64 = {"49financial": "d2eaf3056c1d" + "a" * 52, "cottonwood": "bc2e8f548556" + "b" * 52, "inflection": "bc2e8f548556" + "b" * 52}


def firm(f):
    return {"built_bundle_sha256": H64[f], "changed_members": list(P.MEMBERS), "allow_older_date_count": 0, "drifted_members_equal_live": True,
            "cusip_lines": 12 if f == "49financial" else 0, "cusip_lines_live": 12 if f == "49financial" else 0}


GOOD = {
    "gates": {"packet_blob": P.BLOB, "both_halves_signed": True, "one_change_at_a_time": True, "ib_pr_549_ledger_closed": True},
    "branch_b_reread": {f: {"bundle_version_id": "v-" + f, "manifest_anchor_at_mint": "m-" + f} for f in P.FIRMS},
    "digest_gate": {f: firm(f) for f in P.FIRMS},
    "remeasure": {"49financial": {"verdict": "REFUSED_NO_NODE_MOVES"},
                  "cottonwood": {"verdict": "PUBLISHED_FOUR_LISTED_ACCOUNTS", "nodes_added": 4, "other_nodes_changed": 0},
                  "inflection": {"verdict": "REFUSED_SOURCE_FRONTIER_OLDER_NO_NODE_MOVES"}},
    "window": {"last_fire_all_success_utc": "2026-10-16T14:20:00Z", "mint_start_utc": "2026-10-16T15:00:00Z", "mint_end_utc": "2026-10-16T15:40:00Z",
               "next_fire_utc": "2026-10-19T14:15:00Z", "minutes_before_next_fire": 400},
    "ledger": {"entry": "org/critical_paths/change_management/x.json", "opened_before_first_mint": True},
    "mints": {f: {"before_version_id": "v-" + f, "after_version_id": "n-" + f, "after_sha256_equals_built": True} for f in P.FIRMS},
    "business_date_statement": {"stated_at_utc": "2026-10-16T15:41:00Z", "fire_utc": "2026-10-19T14:15:00Z", "t_minus_1": "2026-10-16"},
    "after_read": {"49financial": {"outcome": "STAMPED_T_MINUS_1", "t1_partition_under_it": True},
                   "cottonwood": {"outcome": "STAMPED_T_MINUS_1", "t1_partition_under_it": True},
                   "inflection": {"outcome": "HELD_NO_NEW_PUBLICATION", "absent_partition_named": "p", "frontier_unchanged": True}},
    "exemption_after_read": {"cottonwood_listed_accounts": 4, "no_closed_name_in_manifest": True, "amount_shown_for_listed": False},
    "rollback_performed": False,
    "counters": {"bundles_minted": 3, "other_bucket_writes": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "files_deleted": 0, "markers_closed": 0},
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
    ("549_ledger_open", "AC1", mut(["gates", "ib_pr_549_ledger_closed"], False)),
    ("digest_differs", "AC1", mut(["digest_gate", "cottonwood", "built_bundle_sha256"], "00" * 32)),
    ("extra_member", "AC1", mut(["digest_gate", "49financial", "changed_members"], list(P.MEMBERS) + ["lib/opal_naming.py"])),
    ("bypass_present", "AC1", mut(["digest_gate", "inflection", "allow_older_date_count"], 1)),
    ("cusip_reversed", "AC1", mut(["digest_gate", "49financial", "cusip_lines"], 0)),
    ("cottonwood_three_nodes", "AC1", mut(["remeasure", "cottonwood", "nodes_added"], 3)),
    ("inflection_other_verdict", "AC1", mut(["remeasure", "inflection", "verdict"], "PUBLISHED_VALUES")),
    ("mint_before_fires", "AC2", mut(["window", "mint_start_utc"], "2026-10-16T14:00:00Z")),
    ("too_close_to_fire", "AC2", mut(["window", "minutes_before_next_fire"], 10)),
    ("ledger_after_mint", "AC2", mut(["ledger", "opened_before_first_mint"], False)),
    ("mint_did_not_move", "AC2", mut(["mints", "cottonwood", "after_version_id"], "v-cottonwood")),
    ("landed_differs", "AC2", mut(["mints", "49financial", "after_sha256_equals_built"], False)),
    ("statement_after_fire", "AC2", mut(["business_date_statement", "stated_at_utc"], "2026-10-19T15:00:00Z")),
    ("hold_frontier_moved", "AC3", mut(["after_read", "inflection", "frontier_unchanged"], False)),
    ("stamp_without_partition", "AC3", mut(["after_read", "cottonwood", "t1_partition_under_it"], False)),
    ("closed_name", "AC3", mut(["exemption_after_read", "no_closed_name_in_manifest"], False)),
    ("amount_shown", "AC3", mut(["exemption_after_read", "amount_shown_for_listed"], True)),
    ("rollback", "AC3", mut(["rollback_performed"], True)),
    ("counter_nonzero", "AC3", mut(["counters", "backfills"], 1)),
    ("minted_count_wrong", "AC3", mut(["counters", "bundles_minted"], 2)),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c236_"))
    for rel, txt in ((P.COO_HALF, "GIVEN blob " + P.BLOB[:10]), (P.CTO_HALF, "SIGNED blob " + P.BLOB[:10]), (P.PACKET, "packet")):
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
    expect("clean", "IB236-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
ACCEPTED = copy.deepcopy(GOOD)
ACCEPTED["remeasure"] = {"49financial": {"verdict": "PUBLISHED_TWO_LISTED_ACCOUNTS_AMOUNT_ZERO", "listed_accounts": 2, "amount_added_usd": 0, "other_nodes_changed": 0, "evidence_values_per_exempted_account": 2},
                         "cottonwood": {"verdict": "PUBLISHED_NO_LISTED_ACCOUNTS", "nodes_added": 0, "other_nodes_changed": 0},
                         "inflection": {"verdict": "PUBLISHED_NO_LISTED_ACCOUNTS"}}
ACCEPTED["exemption_after_read"]["cottonwood_listed_accounts"] = 0
root = build(ACCEPTED)
expect("accepted_counts_msg9538", "IB236-1-AC1", root, True)
expect("accepted_counts_msg9538", "IB236-1-AC3", root, True)
shutil.rmtree(root, ignore_errors=True)
for label, fn in (
    ("49f_two_amount_nonzero", mut(["remeasure", "49financial", "amount_added_usd"], 5)),
    ("49f_two_other_nodes", mut(["remeasure", "49financial", "other_nodes_changed"], 1)),
    ("49f_two_evidence_short", mut(["remeasure", "49financial", "evidence_values_per_exempted_account"], 1)),
    ("49f_three_listed", mut(["remeasure", "49financial", "listed_accounts"], 3)),
    ("cot_none_but_nodes_added", mut(["remeasure", "cottonwood", "nodes_added"], 2)),
    ("cot_none_other_nodes", mut(["remeasure", "cottonwood", "other_nodes_changed"], 1)),
):
    root = build(fn(ACCEPTED))
    expect(label, "IB236-1-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IB236-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c236_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IB236-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
