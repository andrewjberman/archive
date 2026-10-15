"""Positive control and negatives for p204_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control204.py <real_repo_root>
Builds temp git roots with stub files at the real relative paths (a base commit, a worker commit by the cell's worker serial), runs every criterion
expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r204/p204_cells.py"
for sub in ("r196", "r200", "r201", "r204"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p204_cells as P  # noqa: E402

P6 = P.P6
LAM = P.LAMBDA
SHARED_BODY = "def filled_named_accounts(x):\n    return x\n"


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt if isinstance(txt, str) else json.dumps(txt, indent=1), encoding="utf-8")


def commit(root, msg, author=None):
    git(root, "add", "-A")
    git(root, *(["commit", "-qm", msg] + (["--author", "%s <w@x>" % author] if author else [])))
    return git(root, "rev-parse", "HEAD")


def new_root(prefix):
    root = Path(tempfile.mkdtemp(prefix=prefix))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    return root


# ------------------------------------------------------------------ cell 1: the source map
def fn_entry(with_shared, pin=None, sha=None, files_ok=True):
    e = {"source_dir": "x", "files": ["entry.py"] + (["filled_named_accounts.py"] if with_shared and files_ok else []),
         "staged_from": [{"repo_path": LAM + "reporting/entry.py", "pin": "a" * 40, "packaged_as": "entry.py", "sha256": "b" * 64}]}
    if with_shared:
        e["staged_from"].append({"repo_path": P.SHARED, "pin": pin, "packaged_as": "filled_named_accounts.py", "sha256": sha})
    return e


def build1(variant=None):
    c = P.CELLS["1"]
    root = new_root("c204a_")
    wt(root, P.SHARED, SHARED_BODY)
    wt(root, P.MAP, {"functions": {"fn-a": fn_entry(False), "fn-b": {"source_dir": "y", "files": ["z.py"]}, "fn-c": fn_entry(False)}})
    base = commit(root, "base")
    sha = hashlib.sha256(SHARED_BODY.encode("utf-8")).hexdigest()
    pin = base
    funcs = {"fn-a": fn_entry(True, pin, sha), "fn-b": {"source_dir": "y", "files": ["z.py"]}, "fn-c": fn_entry(True, pin, sha)}
    if variant == "missing_entry":
        funcs["fn-c"] = fn_entry(False)
    if variant == "wrong_sha":
        funcs["fn-a"] = fn_entry(True, pin, "e" * 64)
    if variant == "bad_pin":
        funcs["fn-a"] = fn_entry(True, "f" * 40, sha)
    if variant == "files_missing":
        funcs["fn-a"] = fn_entry(True, pin, sha, files_ok=False)
    wt(root, P.MAP, {"functions": funcs})
    test = ("import json, pathlib\n"
            "MAP = pathlib.Path(r'%s')\n"
            "def _m():\n    return json.loads(MAP.read_text(encoding='utf-8'))['functions']\n" % (root / P.MAP))
    test += "".join("def test_has_entry_%d():\n    f = _m()\n    assert 'filled_named_accounts.py' in json.dumps(f['fn-a']) and 'filled_named_accounts.py' in json.dumps(f['fn-c'])\n" % i for i in range(4))
    if variant == "weak_tests":
        test = "".join("def test_w%d():\n    assert True\n" % i for i in range(4))
    if variant == "few_tests":
        test = test.split("def test_has_entry_1")[0]
    wt(root, c["test"], test)
    changed = [P.MAP, c["test"]]
    if variant == "stray":
        wt(root, "docs/other.md", "x")
        changed.append("docs/other.md")
    imports = [{"function": "fn-a", "result": "PASS"}, {"function": "fn-c", "result": "PASS"}]
    if variant == "build_only_fail":
        imports[1]["result"] = "FAIL"
    if variant == "build_only_short":
        imports = imports[:1]
    rec = {"base_commit": base, "changed_paths": sorted(changed), "build_only_imports": imports, "tests_total": 4, "tests_passed": 4, "mutant_tests_failed": 4,
           "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    wt(root, P.rec_path(c), rec)
    commit(root, "work", "0.9.0_WK_IRPT_BCKEND~%d" % c["slot"])
    return root


# ------------------------------------------------------------------ cell 2: the server-side pin
def block(fn):
    return "def %s(x):\n    # BEGIN FILLED-REPORT-E\n    x = x * 2\n    # END FILLED-REPORT-E\n    return x\n" % fn


def build2(variant=None):
    c = P.CELLS["2"]
    root = new_root("c204b_")
    for rel in c["regress"]:
        wt(root, rel, "def test_ok():\n    assert True\n")
    wt(root, LAM + "export/retained_export.py", "def other():\n    return 1\n")
    wt(root, LAM + "export/entry.py", "def other():\n    return 1\n")
    base = commit(root, "base")
    if variant == "no_block":
        wt(root, LAM + "export/retained_export.py", "def other():\n    return 1\n\ndef freeze_pin(x):\n    return x * 2\n")
    elif variant == "import_error":
        wt(root, LAM + "export/retained_export.py", "def other():\n    return 1\n\n# BEGIN FILLED-REPORT-E\nHELPER = 3\n# END FILLED-REPORT-E\nVALUE = HELPER\n\ndef freeze_pin(x):\n    return x * 2\n")
    else:
        wt(root, LAM + "export/retained_export.py", "def other():\n    return 1\n\n" + block("freeze_pin")
           + ("\nADDR = 's3://opal-data-x/y'\n" if variant == "typed_address" else ""))
    if variant != "no_handler":
        wt(root, LAM + "export/entry.py", "def other():\n    return 1\n\n" + block("submit_pin"))
    names = ["overwritten_version_still_exports_pinned_bytes", "forged_client_pin_ignored"]
    if variant == "missing_named_test":
        names = names[:1]
    t = ("import importlib.util\n"
         "spec = importlib.util.spec_from_file_location('m_pin', r'%s')\n"
         "m = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(m)\n" % (root / (LAM + "export/retained_export.py")))
    t += "".join("def test_case_%d():\n    assert m.freeze_pin(%d) == %d\n" % (i, i, 2 * i) for i in range(5))
    t += "".join("def test_%s():\n    assert m.freeze_pin(1) == 2\n" % n for n in names)
    if variant == "weak_tests":
        t = "".join("def test_w%d():\n    assert True\n" % i for i in range(7))
    wt(root, c["test"], t)
    changed = [LAM + "export/retained_export.py", c["test"]] + ([LAM + "export/entry.py"] if variant != "no_handler" else [])
    if variant == "stray":
        wt(root, "docs/other.md", "x")
        changed.append("docs/other.md")
    rec = {"base_commit": base, "changed_paths": sorted(changed), "negative_tests": ["overwritten_version_still_exports_pinned_bytes", "forged_client_pin_ignored"],
           "tests_total": 7, "tests_passed": 7, "mutant_tests_failed": 5, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
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
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


for cell, builder, negs in (
        ("1", build1, [("few_tests", "AC1"), ("weak_tests", "AC2"), ("stray", "AC3"), ("missing_entry", "AC3"), ("wrong_sha", "AC3"), ("bad_pin", "AC3"), ("files_missing", "AC3"),
                       ("build_only_fail", "AC3"), ("build_only_short", "AC3")]),
        ("2", build2, [("no_block", "AC2"), ("import_error", "AC2"), ("weak_tests", "AC2"), ("stray", "AC3"), ("no_handler", "AC3"), ("missing_named_test", "AC3"), ("typed_address", "AC3")])):
    root = builder()
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "IB204-%s-%s" % (cell, ac), root, True)
    shutil.rmtree(root, ignore_errors=True)
    for variant, ac in negs:
        root = builder(variant)
        expect(variant, "IB204-%s-%s" % (cell, ac), root, False)
        shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
