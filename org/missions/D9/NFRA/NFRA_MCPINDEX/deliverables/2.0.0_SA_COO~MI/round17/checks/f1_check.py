"""f1_check.py -- grades MX-c-19 / F1 (the firm field on the 24 prose-firm silver rows; a firm sees its own rows and no other firm's), from the repo root.

  python f1_check.py ac1   the catalog row field: the rows that carry `firm` are EXACTLY the 24 of org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round17/f1_firm_map.json, each with its
                           mapped value (49financial or inflection), each value one of the registry's firm names for that row; no other row carries a firm field
  python f1_check.py ac2   the visibility difference control (vis_matrix.py, run under the BASE tree at git ref BASE_REF and under the NEW tree): for every
                           silver_datasets row x {opal-internal, each known firm, an unknown firm, an empty firm}: opal-internal unchanged; each known firm sees
                           its OLD rows plus exactly the mapped rows of its OWN firm; no mapped row is visible to another firm; the unknown and empty firm see nothing.
                           Prints the pair count, the newly-visible count and the cross-firm leak count (0 expected)
  python f1_check.py ac3   gateway tests: tests/test_firm_catalog_visibility.py (new, at least 6 tests) with tests/test_opal_discover.py and tests/test_portal_index.py pass

The NEW tree is infra/aws/ec2/opal-gateway of the worktree, or F1_GW (a planted tree). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import json
import os
import subprocess
import sys
import tempfile

BASE_REF = "1b18b94979"
GW = "infra/aws/ec2/opal-gateway"
NEWGW = os.environ.get("F1_GW") or GW
HERE = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "2.0.0_SA_COO~MI", "round17", "f1_firm_map.json")
REG = os.path.join("infra", "logic", "registry", "catalog_fork_keys.json")
KNOWN = ("49financial", "inflection", "cottonwood")


def matrix(root):
    r = subprocess.run([sys.executable, os.path.join(HERE, "vis_matrix.py"), root], capture_output=True, text=True, timeout=200)
    line = (r.stdout or "").strip().splitlines()[-1:] or [""]
    try:
        return json.loads(line[0])
    except ValueError:
        print("ERROR: vis_matrix under %s rc %d: %s" % (root, r.returncode, (r.stderr or r.stdout)[-300:]))
        sys.exit(9)


def base_tree():
    d = tempfile.mkdtemp(prefix="f1_base_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (BASE_REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive %s failed: %s" % (BASE_REF, p.stderr[-200:]))
        sys.exit(9)
    return os.path.join(d, GW)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ac1():
    want = json.load(open(MAP, encoding="utf-8"))["rows"]
    new = matrix(NEWGW)["firm_field"]
    reg = json.load(open(REG, encoding="utf-8"))["rows"]
    res = []
    res.append(("the rows carrying a firm field are exactly the %d mapped rows" % len(want), sorted(new) == sorted(want)))
    wrong = [e for e in want if new.get(e) != want[e]]
    res.append(("%d of %d mapped rows carry their mapped firm" % (len(want) - len(wrong), len(want)), not wrong and len(want) == 24))
    res.append(("every value is a known firm", all(v in KNOWN for v in new.values()) and bool(new)))
    # the mapped firm is one the registry's firm values for that row actually name
    import yaml
    named = 0
    for e, f in want.items():
        d = yaml.safe_load(open(os.path.join("workflows", "atom_decomposition", "catalog_entries", e + ".yaml"), encoding="utf-8"))
        full = ((reg.get(d["contract"]["id"]) or {}).get("restore") or {}).get("fork_keys") or d.get("fork_keys") or {}
        vals = " ".join(v for v in (((full.get("firm") or {}).get("values")) or []) if isinstance(v, str)).lower()
        named += 1 if (f == "49financial" and ("49f" in vals or "49 financial" in vals or "49financial" in vals)) or (f in vals and f != "49financial") else 0
    res.append(("%d of %d mapped firms are named by the row's registry firm values" % (named, len(want)), named == len(want)))
    print("DENOMINATOR mapped rows %d; rows with a firm field in the new tree %d" % (len(want), len(new)))
    return report(res)


def ac2():
    want = json.load(open(MAP, encoding="utf-8"))["rows"]
    b, n = matrix(base_tree()), matrix(NEWGW)
    principals = [k for k in b if k == "opal-internal" or k.startswith("firm:")]
    pairs = len(principals) * n["rows"]
    res = []
    res.append(("the silver row sets are equal (%d rows)" % n["rows"], n["rows"] == b["rows"]))
    res.append(("opal-internal sees the same rows", n["opal-internal"] == b["opal-internal"]))
    newly = 0
    for f in KNOWN:
        key = "firm:" + f
        mine = sorted(e for e, v in want.items() if v == f)
        expect = sorted(set(b[key]) | set(mine))
        newly += len(set(n[key]) - set(b[key]))
        res.append(("firm %s sees its old %d rows plus exactly its %d mapped rows" % (f, len(b[key]), len(mine)), n[key] == expect))
    leaks = sum(1 for e, f in want.items() for g in KNOWN if g != f and e in n["firm:" + g])
    res.append(("no mapped row is visible to another firm (leaks %d)" % leaks, leaks == 0))
    res.append(("the unknown and the empty firm see nothing", not n["firm:nosuchfirm"] and not n["firm:"]))
    res.append(("no error in either run", not n.get("errors") and not b.get("errors")))
    print("DENOMINATOR silver rows %d x principals %d = %d pairs; newly visible %d (expected %d); cross-firm leaks %d" % (n["rows"], len(principals), pairs, newly, len(want), leaks))
    return report(res)


def ac3():
    root = NEWGW
    f = os.path.join(root, "tests", "test_firm_catalog_visibility.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(root))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_firm_catalog_visibility.py",
                        "tests/test_opal_discover.py", "tests/test_portal_index.py"], cwd=root, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    new_n = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_firm_catalog_visibility.py"], cwd=root, env=env,
                           capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (new_n.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the three test files pass", r.returncode == 0), ("the new file holds at least 6 tests", n_new >= 6)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
