"""c22_check.py -- grades MX-c-22 (the etfs_get_positioning extension: optional fund_ticker and as_of history, existing answer byte-equal), from the repo root.

  python c22_check.py ac2   the shape of the change in the NEW gateway tree: etfs_get_positioning(as_of: str = "", fund_ticker: str = "") (both optional strings, in that order);
                            the lines the change ADDS to app/integrations/portal_index/integration.py (against BASE_REF) type no S3 key (no gold/, silver/, platinum/ path literal and
                            no opal-data- bucket literal: keys come from the catalog rows opal_data_etfs_gold_book and opal_data_etfs_gold_holding); a NEW test file
                            tests/test_positioning_extension.py exists with at least 10 tests
  python c22_check.py ac3   the gateway tests pass: tests/test_positioning_extension.py, tests/test_portal_index.py, tests/test_opal_discover.py, tests/test_og_et2.py

The NEW tree is infra/aws/ec2/opal-gateway, or C22_GW (a planted tree). Exit 0 PASS, 1 FAIL, 9 no run. ac1 (the difference control) is c22_equal.py."""
import ast
import os
import re
import subprocess
import sys

BASE_REF = "06cfb6db64"
GW = "infra/aws/ec2/opal-gateway"
NEWGW = os.environ.get("C22_GW") or GW
PI = "app/integrations/portal_index/integration.py"
TYPED = re.compile(r"""["'][^"']*\b(gold|silver|platinum|bronze)/[A-Za-z_{}/.]*|opal-data-[a-z0-9-]+""")


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def signature_ok(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "etfs_get_positioning":
            names = [a.arg for a in node.args.args]
            defaults = [d.value if isinstance(d, ast.Constant) else None for d in node.args.defaults]
            return names == ["as_of", "fund_ticker"] and defaults == ["", ""]
    return False


def added_lines():
    r = subprocess.run(["git", "show", "%s:%s/%s" % (BASE_REF, GW, PI)], capture_output=True)
    if r.returncode != 0:
        print("ERROR: git show base rc %d" % r.returncode)
        sys.exit(9)
    base = set(r.stdout.decode("utf-8").splitlines())
    new = open(os.path.join(NEWGW, PI), encoding="utf-8").read().splitlines()
    return [ln for ln in new if ln not in base]


def ac2():
    path = os.path.join(NEWGW, PI)
    res = [("etfs_get_positioning(as_of: str = '', fund_ticker: str = '') in that order", signature_ok(path))]
    added = added_lines()
    typed = [ln.strip()[:100] for ln in added if TYPED.search(ln) and not ln.strip().startswith("#")]
    print("DENOMINATOR lines added to portal_index/integration.py: %d; with a typed S3 key or bucket literal: %d" % (len(added), len(typed)))
    for t in typed[:5]:
        print("  TYPED %s" % t)
    res.append(("the added lines type no S3 key or bucket", not typed))
    tf = os.path.join(NEWGW, "tests", "test_positioning_extension.py")
    n = 0
    if os.path.exists(tf):
        n = sum(1 for node in ast.walk(ast.parse(open(tf, encoding="utf-8").read())) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    print("new tests in test_positioning_extension.py: %d" % n)
    res.append(("the new test file holds at least 10 tests", n >= 10))
    return report(res)


def ac3():
    root = NEWGW
    env = dict(os.environ, PYTHONPATH=os.path.abspath(root))
    files = ["tests/test_positioning_extension.py", "tests/test_portal_index.py", "tests/test_opal_discover.py", "tests/test_og_et2.py"]
    missing = [f for f in files if not os.path.exists(os.path.join(root, f))]
    if missing:
        print("ERROR: absent %s" % missing)
        return report([("the four test files exist", False)])
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header"] + files, cwd=root, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    return report([("the four test files pass", r.returncode == 0)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
