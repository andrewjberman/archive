"""plant_f1.py -- the ISSUER's cut-time planted arms for f1.AC1 to AC3 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root.

Extracts the BASE gateway tree (git ref f1_check.BASE_REF) five times into temp folders and plants into each: the reference change (the firm field on the 24 mapped rows of the
catalog, `_silver_answer` scoping a firm-scoped row to its own firm, a 6-test file) and four defects. Runs f1_check with F1_GW pointing at each."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import f1_check as fc  # noqa: E402

OLD = ('    if rule == "firm-scoped" and principal_class != catalog_gate.OPAL_INTERNAL:\n'
       '        return None                            # no firm field on the row to scope by: no firm principal may see it\n'
       '    firm = catalog_gate.OPAL_INTERNAL\n')
GOOD = ('    row_firm = str(row.get("firm") or "")\n'
        '    scoped = rule == "firm-scoped" and principal_class != catalog_gate.OPAL_INTERNAL\n'
        '    if scoped and not (row_firm in catalog_gate.KNOWN_FIRMS and principal_class == "firm" and principal_firm == row_firm):\n'
        '        return None\n'
        '    firm = row_firm if scoped else catalog_gate.OPAL_INTERNAL\n')
LEAK = ('    row_firm = str(row.get("firm") or "")\n'
        '    scoped = rule == "firm-scoped" and principal_class != catalog_gate.OPAL_INTERNAL\n'
        '    if scoped and not (row_firm in catalog_gate.KNOWN_FIRMS and principal_class == "firm"):\n'
        '        return None\n'
        '    firm = principal_firm if scoped else catalog_gate.OPAL_INTERNAL\n')
TESTS = "\n\n".join("def test_planted_%d():\n    assert True" % i for i in range(6)) + "\n"


def build(tmp, name, patch=GOOD, mapping=None, n_tests=6):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    subprocess.run("git archive %s %s | tar -x -C %s" % (fc.BASE_REF, fc.GW, d.replace("\\", "/")), shell=True, check=True, capture_output=True)
    root = os.path.join(d, fc.GW)
    p = os.path.join(root, "app", "integrations", "opal_discover", "integration.py")
    s = open(p, encoding="utf-8").read()
    assert OLD in s, "the base _silver_answer text moved"
    open(p, "w", encoding="utf-8", newline="\n").write(s.replace(OLD, patch))
    cp = os.path.join(root, "app", "refs", "DATA_CATALOG.yaml")
    cat = yaml.safe_load(open(cp, encoding="ascii"))
    want = dict(mapping or json.load(open(fc.MAP, encoding="utf-8"))["rows"])
    for r in cat["silver_datasets"]:
        if r.get("entity") in want:
            r["firm"] = want[r["entity"]]
    with open(cp, "w", encoding="ascii", newline="\n") as fh:
        yaml.safe_dump(cat, fh, sort_keys=False, allow_unicode=False)
    open(os.path.join(root, "tests", "test_firm_catalog_visibility.py"), "w", encoding="ascii").write(
        "\n\n".join("def test_planted_%d():\n    assert True" % i for i in range(n_tests)) + "\n")
    return root


def main():
    tmp = tempfile.mkdtemp(prefix="plant_f1_")
    want = json.load(open(fc.MAP, encoding="utf-8"))["rows"]
    first = sorted(want)[0]
    wrong = dict(want)
    wrong[first] = "cottonwood" if want[first] != "cottonwood" else "inflection"
    trees = {"good": build(tmp, "good"), "leak": build(tmp, "leak", patch=LEAK), "wrongfirm": build(tmp, "wrongfirm", mapping=wrong),
             "fewtests": build(tmp, "fewtests", n_tests=5)}
    # a tree whose catalog carries a firm field on one UNMAPPED row too (scope creep)
    creep = build(tmp, "creep")
    cp = os.path.join(creep, "app", "refs", "DATA_CATALOG.yaml")
    cat = yaml.safe_load(open(cp, encoding="ascii"))
    extra = next(r for r in cat["silver_datasets"] if r.get("entity") not in want and r.get("firm_scope_rule") == "firm-scoped")
    extra["firm"] = "49financial"
    with open(cp, "w", encoding="ascii", newline="\n") as fh:
        yaml.safe_dump(cat, fh, sort_keys=False, allow_unicode=False)
    trees["creep"] = creep
    arms = [("good tree, ac1", "good", "ac1", 0), ("good tree, ac2", "good", "ac2", 0), ("five tests only, ac3", "fewtests", "ac3", 1),
            ("a leak (every firm sees every firm-scoped row), ac2", "leak", "ac2", 1), ("one mapped row given the wrong firm, ac1", "wrongfirm", "ac1", 1),
            ("one mapped row given the wrong firm, ac2", "wrongfirm", "ac2", 1), ("a firm field on an unmapped row, ac1", "creep", "ac1", 1),
            ("a firm field on an unmapped row, ac2", "creep", "ac2", 1)]
    ok = wrong_n = 0
    for label, key, ac, want_rc in arms:
        r = subprocess.run([sys.executable, os.path.join(HERE, "f1_check.py"), ac], env=dict(os.environ, F1_GW=trees[key]), capture_output=True, text=True, timeout=400)
        if r.returncode == want_rc:
            ok += 1
            print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
        else:
            wrong_n += 1
            print("ARM WRONG: %s -> rc=%d want %d" % (label, r.returncode, want_rc))
            print("\n".join(r.stdout.splitlines()[-6:]))
    print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong_n))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if wrong_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
