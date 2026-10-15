"""Positive control and negatives for p233_cells.py (run by the issuer at the cut). Usage: python control233.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r233/p233_cells.py"
sys.path.insert(0, str(CHECK.parent))
for sub in ("r196", "r218", "r220"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p233_cells as P  # noqa: E402

SRC_REAL = REAL / P.SRC
SRC_DOC = json.loads(SRC_REAL.read_text(encoding="utf-8"))
HASHES = [m["sha256_transplanted"] for m in SRC_DOC["firms"]["49financial"]["changed_members"]]

GOOD = {"base_commit": "a" * 40, "read_date": "2026-10-15", "claim": "measured", "firm_scope": "49financial",
        "method": "Built the 49 Financial candidate from the live pinned inputs with the TRANSPLANT tree of IB-pr-595 (pin 1 plus the exemption), then gated it twice: WITHOUT the evidence provider and WITH it; classified every lost account, in process, nothing written.",
        "candidate_day": "2026-10-14", "served_day": "2026-10-12", "builder": "build_snapshot over VersionedInputs",
        "tree": {"holdings_snapshot_sha256": HASHES[0], "publication_sha256": HASHES[1], "cusip_port_present": True, "one_date_bypass_absent": True},
        "anatomy": {
            "lost_accounts": {"total": 5, "exempted": 1, "remaining": 4,
                              "classes": {"exempted_absent_at_source": 1, "closed_by_directory": 2, "in_source_with_positions": 1, "evidence_incomplete": 0, "other": 1}},
            "classified_security_lost": {"total": 3, "served_placed_total": 900, "candidate_unclassified_total": 40,
                                         "reading": "Three securities the served snapshot places by class are unclassified in the candidate; the classification input for them is absent."},
            "conditions_remaining": ["account_lost", "classified_security_lost"],
            "conditions_detail": [
                {"condition": "account_lost", "tripped": 4, "denominator": 7664, "threshold": "any served account the candidate lacks that is neither closed nor exempted trips the condition", "value": "4 of 7664 served accounts lost after the exemption", "cause_split": {"source": 2, "join": 1, "undetermined": 1}},
                {"condition": "classified_security_lost", "tripped": 3, "denominator": 900, "threshold": "any served placed security that is unclassified in the candidate trips the condition", "value": "3 of 900 served placed securities", "cause_split": {"source": 0, "join": 3, "undetermined": 0}}]},
        "delta": {"without": {"outcome": "REFUSED", "conditions": ["account_lost", "classified_security_lost"], "node_count": 1000, "account_count": 50},
                  "with": {"outcome": "REFUSED", "conditions": ["account_lost", "classified_security_lost"], "node_count": 1000, "account_count": 50,
                           "exempted_accounts": 1, "first_absent_day": "2026-10-13", "since_bound_reached": False, "listing_applied": False},
                  "exemption_alone": {"nodes_added": 0, "accounts_added": 0, "amount_added_usd": 0, "other_nodes_changed": 0},
                  "second_fire": {"exempt_again": True, "outcome_account_lost": True}},
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
        "notes": ["every count is over one build of the candidate on the transplant tree", "ids are never recorded, only class counts",
                  "the served snapshot was read through the publisher read path only"]}


def mut(fn):
    r = copy.deepcopy(GOOD)
    fn(r)
    return r


NEGS = [
    ("tree_hash_differs", "AC1", lambda r: r["tree"].update(holdings_snapshot_sha256="0" * 64)),
    ("cusip_port_absent", "AC1", lambda r: r["tree"].update(cusip_port_present=False)),
    ("bypass_present", "AC1", lambda r: r["tree"].update(one_date_bypass_absent=False)),
    ("wrong_firm", "AC1", lambda r: r.update(firm_scope="cottonwood")),
    ("method_without_transplant", "AC1", lambda r: r.update(method="x" * 140 + " without")),
    ("classes_do_not_sum", "AC2", lambda r: r["anatomy"]["lost_accounts"]["classes"].update(other=5)),
    ("csl_over_served", "AC2", lambda r: r["anatomy"]["classified_security_lost"].update(total=1000)),
    ("conditions_disagree", "AC2", lambda r: r["anatomy"].update(conditions_remaining=["account_lost"])),
    ("delta_counts_wrong", "AC2", lambda r: r["delta"]["with"].update(node_count=1005)),
    ("delta_other_node_changed", "AC2", lambda r: r["delta"]["exemption_alone"].update(other_nodes_changed=2)),
    ("delta_amount_added", "AC2", lambda r: r["delta"]["exemption_alone"].update(amount_added_usd=5)),
    ("second_fire_not_exempt", "AC2", lambda r: r["delta"]["second_fire"].update(exempt_again=False)),
    ("delta_refuses_but_none_remaining", "AC2", lambda r: r["anatomy"]["lost_accounts"].update(total=1, remaining=0, classes={"exempted_absent_at_source": 1, "closed_by_directory": 0, "in_source_with_positions": 0, "evidence_incomplete": 0, "other": 0}) or r["anatomy"].update(conditions_remaining=["classified_security_lost"]) or r["anatomy"]["conditions_detail"][0].update(tripped=0)),
    ("counter_nonzero", "AC3", lambda r: r.update(rows_written=2)),
    ("short_notes", "AC3", lambda r: r.update(notes=["a", "b", "c"])),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c233_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    for rel, src in ((P.REC, None), (P.SRC, SRC_REAL)):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        if src is None:
            f.write_text(json.dumps(rec), encoding="utf-8")
        else:
            shutil.copy(src, f)
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


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB233-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(mut(fn))
    expect(label, "IB233-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c233_"))
expect("no_record", "IB233-1-AC2", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
