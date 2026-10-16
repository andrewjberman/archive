"""Positive control and negatives for p244_cells.py (run by the issuer at the cut). Usage: python control244.py <real_repo_root>"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r244/p244_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p244_cells as P  # noqa: E402

P6 = P.P6
P6.ROOT = REAL
DAYS = P.days()
DELTA_SHA = hashlib.sha256((REAL / P.DELTA).read_bytes()).hexdigest()


def good():
    return {
        "gates": {"pair_sha256": P.PAIR_SHA256, "addendum_blob": P.ADD_BLOB, "addendum_2_blob": P.ADD2_BLOB, "addendum_3_blob": P.ADD3_BLOB, "both_halves_signed": True,
                  "act_1": {"order_complete": True, "first_scheduled_run_read": True, "manifest_split_adjust_declared": True},
                  "function_code_sha256": P.CAND, "one_change_at_a_time": True, "act_1_ledger_closed": True,
                  "deployed_handler_date_line_present": True, "producer_date_parameter_present": True,
                  "days_equal_signed_record": True, "delta_record_sha256": DELTA_SHA},
        "stopped_at": None,
        "days": [{"day": d, "prior_version_id": "p%d" % i, "new_version_id": "n%d" % i, "rows_changed": c, "rows_changed_expected": c,
                  "other_rows_changed": 0, "changed_only_split_holders": True, "comparison_ok": True} for i, (d, c, _) in enumerate(DAYS)],
        "totals": {"days_run": 47, "account_days_changed": 1291, "invokes": 47, "ratio_absent_named_total": sum(x for _, _, x in DAYS)},
        "event_keys_sent": ["date", "source"], "event_source": P.SOURCE, "source_read_from_schedule": True, "refused_invokes": 1,
        "window": {"minutes_clear_before_fire_min": 45, "minutes_clear_after_fire_min": 40},
        "siblings_invoked": 0,
        "rollback_performed": False,
        "counters": {"lambda_invokes": 48, "version_deletes": 0, "iam_changes": 0, "schedule_changes": 0, "artifact_uploads": 0, "other_keys_written": 0,
                     "markers_closed": 0},
    }


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, cto_ok=True, alter_pair=False):
    root = Path(tempfile.mkdtemp(prefix="c244_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in (P.COO_HALF, P.COO_ADD, P.COO_ADD2, P.DELTA):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        b = (REAL / rel).read_bytes()
        f.write_bytes(b + b"x" if alter_pair and rel == P.COO_HALF else b)
    cto = "%s %s %s %s\n" % (P.PAIR_SHA256[:12], P.ADD_BLOB[:12], P.ADD2_BLOB[:10], P.ADD3_BLOB[:10])
    for rel in (P.CTO_HALF, P.CTO_ADD, P.CTO_ADD2):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(("SIGNED " if cto_ok else "UNSIGNED draft ") + cto, encoding="utf-8")
    rec = good()
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
    print("%s %-12s %-34s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


def put(path, value):
    def fn(r):
        d = r
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return fn


def day(i, **kw):
    return lambda r: r["days"][i].update(kw)


NEGS = [
    ("act_1_run_not_read", "AC1", put(["gates", "act_1", "first_scheduled_run_read"], False)),
    ("act_1_order_not_complete", "AC1", put(["gates", "act_1", "order_complete"], False)),
    ("function_not_at_candidate", "AC1", put(["gates", "function_code_sha256"], "o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok=")),
    ("act_1_ledger_open", "AC1", put(["gates", "act_1_ledger_closed"], False)),
    ("handler_line_absent", "AC1", put(["gates", "deployed_handler_date_line_present"], False)),
    ("days_not_equal_record", "AC1", put(["gates", "days_equal_signed_record"], False)),
    ("delta_record_hash_wrong", "AC1", put(["gates", "delta_record_sha256"], "0" * 64)),
    ("addendum_2_blob_wrong", "AC1", put(["gates", "addendum_2_blob"], "0" * 40)),
    ("run_stopped_midway", "AC2", put(["stopped_at"], "2025-02-14")),
    ("a_day_missing", "AC2", lambda r: r["days"].pop(10)),
    ("days_out_of_order", "AC2", lambda r: r.update(days=list(reversed(r["days"])))),
    ("a_date_outside_the_47", "AC2", day(5, day="2026-09-04")),
    ("prior_version_missing", "AC2", day(7, prior_version_id="")),
    ("write_did_not_move_the_key", "AC2", day(7, new_version_id="p7")),
    ("count_differs_from_record", "AC2", day(20, rows_changed=7777)),
    ("other_rows_changed", "AC2", day(30, other_rows_changed=2)),
    ("non_split_holder_changed", "AC2", day(31, changed_only_split_holders=False)),
    ("comparison_not_ok", "AC2", day(40, comparison_ok=False)),
    ("april_21_typed_920", "AC2", lambda r: [x.update(rows_changed=920, rows_changed_expected=920) for x in r["days"] if x["day"] == "2026-04-21"]),
    ("totals_wrong", "AC3", put(["totals", "account_days_changed"], 1290)),
    ("ratio_absent_names_wrong", "AC3", put(["totals", "ratio_absent_named_total"], 99)),
    ("event_date_only", "AC3", put(["event_keys_sent"], ["date"])),
    ("event_has_extra_key", "AC3", put(["event_keys_sent"], ["date", "source", "dry_run"])),
    ("source_is_a_sibling", "AC3", put(["event_source"], "orion")),
    ("source_not_read_from_schedule", "AC3", put(["source_read_from_schedule"], False)),
    ("refused_invoke_not_recorded", "AC3", put(["refused_invokes"], 0)),
    ("addendum_3_blob_wrong", "AC1", put(["gates", "addendum_3_blob"], "0" * 40)),
    ("window_too_close_before", "AC3", put(["window", "minutes_clear_before_fire_min"], 10)),
    ("window_too_close_after", "AC3", put(["window", "minutes_clear_after_fire_min"], 5)),
    ("sibling_invoked", "AC3", put(["siblings_invoked"], 1)),
    ("rollback", "AC3", put(["rollback_performed"], True)),
    ("version_deleted", "AC3", put(["counters", "version_deletes"], 1)),
    ("invoke_count_wrong", "AC3", put(["counters", "lambda_invokes"], 47)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB244-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB244-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(alter_pair=True)
expect("pair_bytes_changed", "IB244-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
root = build(cto_ok=False)
expect("cto_half_not_signed", "IB244-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
