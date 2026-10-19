"""Positive control and negatives for p259_cells.py (run by the issuer at the cut). Usage: python control259.py <real_repo_root>

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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r259/p259_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p259_cells as P  # noqa: E402

SRC_REL = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
SRC = "\n".join("line %d of the source" % i for i in range(1, 61)) + "\n"


def h(n):
    return hashlib.sha256(("line %d of the source" % n).encode("utf-8")).hexdigest()


def reader(i, kind, line, keyed="client_id", effect="KEY_CHANGES_ENTRY_REMAINS"):
    return {"id": "R%02d" % i, "kind": kind, "file": SRC_REL, "line": line, "excerpt_sha256": h(line), "keyed_on": keyed,
            "rekey_effect": effect, "what": "This reader keys on the directory client key and so sees a new key."}


GOOD = {
    "firm": "cottonwood",
    "readers": [reader(1, "REFRESH_COMPARE", 10), reader(2, "HMAC_LIST", 20, "account_ids", "NONE"), reader(3, "RUNNER", 30, "entry_key"),
                reader(4, "PAGE", 40, "client_id", "UNKNOWN")],
    "census": {"terms": ["client_id", "entry_key", "relationship_id", "ids.client_id"], "files_scanned": 900, "files_with_hits": 12},
    "release_path": {"file": SRC_REL, "line": 50, "excerpt_sha256": h(50), "what": "The runner is read from the repository path on the build host."},
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


def build(findings=GOOD, note="the notes carry no identifier\n", extra=None, drop_findings=False):
    root = Path(tempfile.mkdtemp(prefix="c259_"))
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
        (d / "IBcw3_findings.json").write_text(json.dumps(findings), encoding="utf-8")
    (d / "IBcw3_notes.md").write_text(note, encoding="utf-8")
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
    expect("clean", "IBCW3-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

AC1 = [
    ("wrong_firm", mut(lambda d: d.update(firm="inflection"))),
    ("three_readers", mut(lambda d: d.update(readers=d["readers"][:3]))),
    ("duplicate_reader_ids", mut(lambda d: d["readers"][1].update(id="R01"))),
    ("reader_id_form", mut(lambda d: d["readers"][1].update(id="reader2"))),
    ("kind_invalid", mut(lambda d: d["readers"][3].update(kind="DASHBOARD"))),
    ("no_refresh_compare", mut(lambda d: d["readers"][0].update(kind="PAGE"))),
    ("no_hmac_list", mut(lambda d: d["readers"][1].update(kind="PAGE"))),
    ("no_runner", mut(lambda d: d["readers"][2].update(kind="PAGE"))),
    ("keyed_on_invalid", mut(lambda d: d["readers"][0].update(keyed_on="guess"))),
    ("rekey_effect_invalid", mut(lambda d: d["readers"][0].update(rekey_effect="FINE"))),
    ("wrong_excerpt_hash", mut(lambda d: d["readers"][0].update(excerpt_sha256=h(11)))),
    ("line_out_of_range", mut(lambda d: d["readers"][0].update(line=999))),
    ("cited_file_absent", mut(lambda d: d["readers"][0].update(file="data/nope.py"))),
    ("what_too_short", mut(lambda d: d["readers"][0].update(what="short"))),
    ("census_term_missing", mut(lambda d: d["census"].update(terms=["client_id", "entry_key"]))),
    ("census_no_files", mut(lambda d: d["census"].update(files_scanned=0))),
    ("census_hits_exceed_scanned", mut(lambda d: d["census"].update(files_with_hits=901))),
    ("census_hits_below_cited_files", mut(lambda d: d["census"].update(files_with_hits=0))),
    ("census_missing", mut(lambda d: d.pop("census"))),
    ("release_path_missing", mut(lambda d: d.pop("release_path"))),
    ("release_path_wrong_hash", mut(lambda d: d["release_path"].update(excerpt_sha256=h(51)))),
    ("aws_write_made", mut(lambda d: d["reads"].update(aws_writes=1))),
]
for label, fn in AC1:
    root = build(findings=fn(GOOD))
    expect(label, "IBCW3-AC1", root, False)
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
    expect(label, "IBCW3-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(note="a full sha256: " + "b" * 64 + " and a ten-hex commit abcdef0123\n")
expect("full_sha256_and_short_commit_ok", "IBCW3-AC2", root, True)
shutil.rmtree(root, ignore_errors=True)

for label, kw in (("file_outside_paths", dict(extra=["lib/other.py"])), ("write_under_data", dict(extra=["data/x.parquet"])), ("findings_not_in_commit", dict(drop_findings=True))):
    root = build(**kw)
    expect(label, "IBCW3-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c259_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBCW3-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
