"""Positive control and negatives for p201_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control201.py <real_repo_root>
Builds temp git roots with stub files at the real relative paths (a base commit, a worker commit by the cell's worker serial), runs every criterion
expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r201/p201_cells.py"
for sub in ("r196", "r200", "r201"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p201_cells as P  # noqa: E402

P6 = P.P6
LAM = P.LAMBDA


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt if isinstance(txt, str) else json.dumps(txt), encoding="utf-8")


def commit(root, msg, author=None):
    git(root, "add", "-A")
    git(root, *(["commit", "-qm", msg] + (["--author", "%s <w@x>" % author] if author else [])))
    return git(root, "rev-parse", "HEAD")


def schema(rev, with_kind):
    return {"title": "ExportBundle", "x-contract-revision": rev, "kinds": ["retained", "series"] + (["filled_report"] if with_kind else [])}


# ------------------------------------------------------------------ cell 1: the contract
def build1(variant=None):
    c = P.CELLS["1"]
    root = Path(tempfile.mkdtemp(prefix="c201a_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in c["regress"]:
        wt(root, rel, "def test_ok():\n    assert True\n")
    wt(root, P.DOCS_SCHEMA, schema("1.1", False))
    wt(root, P.PKG_SCHEMA, schema("1.1", False))
    base = commit(root, "base")
    rev = "1.3" if variant == "big_step" else "1.2"
    new = schema(rev, variant != "no_kind")
    wt(root, P.DOCS_SCHEMA, new)
    wt(root, P.PKG_SCHEMA, schema("1.9", True) if variant == "copies_differ" else new)
    tests = ("import json, pathlib\n"
             "DOCS = pathlib.Path(r'%s')\n"
             "def _kinds():\n    return json.loads(DOCS.read_text(encoding='utf-8'))['kinds']\n" % (root / P.DOCS_SCHEMA))
    tests += "".join("def test_new_%d():\n    assert 'filled_report' in _kinds()\n" % i for i in range(3))
    tests += "".join("def test_old_%d():\n    assert 'retained' in _kinds() and 'series' in _kinds()\n" % i for i in range(3))
    if variant == "weak_tests":
        tests = "".join("def test_w%d():\n    assert True\n" % i for i in range(6))
    if variant == "few_tests":
        tests = tests.split("def test_new_1")[0]
    wt(root, c["test"], tests)
    changed = [P.DOCS_SCHEMA, P.PKG_SCHEMA, c["test"]]
    if variant == "stray":
        wt(root, "docs/other.md", "x")
        changed.append("docs/other.md")
    rec = {"base_commit": base, "changed_paths": sorted(changed), "arms_tested": ["new_bundle_validates", "old_bundle_validates_unchanged"],
           "tests_total": 6, "tests_passed": 6, "mutant_tests_failed": 3, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    if variant == "one_arm":
        rec["arms_tested"] = ["new_bundle_validates"]
    wt(root, P.rec_path(c), rec)
    commit(root, "work", "0.9.0_WK_IRPT_BCKEND~%d" % c["slot"])
    return root


# ------------------------------------------------------------------ cell 2: the shared reader
def block(fn):
    return "def %s(x):\n    # BEGIN FILLED-REPORT-D\n    x = x * 2\n    # END FILLED-REPORT-D\n    return x\n" % fn


def build2(variant=None):
    c = P.CELLS["2"]
    root = Path(tempfile.mkdtemp(prefix="c201b_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in c["regress"]:
        wt(root, rel, "def test_ok():\n    assert True\n")
    entry = LAM + "reporting/entry.py"
    freeze = LAM + "export/retained_export.py"
    wt(root, entry, "def _filled_named_accounts(doc):\n    return []\n\ndef _by_row_keys(n):\n    return []\n")
    wt(root, freeze, "def freeze(x):\n    return x\n")
    wt(root, LAM + "export/bundle.py", "def b():\n    return 1\n")
    base = commit(root, "base")
    wt(root, P.SHARED, block("filled_named_accounts") if variant != "no_block" else "def filled_named_accounts(x):\n    return x * 2\n")
    if variant == "inline_stays":
        wt(root, entry, "import filled_named_accounts as _fna\n\ndef _filled_named_accounts(doc):\n    return []\n")
    elif variant == "no_entry_import":
        wt(root, entry, "def other():\n    return 1\n")
    else:
        wt(root, entry, "import filled_named_accounts as _fna\n\ndef use(doc):\n    return _fna.filled_named_accounts(doc)\n")
    fz = "import filled_named_accounts as _fna\n\ndef freeze(x):\n    return x\n" if variant != "no_freeze_import" else "def freeze(x):\n    return x\n"
    fz += "\n" + block("freeze_scope")
    wt(root, freeze, fz)
    if variant == "second_def":
        wt(root, LAM + "export/bundle.py", "def filled_named_accounts(x):\n    return x\n")
    test = ("import importlib.util\n"
            "spec = importlib.util.spec_from_file_location('m_shared', r'%s')\n"
            "m = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(m)\n" % (root / P.SHARED))
    test += "".join("def test_case_%d():\n    assert m.filled_named_accounts(%d) == %d\n" % (i, i, 2 * i) for i in range(5))
    test += "def test_export_freeze_refuses_uncovered_account():\n    assert m.filled_named_accounts(1) == 2\n"
    if variant == "no_neg_name":
        test = test.replace("export_freeze_refuses_uncovered_account", "something_else")
    if variant == "weak_tests":
        test = "".join("def test_w%d():\n    assert True\n" % i for i in range(7))
    wt(root, c["test"], test)
    changed = [P.SHARED, entry, freeze, c["test"]] + ([LAM + "export/bundle.py"] if variant == "second_def" else [])
    if variant == "stray":
        wt(root, "docs/other.md", "x")
        changed.append("docs/other.md")
    rec = {"base_commit": base, "changed_paths": sorted(changed), "negative_tests": ["export_freeze_refuses_uncovered_account"],
           "tests_total": 7, "tests_passed": 7, "mutant_tests_failed": 4, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    wt(root, P.rec_path(c), rec)
    commit(root, "work", "0.9.0_WK_IRPT_BCKEND~%d" % c["slot"])
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=200, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-40s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


for cell, builder, negs in (("1", build1, [("few_tests", "AC1"), ("weak_tests", "AC2"), ("stray", "AC3"), ("copies_differ", "AC3"), ("big_step", "AC3"), ("no_kind", "AC3"), ("one_arm", "AC3")]),
                            ("2", build2, [("few_tests_dummy", None), ("no_block", "AC2"), ("weak_tests", "AC2"), ("stray", "AC3"), ("inline_stays", "AC3"), ("no_entry_import", "AC3"),
                                           ("no_freeze_import", "AC3"), ("second_def", "AC3"), ("no_neg_name", "AC3")])):
    root = builder()
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "IB201-%s-%s" % (cell, ac), root, True)
    shutil.rmtree(root, ignore_errors=True)
    for variant, ac in negs:
        if ac is None:
            continue
        root = builder(variant)
        expect(variant, "IB201-%s-%s" % (cell, ac), root, False)
        shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
