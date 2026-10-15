"""Positive control and negatives for p209_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control209.py <real_repo_root>
Builds a temp tree holding the real lib/trading_calendar.py and a stub publisher file with the guard and override identifiers, writes a clean synthetic record,
runs every criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp tree is removed.
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r209/p209_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p209_cells as P  # noqa: E402

PUB = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"


def build():
    root = Path(tempfile.mkdtemp(prefix="c209_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / PUB).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# stub"] * 40
    lines[9] = '    add("account_lost", gone - closed)'
    lines[19] = "    if bypass_one_date:"
    lines[29] = "    closed = _closed_accounts(directory)"
    (root / PUB).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def record():
    return {"base_commit": "a" * 40, "read_date": "2026-10-15",
            "served": {"firm": "cottonwood", "business_date": "2026-10-08"},
            "refusals": {"first_refused_candidate_date": "2026-10-09", "refused_dates": ["2026-10-09", "2026-10-12", "2026-10-13", "2026-10-14"], "refusal_records_read": 3,
                         "condition": "account_lost", "lost_count": 1},
            "lost_account": {"present_in_served": True, "absent_in_candidates": True, "claim": "measured",
                             "source_partition_checks": [{"date": "2026-10-08", "listed_in_source": True}, {"date": "2026-10-09", "listed_in_source": False}],
                             "directory_mark": {"found": True, "class": "closed", "note": "the directory marks the account closed from 2026-10-09; class only"}},
            "cause": {"class": "terminated_or_closed_account", "claim": "measured",
                      "statement": "The account is marked closed in the directory from the first refused date and the custodian source no longer lists it, so the candidate loses it.",
                      "evidence": ["directory mark found with class closed from 2026-10-09", "source partition for 2026-10-09 does not list the account, 2026-10-08 does"]},
            "self_clears": {"claim": "inferred", "statement": "The refusal does not clear on its own: the account stays absent from the source on every later date."},
            "acceptance_path": {"guard": {"file": PUB, "line": 10, "identifier": "account_lost"},
                                "override_mechanisms": [{"name": "bypass_one_date", "file": PUB, "line": 20, "identifier": "bypass_one_date"},
                                                        {"name": "closed-account exclusion", "file": PUB, "line": 30, "identifier": "_closed_accounts"}],
                                "owner": "the holdings publisher owner (the CTO decides)", "recommended_path": "mark the account closed in the directory so the guard excludes it, then publish"},
            "other_firms": {"49financial": {"refusal_record_present": False, "served_business_date": "2026-10-14"},
                            "inflection": {"refusal_record_present": False, "served_business_date": "2026-10-14"}},
            "notes": ["read 3 refusal records and 2 source partition listings, counts only", "no account id is recorded; class only", "not read: the custodian's own system"],
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
    ("AC1", "wrong_firm", lambda r: sp(r, ["served", "firm"], "inflection")),
    ("AC1", "refused_date_not_trading", lambda r: sp(r, ["refusals", "refused_dates"], ["2026-10-10", "2026-10-12"])),
    ("AC1", "refused_before_served", lambda r: sp(r, ["refusals", "refused_dates"], ["2026-10-07", "2026-10-09"])),
    ("AC1", "first_date_mismatch", lambda r: sp(r, ["refusals", "first_refused_candidate_date"], "2026-10-12")),
    ("AC1", "second_condition", lambda r: sp(r, ["refusals", "condition"], "source_frontier_older")),
    ("AC1", "lost_count_two", lambda r: sp(r, ["refusals", "lost_count"], 2)),
    ("AC1", "one_source_check", lambda r: sp(r, ["lost_account", "source_partition_checks"], [{"date": "2026-10-09", "listed_in_source": False}])),
    ("AC1", "not_present_in_served", lambda r: sp(r, ["lost_account", "present_in_served"], False)),
    ("AC2", "cause_class_unknown", lambda r: sp(r, ["cause", "class"], "bad luck")),
    ("AC2", "one_evidence_line", lambda r: sp(r, ["cause", "evidence"], ["only one line of evidence that is long enough"])),
    ("AC2", "guard_line_wrong", lambda r: sp(r, ["acceptance_path", "guard", "line"], 3)),
    ("AC2", "guard_file_missing", lambda r: sp(r, ["acceptance_path", "guard", "file"], "data/none.py")),
    ("AC2", "no_override_mechanism", lambda r: sp(r, ["acceptance_path", "override_mechanisms"], [])),
    ("AC2", "override_identifier_absent", lambda r: sp(r, ["acceptance_path", "override_mechanisms", 0, "identifier"], "no_such_name")),
    ("AC2", "other_firm_missing", lambda r: r["other_firms"].pop("inflection")),
    ("AC2", "self_clears_no_claim", lambda r: sp(r, ["self_clears", "claim"], "maybe")),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["vendor_requests_sent"], 1)),
    ("AC3", "long_digit_run", lambda r: sp(r, ["notes"], ["an account id 123456789012 leaked into this long enough line", "second line that is long enough to count here", "third line that is long enough to count here"])),
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
    expect("clean", "IB209-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB209-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
