"""Positive control and negatives for p213_cells.py (issuer, at the cut). Usage: python control213.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r213/p213_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p213_cells as P  # noqa: E402

PUB = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"


def build():
    root = Path(tempfile.mkdtemp(prefix="c213_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / PUB).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# stub"] * 40
    lines[9] = "def closed_account_ids(s3, bucket, firm):"
    lines[19] = "    entry['status'] = 'TERMINATED'"
    (root / PUB).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def st(line, ident):
    return {"file": PUB, "line": line, "identifier": ident}


def record():
    return {"base_commit": "a" * 40, "read_date": "2026-10-15",
            "mark": {"writer_site": st(20, "'TERMINATED'"), "guard_reading_site": st(10, "def closed_account_ids"),
                     "shape": "a directory entry carries a status field (ACTIVE, TERMINATED or UNKNOWN) and the date it took effect; no account id is recorded here.",
                     "owner": "the directory refresh function of the firm",
                     "precedent": {"terminated_entries_in_cottonwood": 2, "directory_entries": 271, "claim": "measured",
                                   "how_set": "the two existing TERMINATED entries were set by the directory refresh from the custodian's closed status; neither came from a hand edit."}},
            "evidence": {"accounts": 1, "zero_position_dates": ["2026-10-09", "2026-10-12", "2026-10-13"], "positions_on_those_dates": 0, "first_accept_date": "2026-10-09", "claim": "measured",
                         "statement": "The custodian source lists the account on three trading dates with zero positions on each, so the account is empty at the source, not silently lost."},
            "offline_guard": {"performed": True, "read_only": True, "writes": 0, "published": False, "invocation": "python offline_guard.py --mark-applied (scratch; no account id in the command)",
                              "account_listed_as": "closed_accounts_not_refused", "outcome": "WOULD_PUBLISH", "nodes_changed_other_than_the_account": 0, "accounts_leaving": 1},
            "rollback": {"statement": "The prior accepted publication (2026-10-08) returns by repointing the index to its version; no data is deleted."},
            "notes": ["read the writer and the guard in the code, counts only", "no account id is recorded; class only", "not read: the custodian's own system"],
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
    ("AC1", "writer_line_wrong", lambda r: sp(r, ["mark", "writer_site", "line"], 3)),
    ("AC1", "guard_file_missing", lambda r: sp(r, ["mark", "guard_reading_site", "file"], "data/none.py")),
    ("AC1", "shape_short", lambda r: sp(r, ["mark", "shape"], "short")),
    ("AC1", "precedent_not_counts", lambda r: sp(r, ["mark", "precedent", "directory_entries"], 0)),
    ("AC2", "two_accounts", lambda r: sp(r, ["evidence", "accounts"], 2)),
    ("AC2", "two_dates_only", lambda r: sp(r, ["evidence", "zero_position_dates"], ["2026-10-12", "2026-10-13"])),
    ("AC2", "date_not_trading", lambda r: sp(r, ["evidence", "zero_position_dates"], ["2026-10-10", "2026-10-12", "2026-10-13"])),
    ("AC2", "positions_nonzero", lambda r: sp(r, ["evidence", "positions_on_those_dates"], 4)),
    ("AC2", "first_date_mismatch", lambda r: sp(r, ["evidence", "first_accept_date"], "2026-10-12")),
    ("AC2", "claim_inferred", lambda r: sp(r, ["evidence", "claim"], "inferred")),
    ("AC3", "guard_not_performed", lambda r: sp(r, ["offline_guard", "performed"], False)),
    ("AC3", "guard_wrote", lambda r: sp(r, ["offline_guard", "writes"], 1)),
    ("AC3", "guard_published", lambda r: sp(r, ["offline_guard", "published"], True)),
    ("AC3", "account_still_refused", lambda r: sp(r, ["offline_guard", "account_listed_as"], "account_lost")),
    ("AC3", "other_nodes_changed", lambda r: sp(r, ["offline_guard", "nodes_changed_other_than_the_account"], 3)),
    ("AC3", "rollback_short", lambda r: sp(r, ["rollback", "statement"], "short")),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["aws_writes_made"], 1)),
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
    expect("clean", "IB213-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB213-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
