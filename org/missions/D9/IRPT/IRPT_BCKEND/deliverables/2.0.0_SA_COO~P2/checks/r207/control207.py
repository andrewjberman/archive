"""Positive control and negatives for p207_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control207.py <real_repo_root>
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r207/p207_cells.py"
for sub in ("r196", "r200", "r201", "r207"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p207_cells as P  # noqa: E402

P6 = P.P6


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


def block(marker, fn):
    return "def %s(x):\n    # BEGIN %s\n    x = x * 2\n    # END %s\n    return x\n" % (fn, marker, marker)


def build(cid, variant=None):
    c = P.CELLS[cid]
    root = Path(tempfile.mkdtemp(prefix="c207%s_" % cid))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in c["regress"]:
        wt(root, rel, "def test_ok():\n    assert True\n")
    for rel in c["mutants"]:
        wt(root, rel, "def other():\n    return 1\n")
    wt(root, P.X + "handler.py", "def other():\n    return 1\n")
    base = commit(root, "base")
    changed = {c["mutants"][0], *c["required"]}
    changed.discard(c["test"])
    if variant == "any_of_missing":
        changed.add(c["mutants"][2])
        changed -= set(c["any_of"])
    elif not set(c["any_of"]) & changed:
        changed.add(c["any_of"][0])
    target = c["mutants"][0]
    for i, rel in enumerate(sorted(changed)):
        i = 0 if rel == target else i + 1
        if variant == "no_block":
            wt(root, rel, "def other():\n    return 1\n\ndef fn_%d(x):\n    return x * 2\n" % i)
        elif variant == "import_error":
            wt(root, rel, "def other():\n    return 1\n\n# BEGIN %s\nHELPER = 3\n# END %s\nVALUE = HELPER\n\ndef fn_%d(x):\n    return x * 2\n" % (c["marker"], c["marker"], i))
        else:
            wt(root, rel, "def other():\n    return 1\n\n" + block(c["marker"], "fn_%d" % i) + ("\nADDR = 's3://opal-data-x/y'\n" if variant == "typed_address" else ""))
    names = list(c["named"])
    if variant == "missing_named_test":
        names = names[:-1]
    t = ("import importlib.util\n"
         "spec = importlib.util.spec_from_file_location('m_c207', r'%s')\n"
         "m = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(m)\n" % (root / target))
    n_plain = c["min_tests"] - len(names) + (0 if variant != "few_tests" else -2)
    t += "".join("def test_case_%d():\n    assert m.fn_0(%d) == %d\n" % (i, i, 2 * i) for i in range(max(n_plain, 0)))
    t += "".join("def test_%s():\n    assert m.fn_0(1) == 2\n" % n for n in names)
    if variant == "weak_tests":
        t = "".join("def test_w%d():\n    assert True\n" % i for i in range(c["min_tests"] + 2))
    wt(root, c["test"], t)
    allchanged = sorted(changed | {c["test"]})
    if variant == "stray":
        wt(root, "docs/other.md", "x")
        allchanged.append("docs/other.md")
    rec = {"base_commit": base, "changed_paths": sorted(allchanged), "negative_tests": list(c["named"]), "tests_total": 9, "tests_passed": 9,
           "mutant_tests_failed": 5, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
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


NEGS = [("no_block", "AC2"), ("import_error", "AC2"), ("weak_tests", "AC2"), ("few_tests", "AC1"), ("stray", "AC3"), ("any_of_missing", "AC3"),
        ("missing_named_test", "AC3"), ("typed_address", "AC3")]
for cell in ("1", "2"):
    root = build(cell)
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "IB207-%s-%s" % (cell, ac), root, True)
    shutil.rmtree(root, ignore_errors=True)
    for variant, ac in NEGS:
        root = build(cell, variant)
        expect(variant, "IB207-%s-%s" % (cell, ac), root, False)
        shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
