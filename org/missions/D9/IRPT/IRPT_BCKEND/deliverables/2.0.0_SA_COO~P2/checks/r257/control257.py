"""Positive control and negatives for p257_cells.py (run by the issuer at the cut). Usage: python control257.py <real_repo_root>

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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r257/p257_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p257_cells as P  # noqa: E402

SRC_REL = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
SRC = "\n".join("line %d of the source" % i for i in range(1, 41)) + "\n"


def h(n):
    return hashlib.sha256(("line %d of the source" % n).encode("utf-8")).hexdigest()


GOOD = {
    "firm": "cottonwood", "as_of": "2026-10-14", "dropped_count": 6,
    "dropped_hashed_ids": ["%012x" % (0xabc000 + i) for i in range(6)],
    "stage": {"file": SRC_REL, "line": 12, "excerpt_sha256": h(12), "what": "The advisor join drops a client with no advisor mapping."},
    "parked_link": {"checked_first": True, "what": "The account-to-advisor map is parked and the build does not read it.", "used_by_build": False},
    "shared": {"attributes": [{"name": "no advisor mapping", "dropped_with": 6, "dropped_total": 6, "retained_with": 0, "retained_total": 200}]},
    "verdict": "BUILD_FAULT", "evidence_for_verdict": "All six lack the mapping and none of the retained clients do.",
    "reads": {"aws_writes": 0, "s3_puts": 0, "raw_ids_in_artifacts": 0},
}


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def mut(**kv):
    def f(d):
        d = copy.deepcopy(d)
        for k, v in kv.items():
            cur = d
            ks = k.split(".")
            for p in ks[:-1]:
                cur = cur[p]
            if v is KeyError:
                del cur[ks[-1]]
            else:
                cur[ks[-1]] = v
        return d
    return f


def build(findings=GOOD, note="the notes carry only hashed ids and counts\n", extra=None, drop_findings=False):
    root = Path(tempfile.mkdtemp(prefix="c257_"))
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
        (d / "IBcw1_findings.json").write_text(json.dumps(findings), encoding="utf-8")
    (d / "IBcw1_notes.md").write_text(note, encoding="utf-8")
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
    print("%s %-12s %-32s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBCW1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

USED = mut(**{"parked_link.used_by_build": True, "parked_link.file": SRC_REL, "parked_link.line": 7, "parked_link.excerpt_sha256": h(7)})
root = build(findings=USED(GOOD))
expect("parked_link_used_with_cite", "IBCW1-AC1", root, True)
shutil.rmtree(root, ignore_errors=True)

AC1 = [
    ("missing_verdict", mut(verdict=KeyError)),
    ("wrong_firm", mut(firm="inflection")),
    ("dropped_count_five", mut(dropped_count=5)),
    ("duplicate_ids", mut(dropped_hashed_ids=["abcdef012345"] * 6)),
    ("id_not_12_hex", mut(**{"dropped_hashed_ids": ["cli_2dce3a062b86"] + ["%012x" % i for i in range(5)]})),
    ("wrong_excerpt_hash", mut(**{"stage.excerpt_sha256": h(13)})),
    ("line_out_of_range", mut(**{"stage.line": 999})),
    ("cited_file_absent", mut(**{"stage.file": "data/nope.py"})),
    ("stage_what_empty", mut(**{"stage.what": "short"})),
    ("parked_not_checked_first", mut(**{"parked_link.checked_first": False})),
    ("parked_used_without_cite", mut(**{"parked_link.used_by_build": True})),
    ("shared_empty", mut(**{"shared.attributes": []})),
    ("shared_counts_inconsistent", mut(**{"shared.attributes": [{"name": "x", "dropped_with": 3, "dropped_total": 6, "retained_with": 9, "retained_total": 4}]})),
    ("shared_dropped_total_not_six", mut(**{"shared.attributes": [{"name": "x", "dropped_with": 3, "dropped_total": 5, "retained_with": 1, "retained_total": 4}]})),
    ("verdict_invalid", mut(verdict="MAYBE")),
    ("aws_write_made", mut(**{"reads.aws_writes": 1})),
    ("s3_put_made", mut(**{"reads.s3_puts": 1})),
]
for label, fn in AC1:
    root = build(findings=fn(GOOD))
    expect(label, "IBCW1-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)

AC2 = [
    ("cli_id_in_notes", "found cli_2dce3a062b865d59bb9ed552 missing\n"),
    ("acc_id_in_notes", "account acc_0123456789abcdef01234567 seen\n"),
    ("long_digit_run", "account 123456789012 seen\n"),
    ("email_in_notes", "contact someone@example.com\n"),
    ("odd_hex_run_40", "commit " + "a" * 40 + " seen\n"),
]
for label, note in AC2:
    root = build(note=note)
    expect(label, "IBCW1-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(note="a full sha256 of a line: " + "b" * 64 + " and a ten-hex commit abcdef0123\n")
expect("full_sha256_and_short_commit_ok", "IBCW1-AC2", root, True)
shutil.rmtree(root, ignore_errors=True)

for label, kw in (("file_outside_paths", dict(extra=["lib/other.py"])), ("write_under_data", dict(extra=["data/x.parquet"])), ("findings_not_in_commit", dict(drop_findings=True))):
    root = build(**kw)
    expect(label, "IBCW1-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c257_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBCW1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
