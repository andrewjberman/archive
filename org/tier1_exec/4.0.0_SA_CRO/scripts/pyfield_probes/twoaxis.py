"""ARE THE TWO DISCRIMINATORS ADDITIVE OR OVERLAPPING?

CTO~D's question. Two INDEPENDENT signals that a name["lit"] subscript is a DataFrame column:

  BINDING-side  (mine)     the base name was bound from a DF constructor / df-returning method
  USAGE-side    (CTO~D's)  a pandas-only method is called ON THE SUBSCRIPT RESULT

This does NOT need the column denominator. It answers: does usage-side reach subscripts that
binding-side misses, and by how much? Reports the 2x2 so overlap is visible, not inferred.
"""

from __future__ import annotations
import ast
import os
import sys
import collections

DF_CONSTRUCTORS = {
    "read_parquet",
    "read_csv",
    "read_json",
    "read_sql",
    "read_excel",
    "DataFrame",
    "concat",
    "merge",
    "json_normalize",
}
DF_METHODS = {
    "merge",
    "copy",
    "drop",
    "dropna",
    "fillna",
    "rename",
    "reset_index",
    "set_index",
    "sort_values",
    "query",
    "assign",
    "astype",
    "head",
    "tail",
    "sample",
    "groupby",
    "agg",
}
# pandas-ONLY surface on a Series/DataFrame result. Deliberately EXCLUDES dict-ambiguous
# names (get, keys, items, values, update) -- a dict has those too.
USAGE_MARKERS = {
    "fillna",
    "nunique",
    "value_counts",
    "astype",
    "isna",
    "notna",
    "dropna",
    "unique",
    "str",
    "dt",
    "sum",
    "mean",
    "median",
    "std",
    "min",
    "max",
    "abs",
    "round",
    "cumsum",
    "shift",
    "diff",
    "rank",
    "between",
    "isin",
    "tolist",
    "to_numpy",
    "idxmax",
    "idxmin",
    "map",
    "apply",
    "where",
    "mask",
    "clip",
    "pct_change",
    "rolling",
    "expanding",
}


def constructor_name(node):
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return None


def df_names_of(tree):
    names = set()
    for _ in range(2):  # 2 passes so propagation settles
        for n in ast.walk(tree):
            if isinstance(n, (ast.Assign, ast.AnnAssign)):
                val = n.value
                if val is None:
                    continue
                cn = constructor_name(val)
                if cn is None:
                    continue
                is_df = cn in DF_CONSTRUCTORS
                if (
                    not is_df
                    and cn in DF_METHODS
                    and isinstance(val.func, ast.Attribute)
                ):
                    b = val.func.value
                    if isinstance(b, ast.Name) and b.id in names:
                        is_df = True
                    elif (
                        isinstance(b, ast.Subscript)
                        and isinstance(b.value, ast.Name)
                        and b.value.id in names
                    ):
                        is_df = True
                if not is_df:
                    continue
                tgts = n.targets if isinstance(n, ast.Assign) else [n.target]
                for t in tgts:
                    for tt in (
                        [t] if not isinstance(t, (ast.Tuple, ast.List)) else t.elts
                    ):
                        if isinstance(tt, ast.Name):
                            names.add(tt.id)
    return names


cell = collections.Counter()  # (binding, usage) -> count
usage_only_bases = collections.Counter()
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
            dfn = df_names_of(tree)
            # map: id(Subscript node) -> was a USAGE_MARKER called on it?
            used = set()
            for n in ast.walk(tree):
                if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Subscript):
                    if n.attr in USAGE_MARKERS:
                        used.add(id(n.value))
            for n in ast.walk(tree):
                if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name):
                    k = n.slice
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        b = n.value.id in dfn
                        u = id(n) in used
                        cell[(b, u)] += 1
                        if u and not b:
                            usage_only_bases[n.value.id] += 1

tot = sum(cell.values())
bb = cell[(True, True)] + cell[(True, False)]
uu = cell[(True, True)] + cell[(False, True)]
union = tot - cell[(False, False)]
print(f"DENOMINATOR: {files} files, {tot} name-based string-literal subscripts\n")
print("                      usage YES   usage NO")
print(f"  binding YES        {cell[(True, True)]:8d} {cell[(True, False)]:10d}")
print(f"  binding NO         {cell[(False, True)]:8d} {cell[(False, False)]:10d}\n")
print(f"  BINDING-side reach ....... {bb:5d}  {100 * bb / tot:.1f}%")
print(f"  USAGE-side reach ......... {uu:5d}  {100 * uu / tot:.1f}%")
print(f"  UNION (either) ........... {union:5d}  {100 * union / tot:.1f}%")
print(
    f"  usage-side NET-NEW ....... {cell[(False, True)]:5d}  (+{100 * cell[(False, True)] / tot:.1f} pts over binding alone)"
)
if bb:
    print(f"  overlap as share of binding: {100 * cell[(True, True)] / bb:.1f}%")
print("\nTOP BASES REACHED BY USAGE-SIDE ONLY (invisible to binding-side):")
for n, c in usage_only_bases.most_common(10):
    print(f"  {c:5d}  {n}")
