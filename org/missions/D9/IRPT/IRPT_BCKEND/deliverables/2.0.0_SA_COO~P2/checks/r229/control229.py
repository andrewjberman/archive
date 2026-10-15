"""Positive control and negatives for p229_cells.py (run by the issuer at the cut). Usage: python control229.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r229/p229_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p229_cells as P  # noqa: E402

H64 = "ab" * 32
GOOD = {
    "gates": {"addendum_blob": P.BLOB, "both_halves_signed": True, "builds_merged": {"IB-pr-586": True, "IB-pr-594": True},
              "dispatch_object": {"live_sha256": H64, "repository_sha256": H64, "equal": True}, "roster_column_present": "accountStartDate",
              "runner_role": {"secret_read_allowed": True, "feed_prefix_write_allowed": True, "cross_bucket_write_checked": True},
              "notification_filter": {"printed": True, "matches_feed_key": False}, "household_count": 294, "request_bound": 294, "write_set_inflection_only": True},
    "apply": {"script": {"uploaded_sha256": H64, "repository_sha256": H64}, "trading_calendar": {"uploaded_sha256": "cd" * 32, "repository_sha256": "cd" * 32},
              "sidecar": {"sha256": "ef" * 32, "generated_from": "address()", "keys": ["bucket", "bronze_key_prefix", "silver_key_prefix"]},
              "dispatch_edit": {"saved_copy_sha256": H64, "rows_added": 1, "chain_entries_added": 3, "chains_carrying_perf": 3, "other_lines_changed": 0},
              "rollback_performed": False},
    "first_run": {"exit_code": 0, "tolerated_failure": False, "requests_made": 294, "calc_gross_of_fees_false_on_every_request": True, "keys_outside_inflection_scope": 0,
                  "coverage": {"denominator": 800, "returned": 790, "absent": 10, "absent_by_reason": {"NO_GROUP": 4, "NO_START_DATE_AT_SOURCE": 5, "SERIES_ENDED_AT_SOURCE": 1},
                               "zero_returns_written": 0, "value_stored": "daily_factor"}},
    "counters": {"function_updates": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "terraform_changes": 0, "existing_keys_changed": 0, "secrets_printed": 0},
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
    ("594_not_merged", "AC1", mut(["gates", "builds_merged", "IB-pr-594"], False)),
    ("dispatch_differs", "AC1", mut(["gates", "dispatch_object", "equal"], False)),
    ("no_roster_column", "AC1", mut(["gates", "roster_column_present"], "x")),
    ("secret_not_readable", "AC1", mut(["gates", "runner_role", "secret_read_allowed"], False)),
    ("filter_matches", "AC1", mut(["gates", "notification_filter", "matches_feed_key"], True)),
    ("bound_not_household_count", "AC1", mut(["gates", "request_bound"], 500)),
    ("upload_differs", "AC2", mut(["apply", "script", "uploaded_sha256"], "00" * 32)),
    ("sidecar_not_from_builder", "AC2", mut(["apply", "sidecar", "generated_from"], "hand")),
    ("dispatch_other_lines", "AC2", mut(["apply", "dispatch_edit", "other_lines_changed"], 2)),
    ("entries_not_all_chains", "AC2", mut(["apply", "dispatch_edit", "chain_entries_added"], 2)),
    ("tolerated_failure", "AC3", mut(["first_run", "tolerated_failure"], True)),
    ("coverage_not_summing", "AC3", mut(["first_run", "coverage", "returned"], 700)),
    ("a_zero_written", "AC3", mut(["first_run", "coverage", "zero_returns_written"], 3)),
    ("summary_stored", "AC3", mut(["first_run", "coverage", "value_stored"], "performance")),
    ("over_the_bound", "AC3", mut(["first_run", "requests_made"], 400)),
    ("key_outside_scope", "AC3", mut(["first_run", "keys_outside_inflection_scope"], 1)),
    ("existing_key_changed", "AC3", mut(["counters", "existing_keys_changed"], 1)),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c229_"))
    for rel, txt in ((P.COO_HALF, "SIGNED blob " + P.BLOB[:10]), (P.CTO_HALF, "SIGNED blob " + P.BLOB[:10]), (P.ADD, "addendum")):
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
    expect("clean", "IB229-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IB229-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c229_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IB229-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
