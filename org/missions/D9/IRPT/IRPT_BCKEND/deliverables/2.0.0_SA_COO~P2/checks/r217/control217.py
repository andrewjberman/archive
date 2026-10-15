"""Positive control and negatives for p217_cells.py (run by the issuer at the cut, never by the applier).

Usage: python control217.py <real_repo_root>
Builds temp roots with stub halves, a ledger entry and a synthetic apply record at the real relative paths, runs every criterion expecting PASS,
then applies each mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r217/p217_cells.py"
sys.path.insert(0, str(CHECK.parent))
import p217_cells as P  # noqa: E402

LEDGER = "org/critical_paths/change_management/20261015T150000Z_irpt-ycharts-generate-456_deploy.md"
GOOD = {
    "gates": {"packet_sha256": P.PACKET_SHA, "both_halves_signed": True,
              "open_markers": {"worktrees_read": 9, "marker_files_read": 12, "naming_the_function_with_open_trunk_ledger": 0, "stale_views_naming_the_function": 2},
              "open_ledgers": {"ledger_files_read": 1860, "open_naming_the_function": 0}},
    "start_read": {"code_sha256": P.LIVE_B64}, "ledger_entry": LEDGER, "branch_b_version_id": "vers.synthetic.1",
    "before": {"live_zip_commentary_requested": {"submission.py": 0, "acceptance.py": 0, "contracts/AnalysisSubmissionRequest.schema.json": 0}, "accepted_request_item_sha256": "ab" * 32},
    "apply": {"built_code_sha256": P.BUILT_B64, "plan": {"add": 0, "change": 1, "destroy": 0}, "safe_apply_rc": 0, "path": "terraform-safe-apply"},
    "after": {"code_sha256": P.BUILT_B64, "replan_changes": 0, "changed_members": sorted(P.MEMBERS), "import_census_failed": {},
              "replay_at_pin": {"arms": 53, "unexpected": 0}, "accepted_request_item_sha256": "ab" * 32, "composition_test": {"passed": 6, "failed": 0}},
    "source_map_rows": {"committed": True, "function": P.FN, "rows_changed": 3, "siblings_changed": 0},
    "rollback_performed": False,
    "unexercised_live": "That the released function ACCEPTS a submission is UNEXERCISED LIVE until the DEV FWD-1 run.",
    "health_proof": {"deployed_member_sha256": dict(P.MEMBERS), "window_start_utc": "2026-10-15T15:10:00Z", "window_end_utc": "2026-10-15T15:25:00Z",
                     "invocations_in_window": 4, "errors_in_window": 0},
    "counters": {"function_updates": 1, "lambda_invokes": 1, "iam_changes": 0, "route_changes": 0, "env_changes": 0, "table_writes": 0, "figures_written": 0,
                 "files_deleted": 0, "sibling_functions_moved": 0, "vendor_requests_sent": 0, "jobs_queued": 0},
}


def mutate(path, value):
    def f(r):
        r = copy.deepcopy(r)
        cur = r
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return r
    return f


NEGS = [
    ("wrong_packet_sha", "AC1", mutate(["gates", "packet_sha256"], "0" * 64)),
    ("open_ledger", "AC1", mutate(["gates", "open_ledgers", "open_naming_the_function"], 1)),
    ("stale_start_digest", "AC1", mutate(["start_read", "code_sha256"], "AAAA")),
    ("live_zip_has_the_member", "AC1", mutate(["before", "live_zip_commentary_requested", "submission.py"], 2)),
    ("wrong_built_digest", "AC2", mutate(["apply", "built_code_sha256"], "AAAA")),
    ("plan_destroys", "AC2", mutate(["apply", "plan"], {"add": 0, "change": 1, "destroy": 1})),
    ("fifth_member", "AC2", mutate(["after", "changed_members"], sorted(P.MEMBERS) + ["generate_installed.py"])),
    ("sibling_moved", "AC2", mutate(["source_map_rows", "siblings_changed"], 1)),
    ("rolled_back", "AC2", mutate(["rollback_performed"], True)),
    ("replay_arm_differs_unexplained", "AC3", mutate(["after", "replay_at_pin", "unexpected"], 2)),
    ("item_changed", "AC3", mutate(["after", "accepted_request_item_sha256"], "cd" * 32)),
    ("errors_in_window", "AC3", mutate(["health_proof", "errors_in_window"], 2)),
    ("table_written", "AC3", mutate(["counters", "table_writes"], 1)),
    ("no_unexercised_statement", "AC3", mutate(["unexercised_live"], "all good")),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c217_"))
    for rel, txt in ((P.COO_HALF, "SIGNED for the blast radius below"), (P.COO_ADD, "COO half addendum"), (P.CTO_ADD, "CTO half -- SIGNED on blob x"),
                     (LEDGER, "branch b vers.synthetic.1 OPEN")):
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


EXPL = copy.deepcopy(GOOD)
EXPL["after"]["replay_at_pin"] = {"arms": 17, "unexpected": 3, "explained_unexpected": 3, "explanation": "The packet recorded the live side before release 29; the live side now carries release 29's acting_principal_id pairing, so three arms read identical now."}
root = build(EXPL)
expect("explained_arms", "IB217-1-AC3", root, True)
shutil.rmtree(root, ignore_errors=True)
root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB217-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IB217-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c217_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IB217-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
