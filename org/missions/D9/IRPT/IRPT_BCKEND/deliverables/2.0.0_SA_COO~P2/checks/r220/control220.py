"""Positive control and negatives for p220_cells.py (run by the issuer at the cut). Usage: python control220.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r220/p220_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent.parent / "r218"))
import p220_cells as P  # noqa: E402

GOOD = {"base_commit": "a" * 40, "read_date": "2026-10-15", "claim": "measured", "firm_scope": "49financial",
        "method": "Built the 49 Financial candidate once from the live pinned inputs and classified every lost account by the evidence readers' four partitions, in process, nothing written.",
        "candidate_day": "2026-10-14", "served_day": "2026-10-12",
        "lost_accounts": {"total": 5, "exempted": 1, "remaining": 4,
                          "classes": {"exempted_absent_at_source": 1, "closed_by_directory": 2, "in_source_with_positions": 1, "evidence_incomplete": 0, "other": 1}},
        "classified_security_lost": {"total": 3, "served_placed_total": 900, "candidate_unclassified_total": 40,
                                     "reading": "Three securities the served snapshot places by class are unclassified in the candidate; the classification input for them is absent."},
        "conditions_remaining": ["account_lost", "classified_security_lost"],
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
        "notes": ["every count is over one build of the candidate, nothing re-built per class", "ids are never recorded, only class counts",
                  "the served snapshot was read through the publisher read path only"]}


def mut(fn):
    r = copy.deepcopy(GOOD)
    fn(r)
    return r


NEGS = [
    ("classes_do_not_sum", "AC2", lambda r: r["lost_accounts"]["classes"].update(other=5)),
    ("exempted_mismatch", "AC2", lambda r: r["lost_accounts"].update(exempted=2)),
    ("remaining_wrong", "AC2", lambda r: r["lost_accounts"].update(remaining=3)),
    ("csl_over_served", "AC2", lambda r: r["classified_security_lost"].update(total=1000)),
    ("conditions_disagree", "AC2", lambda r: r.update(conditions_remaining=["account_lost"])),
    ("missing_class", "AC2", lambda r: r["lost_accounts"]["classes"].pop("other")),
    ("wrong_firm", "AC1", lambda r: r.update(firm_scope="cottonwood")),
    ("counter_nonzero", "AC3", lambda r: r.update(rows_written=2)),
    ("short_notes", "AC3", lambda r: r.update(notes=["a", "b", "c"])),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c220_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
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
    print("%s %-12s %-22s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB220-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(mut(fn))
    expect(label, "IB220-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c220_"))
expect("no_record", "IB220-1-AC2", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
