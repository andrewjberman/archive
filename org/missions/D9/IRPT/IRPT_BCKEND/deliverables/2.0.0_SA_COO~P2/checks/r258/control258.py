"""Positive control and negatives for p258_cells.py (run by the issuer at the cut). Usage: python control258.py <real_repo_root>

Synthetic git repositories: a base commit holding a small source file to cite, then ONE worker commit holding the findings.
"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r258/p258_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p258_cells as P  # noqa: E402

SRC_REL = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
SRC = "\n".join("line %d of the source" % i for i in range(1, 41)) + "\n"


def h(n):
    return hashlib.sha256(("line %d of the source" % n).encode("utf-8")).hexdigest()


def acct(i, role, pos_c=0, pos_p=0, bal_c=0, bal_p=0, closed=False):
    return {"hashed_id": "%012x" % (0xabc000 + i), "role": role, "closed_marker": closed,
            "source_rows": {"positions": {"candidate": pos_c, "prior": pos_p}, "balance": {"candidate": bal_c, "prior": bal_p}}}


GOOD = {
    "firm": "49financial", "candidate_day": "2026-10-16", "prior_day": "2026-10-15",
    "accounts": [acct(1, "gone_not_exempt", pos_c=3, pos_p=3), acct(2, "exempt_listed"), acct(3, "exempt_listed")],
    "partitions": [
        {"table": "positions", "day": "candidate", "account_count": 7690, "prior_account_count": 7700, "percent_of_prior": 7690 * 100 // 7700},
        {"table": "positions", "day": "prior", "account_count": 7700, "prior_account_count": 7700, "percent_of_prior": 100},
        {"table": "balance", "day": "candidate", "account_count": 7690, "prior_account_count": 7700, "percent_of_prior": 7690 * 100 // 7700},
        {"table": "balance", "day": "prior", "account_count": 7700, "prior_account_count": 7700, "percent_of_prior": 100},
    ],
    "lost_count_per_fire": [{"fire_date": "2026-10-14", "account_lost_count": 3, "listed_absent_at_source": 0}, {"fire_date": "2026-10-15", "account_lost_count": 1, "listed_absent_at_source": 2},
                            {"fire_date": "2026-10-16", "account_lost_count": 1, "listed_absent_at_source": 2}, {"fire_date": "2026-10-19", "account_lost_count": 1, "listed_absent_at_source": 2}],
    "decision_line": {"file": SRC_REL, "line": 12, "excerpt_sha256": h(12), "what": "The exemption test refuses an account with positions in a source table."},
    "why_not_exempt": "HAS_POSITIONS_IN_A_SOURCE_TABLE", "verdict": "BUILD_FAULT_ACCOUNT_HAS_SOURCE_POSITIONS",
    "evidence_for_verdict": "The account holds positions in both tables on both days, so it should be in the candidate.",
    "reads": {"aws_writes": 0, "s3_puts": 0},
}


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def mut(fn):
    def f(d):
        d = copy.deepcopy(d)
        fn(d)
        return d
    return f


def build(findings=GOOD, note="the notes carry only hashed ids and counts\n", extra=None, drop_findings=False):
    root = Path(tempfile.mkdtemp(prefix="c258_"))
    (root / SRC_REL).parent.mkdir(parents=True)
    (root / SRC_REL).write_text(SRC, encoding="utf-8")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    d = root / P.DELIVD
    d.mkdir(parents=True)
    if not drop_findings:
        (d / "IBhx1_findings.json").write_text(json.dumps(findings), encoding="utf-8")
    (d / "IBhx1_notes.md").write_text(note, encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "worker")
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


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHX1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

AC1 = [
    ("wrong_firm", mut(lambda d: d.update(firm="inflection"))),
    ("wrong_candidate_day", mut(lambda d: d.update(candidate_day="2026-10-15"))),
    ("two_accounts_only", mut(lambda d: d.update(accounts=d["accounts"][:2]))),
    ("two_gone_not_exempt", mut(lambda d: d["accounts"][1].update(role="gone_not_exempt"))),
    ("duplicate_hashed_ids", mut(lambda d: d["accounts"][1].update(hashed_id=d["accounts"][0]["hashed_id"]))),
    ("hashed_id_not_12_hex", mut(lambda d: d["accounts"][0].update(hashed_id="acc_1234567890"))),
    ("negative_row_count", mut(lambda d: d["accounts"][0]["source_rows"]["positions"].update(candidate=-1))),
    ("missing_balance_rows", mut(lambda d: d["accounts"][0]["source_rows"].pop("balance"))),
    ("closed_marker_not_bool", mut(lambda d: d["accounts"][0].update(closed_marker="no"))),
    ("three_partitions", mut(lambda d: d.update(partitions=d["partitions"][:3]))),
    ("duplicate_partition", mut(lambda d: d["partitions"][1].update(table="positions", day="candidate"))),
    ("percent_inconsistent", mut(lambda d: d["partitions"][0].update(percent_of_prior=98))),
    ("prior_count_zero", mut(lambda d: d["partitions"][1].update(prior_account_count=0))),
    ("lost_count_per_fire_missing", mut(lambda d: d.pop("lost_count_per_fire"))),
    ("lost_count_per_fire_three", mut(lambda d: d.update(lost_count_per_fire=d["lost_count_per_fire"][:3]))),
    ("lost_count_wrong_dates", mut(lambda d: d["lost_count_per_fire"][0].update(fire_date="2026-10-13"))),
    ("lost_count_negative", mut(lambda d: d["lost_count_per_fire"][1].update(account_lost_count=-1))),
    ("wrong_excerpt_hash", mut(lambda d: d["decision_line"].update(excerpt_sha256=h(13)))),
    ("line_out_of_range", mut(lambda d: d["decision_line"].update(line=999))),
    ("cited_file_absent", mut(lambda d: d["decision_line"].update(file="data/nope.py"))),
    ("reason_invalid", mut(lambda d: d.update(why_not_exempt="BAD_LUCK"))),
    ("verdict_invalid", mut(lambda d: d.update(verdict="MAYBE"))),
    ("aws_write_made", mut(lambda d: d["reads"].update(aws_writes=1))),
]
for label, fn in AC1:
    root = build(findings=fn(GOOD))
    expect(label, "IBHX1-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)

AC2 = [
    ("cli_id_in_notes", "found cli_2dce3a062b865d59bb9ed552 seen\n"),
    ("acc_id_in_notes", "account acc_0123456789abcdef01234567 seen\n"),
    ("long_digit_run", "account 123456789012 seen\n"),
    ("email_in_notes", "contact someone@example.com\n"),
    ("odd_hex_run_40", "commit " + "a" * 40 + " seen\n"),
]
for label, note in AC2:
    root = build(note=note)
    expect(label, "IBHX1-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(note="a full sha256: " + "b" * 64 + " and a ten-hex commit abcdef0123\n")
expect("full_sha256_and_short_commit_ok", "IBHX1-AC2", root, True)
shutil.rmtree(root, ignore_errors=True)

for label, kw in (("file_outside_paths", dict(extra=["lib/other.py"])), ("write_under_data", dict(extra=["data/x.parquet"])), ("findings_not_in_commit", dict(drop_findings=True))):
    root = build(**kw)
    expect(label, "IBHX1-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c258_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBHX1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
