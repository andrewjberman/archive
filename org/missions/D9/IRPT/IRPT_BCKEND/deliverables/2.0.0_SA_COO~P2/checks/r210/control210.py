"""Positive control and negatives for p210_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control210.py <real_repo_root>
Builds a temp tree holding the real lib/trading_calendar.py and a stub publisher file with the guard, screen and validator identifiers, writes clean synthetic records,
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r210/p210_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p210_cells as P  # noqa: E402

PUB = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"


def build():
    root = Path(tempfile.mkdtemp(prefix="c210_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / PUB).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# stub"] * 60
    lines[9] = '    add("count_regression", old - new)'
    lines[19] = "    closed = closed_accounts() & gone"
    lines[29] = "def cot_screen_accounts(rows):"
    lines[39] = "def validate_cot_actual_positions(rows):"
    lines[44] = '        raise CotRefused("negative_quantity")'
    (root / PUB).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def site(line, ident):
    return {"file": PUB, "line": line, "identifier": ident}


def rec1():
    return {"base_commit": "a" * 40, "read_date": "2026-10-15",
            "served": {"firm": "49financial", "business_date": "2026-10-12", "t_minus_1": "2026-10-14", "trading_days_behind": 2},
            "refusals": {"refused_dates": ["2026-10-13", "2026-10-14"], "refusal_records_read": 2,
                         "per_candidate": [{"candidate_date": "2026-10-13", "conditions": [{"condition": "count_regression", "count": 3}]},
                                           {"candidate_date": "2026-10-14", "conditions": [{"condition": "count_regression", "count": 3}]}]},
            "guard_site": site(10, "count_regression"),
            "account_or_field": {"claim": "measured", "class": "a position-count field", "statement": "Three accounts report fewer positions than the served snapshot; the class is the position count, ids are private."},
            "cause": {"claim": "inferred", "statement": "The candidate loses positions on three accounts compared with the served snapshot, which the guard counts as a regression.",
                      "evidence": ["the refusal records name count_regression three on both candidates", "the guard line raises count_regression when positions fall"]},
            "acceptance_path": {"mechanisms": [site(20, "closed_accounts")], "recommended_path": "the owner decides on the three accounts; a custodian-confirmed closure excludes them"},
            "other_firms": {"cottonwood": {"served_business_date": "2026-10-08"}, "inflection": {"served_business_date": "2026-10-13"}},
            "notes": ["read 2 refusal records, counts and condition names only", "no account id is recorded; class only", "not read: the custodian's own system"],
            **{k: 0 for k in P.P6.BOUND}}


def rec2():
    return {"base_commit": "a" * 40, "read_date": "2026-10-15",
            "validator_site": site(40, "validate_cot_actual_positions"), "screen_site": site(30, "cot_screen_accounts"),
            "source_rows": {"count": 12, "distinct_dates": 3},
            "offline_run": {"performed": True, "read_only": True, "writes": 0, "published": False, "invocation": "python offline_validate.py --rows scratch/rows.json (no account id in the command)", "outcome": "refused"},
            "failing_condition": {"name": "negative_quantity", "claim": "measured", "site": site(45, "negative_quantity"),
                                  "explanation": "The validator refuses an account when any position quantity is negative, which a short or an adjustment row produces."},
            "fix_options": [{"option": "correct the screen to admit signed adjustment rows", "site": site(45, "negative_quantity"), "effect": "the account passes the screen and is no longer lost"},
                            {"option": "a custodian-confirmed TERMINATED mark in the directory", "site": site(20, "closed_accounts"), "effect": "the guard lists the account as closed and not refused"}],
            "ids_private": True,
            "notes": ["ran the validator offline on 12 source rows, counts only", "no account id is recorded; class only", "not read: the custodian's own system"],
            **{k: 0 for k in P.P6.BOUND}}


def write(root, rel, rec):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def sp(d, path, v):
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = v


M1 = [
    ("AC1", "wrong_firm", lambda r: sp(r, ["served", "firm"], "cottonwood")),
    ("AC1", "behind_count_wrong", lambda r: sp(r, ["served", "trading_days_behind"], 4)),
    ("AC1", "t_minus_1_wrong", lambda r: sp(r, ["served", "t_minus_1"], "2026-10-13")),
    ("AC1", "refused_before_served", lambda r: sp(r, ["refusals", "refused_dates"], ["2026-10-09", "2026-10-13"])),
    ("AC1", "per_candidate_short", lambda r: r["refusals"]["per_candidate"].pop()),
    ("AC1", "condition_row_bad", lambda r: sp(r, ["refusals", "per_candidate", 0, "conditions"], [{"condition": "", "count": "x"}])),
    ("AC1", "guard_line_wrong", lambda r: sp(r, ["guard_site", "line"], 3)),
    ("AC2", "claim_missing", lambda r: sp(r, ["account_or_field", "claim"], "maybe")),
    ("AC2", "one_evidence_line", lambda r: sp(r, ["cause", "evidence"], ["only one line of evidence that is long enough"])),
    ("AC2", "no_mechanism", lambda r: sp(r, ["acceptance_path", "mechanisms"], [])),
    ("AC2", "other_firm_missing", lambda r: r["other_firms"].pop("inflection")),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["vendor_requests_sent"], 1)),
    ("AC3", "long_digit_run", lambda r: sp(r, ["notes"], ["an id 123456789012 leaked into this long enough line", "second line that is long enough to count here", "third line that is long enough to count here"])),
]
M2 = [
    ("AC1", "validator_line_wrong", lambda r: sp(r, ["validator_site", "line"], 3)),
    ("AC1", "screen_identifier_wrong", lambda r: sp(r, ["screen_site", "identifier"], "something_else")),
    ("AC1", "no_source_rows", lambda r: sp(r, ["source_rows", "count"], 0)),
    ("AC1", "run_wrote", lambda r: sp(r, ["offline_run", "writes"], 1)),
    ("AC1", "run_not_performed", lambda r: sp(r, ["offline_run", "performed"], False)),
    ("AC2", "accepted_without_a_run", lambda r: (sp(r, ["offline_run", "performed"], False), sp(r, ["offline_run", "outcome"], "accepted"), sp(r, ["failing_condition"], {"name": "", "claim": "inferred", "statement": "x" * 70, "explanation": "y" * 70}))),
    ("AC1", "run_published", lambda r: sp(r, ["offline_run", "published"], True)),
    ("AC2", "refused_but_inferred", lambda r: sp(r, ["failing_condition", "claim"], "inferred")),
    ("AC2", "condition_line_wrong", lambda r: sp(r, ["failing_condition", "site", "line"], 3)),
    ("AC2", "one_fix_option", lambda r: r["fix_options"].pop()),
    ("AC2", "ids_not_private", lambda r: sp(r, ["ids_private"], False)),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["aws_writes_made"], 1)),
]
bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-26s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for cell, rel, rec, muts in (("1", P.REC1, rec1(), M1), ("2", P.REC2, rec2(), M2)):
    write(root, rel, rec)
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "IB210-%s-%s" % (cell, ac), root, True)
    for ac, name, fn in muts:
        r = copy.deepcopy(rec)
        fn(r)
        write(root, rel, r)
        expect(name, "IB210-%s-%s" % (cell, ac), root, False)
    write(root, rel, rec)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
