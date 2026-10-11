"""ADVI_FIRMBKTS round 4 check for cell FB-g-26 (the two stale-advisor cleanups read the `Errors` of delete_objects and exit
non-zero naming the keys; the CTO's act-0 CTO half ADDENDUM 1 item 2), issuer 2.0.0_SA_COO~B1.

Row ADVI_FIRMBKTS-D1-S29: boto3 `delete_objects` answers HTTP 200 with a per-key `Errors` list for an AccessDenied, so a
cleanup that does not read it silently removes nothing at the canonical home.

--arms static [--root <tree>]  (4 arms)
  F1 D_04.client_portal_summary.py: its ONE `delete_objects` call is inside a function (or the module body) that reads the
     response's `Errors` and ends in a non-zero exit (`sys.exit(<non-zero>)`, `raise SystemExit(<non-zero>)` or `raise`),
     and the message names the failing keys.
  F2 D_02.advisor_client_detail.py: the same, for its ONE `delete_objects` call.
  F3 the unit test `data/black_diamond/scripts/gold/tests/test_delete_errors_fail_loud.py` exists and passes under
     `python -m unittest discover` (at least 4 tests: for each script a stubbed per-key AccessDenied response raises or
     exits non-zero naming the key, and a clean response returns).
  F4 control: each script holds exactly one `delete_objects` call and no `delete_object(` call, so the fix is the whole
     delete surface of the two blobs.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import ast
import os
import re
import subprocess
import sys

GOLD = "data/black_diamond/scripts/gold"
FILES = {"D_04": GOLD + "/D_04.client_portal_summary.py", "D_02": GOLD + "/D_02.advisor_client_detail.py"}
TEST = GOLD + "/tests/test_delete_errors_fail_loud.py"


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _calls(tree, name):
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == name]


def _scope_of(tree, call):
    best = tree
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(c is call for c in ast.walk(n)):
                if best is tree or n.lineno >= getattr(best, "lineno", 0):
                    best = n
    return best


def _fail_loud(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    calls = _calls(tree, "delete_objects")
    if len(calls) != 1:
        return False, "delete_objects calls=%d" % len(calls)
    scope = _scope_of(tree, calls[0])
    nodes = list(ast.walk(scope))
    reads_errors = any(isinstance(n, ast.Constant) and n.value == "Errors" for n in nodes)
    exits = False
    for n in nodes:
        if isinstance(n, ast.Raise):
            exits = True
        if isinstance(n, ast.Call):
            f = n.func
            nm = (f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", ""))
            if nm in ("exit", "SystemExit", "_exit"):
                nonzero = any(not (isinstance(a, ast.Constant) and a.value in (0, None)) for a in n.args) or not n.args
                exits = exits or nonzero
    seg = ast.get_source_segment(src, scope) or ""
    names_keys = re.search(r"Key|keys|\['Key'\]|\"Key\"", seg) is not None
    return reads_errors and exits and names_keys, "reads Errors=%s exits=%s names keys=%s" % (
        reads_errors, exits, names_keys)


def static(root):
    res = []
    for tag, rel in FILES.items():
        p = os.path.join(root, *rel.split("/"))
        try:
            ok, why = _fail_loud(p)
        except Exception as e:  # noqa: BLE001
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:100])
        print("  %s %s: %s" % (tag, rel.rsplit("/", 1)[-1], why))
        res.append(("F%d %s reads delete_objects Errors and exits non-zero naming the keys" % (
            1 if tag == "D_04" else 2, tag), ok))
    tp = os.path.join(root, *TEST.split("/"))
    ok3 = False
    if os.path.isfile(tp):
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.dirname(tp), "-p",
                            os.path.basename(tp)], cwd=root, capture_output=True, text=True, timeout=110)
        m = re.search(r"Ran (\d+) tests?", r.stderr + r.stdout)
        n = int(m.group(1)) if m else 0
        ok3 = r.returncode == 0 and n >= 4
        print("  unit test: rc=%d ran=%d" % (r.returncode, n))
    else:
        print("  unit test file absent")
    res.append(("F3 the unit test exists and passes (stubbed AccessDenied fails loud, a clean delete passes)", ok3))
    ok4 = True
    for tag, rel in FILES.items():
        src = open(os.path.join(root, *rel.split("/")), encoding="utf-8").read()
        t = ast.parse(src)
        c1, c2 = len(_calls(t, "delete_objects")), len(_calls(t, "delete_object"))
        print("  %s delete_objects=%d delete_object=%d" % (tag, c1, c2))
        ok4 = ok4 and c1 == 1 and c2 == 0
    res.append(("F4 each script holds one delete_objects call and no delete_object call", ok4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("static",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = static(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the scripts readable", False)]
    order = ["F1", "F2", "F3", "F4"]
    res.sort(key=lambda t: order.index(t[0].split()[0]) if t[0].split()[0] in order else 9)
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 FAIL-LOUD: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
