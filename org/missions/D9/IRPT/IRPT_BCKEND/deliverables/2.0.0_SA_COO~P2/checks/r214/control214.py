"""Positive control and negatives for p214_cells.py (issuer, at the cut). Usage: python control214.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r214/p214_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p214_cells as P  # noqa: E402

WR = "data/assets/scripts/gold/investor_reporting/holdings_49f.py"


def build():
    root = Path(tempfile.mkdtemp(prefix="c214_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / WR).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# stub"] * 40
    lines[14] = "def write_dim_balance(partition):"
    (root / WR).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def record():
    days = ["2026-10-08", "2026-10-09", "2026-10-12", "2026-10-13", "2026-10-14"]
    parts = [{"day": d, "partition_present": True, "row_count": 5000 + i, "account_present": d in ("2026-10-08", "2026-10-09", "2026-10-12")} for i, d in enumerate(days)]
    return {"base_commit": "a" * 40, "read_date": "2026-10-15", "partitions": parts, "served_snapshot_day": "2026-10-12", "candidate_day_refused": "2026-10-13",
            "gap": {"first_absent_day": "2026-10-13", "claim": "measured"},
            "upstream_writer": {"site": {"file": WR, "line": 15, "identifier": "def write_dim_balance"}, "name": "the dim_balance builder of the 49 Financial custody channel, run by its scheduled job",
                                "run_2026_10_13": {"status": "succeeded", "claim": "inferred", "row_counts": {"prior_day": 5002, "day": 5003, "next_day": 5004}, "truncation_signal": False,
                                                   "statement": "The partition for 2026-10-13 has a normal row count beside its neighbours and no failed step is recorded; why it omits the account is not shown by the run."}},
            "self_clears": {"claim": "measured", "account_present_on_2026_10_14": False, "statement": "The account is absent from the 2026-10-14 partition as well, so the refusal does not clear on its own."},
            "remedy": {"path": "a custodian-confirmed TERMINATED mark if the account is closed, a partner-firm contact drafted for Andrew; otherwise a re-landed custody row", "partner_contact_needed": True},
            "notes": ["read 5 dim_balance partitions, row counts and the account's presence only", "no account id is recorded anywhere in this record", "not read: the custodian's own system"],
            **{k: 0 for k in P.P6.BOUND}}


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
    ("AC1", "day_missing", lambda r: r["partitions"].pop(2)),
    ("AC1", "extra_day", lambda r: r["partitions"].insert(0, {"day": "2026-10-07", "partition_present": True, "row_count": 1, "account_present": True})),
    ("AC1", "present_without_count", lambda r: sp(r, ["partitions", 1, "row_count"], 0)),
    ("AC1", "absent_with_account", lambda r: sp(r, ["partitions", 4], {"day": "2026-10-14", "partition_present": False, "row_count": None, "account_present": True})),
    ("AC1", "account_present_on_gap_day", lambda r: sp(r, ["partitions", 3, "account_present"], True)),
    ("AC1", "served_day_wrong", lambda r: sp(r, ["served_snapshot_day"], "2026-10-09")),
    ("AC1", "gap_day_wrong", lambda r: sp(r, ["gap", "first_absent_day"], "2026-10-12")),
    ("AC2", "writer_line_wrong", lambda r: sp(r, ["upstream_writer", "site", "line"], 3)),
    ("AC2", "run_status_unknown_word", lambda r: sp(r, ["upstream_writer", "run_2026_10_13", "status"], "maybe")),
    ("AC2", "row_counts_missing", lambda r: sp(r, ["upstream_writer", "run_2026_10_13", "row_counts"], {"prior_day": 1})),
    ("AC2", "truncation_not_boolean", lambda r: sp(r, ["upstream_writer", "run_2026_10_13", "truncation_signal"], "no")),
    ("AC3", "self_clears_claim_bad", lambda r: sp(r, ["self_clears", "claim"], "maybe")),
    ("AC3", "remedy_short", lambda r: sp(r, ["remedy", "path"], "short")),
    ("AC3", "partner_flag_missing", lambda r: sp(r, ["remedy", "partner_contact_needed"], "yes")),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["vendor_requests_sent"], 1)),
    ("AC3", "long_digit_run", lambda r: sp(r, ["notes"], ["an id 123456789012 leaked into this long enough line", "second line that is long enough to count here", "third line that is long enough to count here"])),
]
bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
rec = record()
write(root, rec)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB214-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB214-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
