"""Is the unresolved mass FUNCTION PARAMETERS? If so, widening the constructor set
cannot fix it -- the base arrives from a CALLER, and flow-LOCAL inference is blind by
construction. That changes which mechanism the PRD needs."""

from __future__ import annotations
import ast
import os
import sys
import collections

params_subscripted = 0
other_unresolved = 0
param_names_hit = collections.Counter()
files = 0
for root in sys.argv[1:]:
    for dp, _dn, fn in os.walk(root):
        if "__pycache__" in dp:
            continue
        for f in fn:
            if not f.endswith(".py"):
                continue
            p = os.path.join(dp, f)
            try:
                tree = ast.parse(open(p, encoding="utf-8", errors="replace").read())
            except Exception:
                continue
            files += 1
            for fn_node in ast.walk(tree):
                if not isinstance(fn_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                pnames = {a.arg for a in fn_node.args.args} | {
                    a.arg for a in fn_node.args.kwonlyargs
                }
                if fn_node.args.vararg:
                    pnames.add(fn_node.args.vararg.arg)
                for n in ast.walk(fn_node):
                    if isinstance(n, ast.Subscript):
                        k = n.slice
                        if (
                            isinstance(k, ast.Constant)
                            and isinstance(k.value, str)
                            and isinstance(n.value, ast.Name)
                        ):
                            if n.value.id in pnames:
                                params_subscripted += 1
                                param_names_hit[n.value.id] += 1
                            else:
                                other_unresolved += 1
tot = params_subscripted + other_unresolved
print(
    f"DENOMINATOR: {files} files, {tot} name-based string-literal subscripts INSIDE functions"
)
print(
    f"  base is a FUNCTION PARAMETER ... {params_subscripted}  ({100 * params_subscripted / tot:.1f}%)"
)
print(
    f"  base is local/other ............ {other_unresolved}  ({100 * other_unresolved / tot:.1f}%)"
)
print("\nTOP PARAMETER BASES:")
for n, c in param_names_hit.most_common(10):
    print(f"  {c:5d}  {n}")
