"""Positive control and negatives for p218_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control218.py <real_repo_root>
Builds temp roots holding the real lib/trading_calendar.py and a synthetic record, runs every criterion expecting PASS, then applies each mutation
expecting the NAMED criterion to FAIL. The temp roots are removed.
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r218/p218_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p218_cells as P  # noqa: E402

BASE = {"base_commit": "a" * 40, "read_date": "2026-10-15", "claim": "measured", "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0,
        "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
        "notes": ["the candidate was built from the live pinned inputs, not uploaded", "the served snapshot was read through the publisher read path only",
                  "the second fire is simulated by serving the listed snapshot, nothing is written"]}


def firm(exempted=1):
    wo = {"outcome": "REFUSED", "conditions": ["account_lost"] if exempted else [], "node_count": 1000, "account_count": 50}
    if not exempted:
        wo["outcome"] = "PUBLISHED"
    wi = {"outcome": "PUBLISHED", "conditions": [], "node_count": 1000 + exempted, "account_count": 50 + exempted, "exempted_accounts": exempted,
          "first_absent_day": "2026-10-13", "since_bound_reached": False}
    return {"candidate_day": "2026-10-14", "served_day": "2026-10-12", "builder": "build_synthetic_builder", "without": wo, "with": wi,
            "exemption_alone": {"nodes_added": exempted, "accounts_added": exempted, "amount_added_usd": 0, "other_nodes_changed": 0},
            "second_fire": {"exempt_again": True, "outcome_account_lost": False}}


REC1 = {**BASE, "method": "Built the candidate of each firm from the live pinned inputs with the HEAD code, then gated it twice: WITHOUT the evidence provider and WITH it.",
        "firms": {"49financial": firm(), "cottonwood": firm()}}
REC2 = {**BASE, "method": "Ran the producer's pure return over each split day of the channel BEFORE the adjustment (no split ratios) and AFTER it, same inputs.",
        "firm_scope": "49financial", "split_days": ["2026-04-21", "2026-05-08"],
        "totals": {"account_days_run": 1000, "account_days_changed": 80, "account_days_holding_a_split_security": 90, "securities_adjusted": 7, "securities_ratio_absent": 1,
                   "at_or_below_minus_50pct_before": 60, "at_or_below_minus_50pct_after": 3, "status_moves": {"IMPLAUSIBLE->OK": 55}},
        "per_day": [{"day": "2026-04-21", "account_days_changed": 70}, {"day": "2026-05-08", "account_days_changed": 10}]}


def mut(rec, fn):
    r = copy.deepcopy(rec)
    fn(r)
    return r


NEG1 = [
    ("one_firm_only", "IB218-1-AC1", lambda r: r["firms"].pop("cottonwood")),
    ("count_mismatch", "IB218-1-AC2", lambda r: r["firms"]["49financial"]["with"].update(node_count=5000)),
    ("other_node_changed", "IB218-1-AC2", lambda r: r["firms"]["49financial"]["exemption_alone"].update(other_nodes_changed=3)),
    ("amount_added", "IB218-1-AC2", lambda r: r["firms"]["cottonwood"]["exemption_alone"].update(amount_added_usd=12.5)),
    ("still_account_lost", "IB218-1-AC2", lambda r: r["firms"]["cottonwood"]["with"].update(outcome="REFUSED", conditions=["account_lost"])),
    ("no_second_fire", "IB218-1-AC2", lambda r: r["firms"]["49financial"]["second_fire"].update(exempt_again=False)),
    ("long_digits", "IB218-1-AC3", lambda r: r.update(notes=r["notes"] + ["an identifier 1234567890123 slipped into this line of notes"])),
    ("counter_nonzero", "IB218-1-AC3", lambda r: r.update(aws_writes_made=1)),
]
NEG2 = [
    ("no_apr21", "IB218-2-AC1", lambda r: (r.update(split_days=["2026-05-08"]), r.update(per_day=[r["per_day"][1]]))),
    ("not_trading_day", "IB218-2-AC1", lambda r: r.update(split_days=["2026-04-21", "2026-05-09"])),
    ("changed_over_held", "IB218-2-AC2", lambda r: r["totals"].update(account_days_changed=95)),
    ("minus50_rises", "IB218-2-AC2", lambda r: r["totals"].update(at_or_below_minus_50pct_after=70)),
    ("per_day_sum", "IB218-2-AC2", lambda r: r["per_day"][0].update(account_days_changed=1)),
    ("short_notes", "IB218-2-AC3", lambda r: r.update(notes=["short", "short", "short"])),
]


def build(rec1, rec2):
    root = Path(tempfile.mkdtemp(prefix="c218_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    for rel, rec in ((P.REC1, rec1), (P.REC2, rec2)):
        f = root / rel
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


root = build(REC1, REC2)
for c in ("IB218-1", "IB218-2"):
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "%s-%s" % (c, ac), root, True)
shutil.rmtree(root, ignore_errors=True)
for label, cid, fn in NEG1:
    root = build(mut(REC1, fn), REC2)
    expect(label, cid, root, False)
    shutil.rmtree(root, ignore_errors=True)
for label, cid, fn in NEG2:
    root = build(REC1, mut(REC2, fn))
    expect(label, cid, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c218_"))
for cid in ("IB218-1-AC1", "IB218-2-AC2"):
    expect("no_record", cid, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
