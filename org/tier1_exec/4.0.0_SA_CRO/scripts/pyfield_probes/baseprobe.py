"""THE DISCRIMINATION QUESTION: my 77.9% counts SUBSCRIPTS, not COLUMNS.
df["col"] and cfg["key"] are the SAME AST SHAPE. Can the BASE name discriminate?"""

from __future__ import annotations
import ast
import os
import sys
import collections

bases = collections.Counter()
files = []
for root in sys.argv[1:]:
    for dp, _dn, fn in os.walk(root):
        if "__pycache__" in dp:
            continue
        files += [os.path.join(dp, f) for f in fn if f.endswith(".py")]
for f in files:
    try:
        tree = ast.parse(open(f, encoding="utf-8", errors="replace").read())
    except Exception:
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript):
            k = n.slice
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                b = n.value
                name = (
                    b.id
                    if isinstance(b, ast.Name)
                    else (f".{b.attr}" if isinstance(b, ast.Attribute) else "<expr>")
                )
                bases[name] += 1
print(
    f"DENOMINATOR: {sum(bases.values())} string-literal subscripts over {len(files)} files"
)
print(f"DISTINCT BASE NAMES: {len(bases)}")
print("\nTOP 20 BASES:")
for n, c in bases.most_common(20):
    print(f"  {c:5d}  {n}")
dfish = sum(
    c
    for n, c in bases.items()
    if any(t in n.lower() for t in ("df", "frame", "data", "rec", "row"))
)
print(
    f"\nbases matching a df-ish naming convention: {dfish} / {sum(bases.values())} = {100 * dfish / sum(bases.values()):.1f}%"
)
