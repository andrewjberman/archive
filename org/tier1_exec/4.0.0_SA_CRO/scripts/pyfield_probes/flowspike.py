"""Q2 SPIKE -- what fraction does FLOW-LOCAL INFERENCE actually reach?

Mechanism under test = CTO~D's ruled option (b): track names BOUND FROM a known DataFrame
constructor, follow them within a scope, and only then treat name["lit"] as a COLUMN.

This measures REACH, not correctness. It answers exactly one question: of all string-literal
subscripts, what share sit on a base we can PROVE is a DataFrame by construction-tracking?

Prints its denominator. Emits the UNRESOLVED share as the headline, because that is the number
a build lane would have to declare as `unresolved` under LAW-1 honest-degrade.
"""

from __future__ import annotations
import ast
import os
import sys
import collections

# The constructor set. DELIBERATELY SMALL -- CTO~D ruled "smallest constructor set that clears
# a stated bar". Widening this is the tuning knob; the spike measures the FLOOR.
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
# methods that RETURN a dataframe when called on one (propagation set)
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


def constructor_name(node):
    """Return the callee name if this Call looks like a DF constructor."""
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return None


class Scope(ast.NodeVisitor):
    def __init__(self):
        self.df_names: set[str] = set()
        self.sub_on_df = 0
        self.sub_on_other = 0
        self.bases_unresolved = collections.Counter()

    def _bind(self, tgt, value):
        cn = constructor_name(value)
        if cn is None:
            return
        is_df = cn in DF_CONSTRUCTORS
        # propagation: x = <known-df>.method(...)
        if not is_df and cn in DF_METHODS and isinstance(value.func, ast.Attribute):
            b = value.func.value
            if isinstance(b, ast.Name) and b.id in self.df_names:
                is_df = True
            elif (
                isinstance(b, ast.Subscript)
                and isinstance(b.value, ast.Name)
                and b.value.id in self.df_names
            ):
                is_df = True
        if is_df:
            for t in [tgt] if not isinstance(tgt, (ast.Tuple, ast.List)) else tgt.elts:
                if isinstance(t, ast.Name):
                    self.df_names.add(t.id)

    def visit_Assign(self, node):
        for t in node.targets:
            self._bind(t, node.value)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if node.value is not None:
            self._bind(node.target, node.value)
        self.generic_visit(node)

    def visit_For(self, node):
        # for _, row in df.iterrows():  -> row is NOT a df; skip binding deliberately
        self.generic_visit(node)


def probe(path, agg):
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except Exception:
        agg["parse_errors"] += 1
        return
    s = Scope()
    s.visit(tree)  # pass 1: collect df-bound names
    for n in ast.walk(tree):  # pass 2: classify subscripts
        if isinstance(n, ast.Subscript):
            k = n.slice
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                b = n.value
                if isinstance(b, ast.Name):
                    if b.id in s.df_names:
                        agg["resolved_df"] += 1
                    else:
                        agg["unresolved"] += 1
                        agg["bases"][b.id] += 1
                else:
                    agg["unresolved_nonname"] += 1
    agg["df_names"] += len(s.df_names)
    agg["files"] += 1


agg = {
    "files": 0,
    "parse_errors": 0,
    "resolved_df": 0,
    "unresolved": 0,
    "unresolved_nonname": 0,
    "df_names": 0,
    "bases": collections.Counter(),
}
files = []
for root in sys.argv[1:]:
    for dp, _dn, fn in os.walk(root):
        if "__pycache__" in dp:
            continue
        files += [os.path.join(dp, f) for f in fn if f.endswith(".py")]
for f in sorted(files):
    probe(f, agg)

total = agg["resolved_df"] + agg["unresolved"] + agg["unresolved_nonname"]
print(
    f"DENOMINATOR: {agg['files']} files ({agg['parse_errors']} parse errors), "
    f"{total} string-literal subscripts"
)
print(f"  df-bound names found ............ {agg['df_names']}")
print(f"  RESOLVED as DataFrame column ... {agg['resolved_df']}")
print(f"  unresolved (name base) ......... {agg['unresolved']}")
print(f"  unresolved (non-name base) ..... {agg['unresolved_nonname']}")
if total:
    print(
        f"\n>> FLOW-LOCAL REACH: {100 * agg['resolved_df'] / total:.1f}%   "
        f"UNRESOLVED: {100 * (total - agg['resolved_df']) / total:.1f}%"
    )
print("\nTOP UNRESOLVED BASES (what a wider constructor set would have to catch):")
for n, c in agg["bases"].most_common(12):
    print(f"  {c:5d}  {n}")
