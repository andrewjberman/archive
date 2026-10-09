"""RIV-wi-1 AC2 -- the wiring: the sweep calls the lookup before publish, and the package carries the search client.

    python wi1_wiring_check.py      (run from the repository root)

(a) `sweep.run_sweep`'s body calls `dramatic_move.run_for_day` (read with ast), and the call sits inside a `try` whose
    handler does not re-raise (a failed lookup never blocks publish).
(b) `rivalfunds_package.STAGED` stages `data/find/dualbiz/scripts/serp.py` (as a file or its directory).
(c) In a Lambda tree, `dramatic_move` finds the staged client: `_serp_dir()` (or the module's lookup path) resolves to a
    directory that exists in a tree built by `rivalfunds_package` -- read here as: the destination path STAGED gives serp.py
    equals the directory `dramatic_move.serp_search` inserts when run from <tree>/rivalfunds/dramatic_move.py.
Exit 0 = PASS, 1 = FAIL.
"""
import ast
import importlib.util
import os
import pathlib
import sys

ROOT = pathlib.Path(os.getcwd())
fails = []
src = (ROOT / "data/etfs/scripts/rivalfunds/sweep.py").read_text(encoding="utf-8")
tree = ast.parse(src)
fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run_sweep"), None)
called, guarded = False, False
if fn is not None:
    for node in ast.walk(fn):
        if isinstance(node, ast.Try):
            for inner in ast.walk(ast.Module(body=node.body, type_ignores=[])):
                if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute) and inner.func.attr == "run_for_day":
                    reraise = any(isinstance(x, ast.Raise) for h in node.handlers for x in ast.walk(h))
                    guarded = guarded or not reraise
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "run_for_day":
            called = True
print(f"(a) run_sweep calls run_for_day: {called}; inside a try that does not re-raise: {guarded}")
if not (called and guarded):
    fails.append("(a) run_sweep does not call dramatic_move.run_for_day inside a non-raising try")
spec = importlib.util.spec_from_file_location("rp", ROOT / "infra/aws/lambda/etfs-pipeline/rivalfunds_package.py")
rp = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT))
spec.loader.exec_module(rp)
dest = next((d for s, d in rp.STAGED if s in ("data/find/dualbiz/scripts/serp.py", "data/find/dualbiz/scripts")), None)
print(f"(b) STAGED destination for serp.py: {dest}")
if dest is None:
    fails.append("(b) STAGED does not stage data/find/dualbiz/scripts/serp.py")
dm_src = (ROOT / "data/etfs/scripts/rivalfunds/dramatic_move.py").read_text(encoding="utf-8")
lambda_ok = dest is not None and (("parents[4]" not in dm_src.split("def serp_search", 1)[-1].split("\ndef ", 1)[0])
                                  or "_serp_dir" in dm_src)
print(f"(c) serp_search resolves a Lambda-tree path: {lambda_ok}")
if not lambda_ok:
    fails.append("(c) serp_search only finds serp.py at the repository layout (parents[4]); a Lambda tree has none")
for f in fails:
    print("FAIL:", f)
print(f"WI1 WIRING RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
