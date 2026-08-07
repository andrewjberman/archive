"""FEASIBILITY PROBE -- can a Python AST resolve COLUMN-grain IO on real gold scripts?
Counts, per file: column-literal reads df["x"], column writes df["y"]=..., .rename(columns=...),
groupby/merge keys, and DYNAMIC subscripts (df[var]) which are the unresolvable class.
Prints its denominator. Not a tool -- a measurement."""

from __future__ import annotations
import ast
import sys
import os
import json


def probe(path):
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(src)
    except Exception as e:
        return {"file": path, "parse_error": str(e)}
    r = {
        "file": path,
        "lines": src.count("\n") + 1,
        "sub_read_literal": 0,
        "sub_read_dynamic": 0,
        "sub_write_literal": 0,
        "sub_write_dynamic": 0,
        "rename_kw": 0,
        "groupby_keys": 0,
        "merge_on": 0,
        "agg_dict": 0,
    }
    for n in ast.walk(tree):
        # df["col"] = ...   vs   df["col"] read
        if isinstance(n, ast.Subscript):
            k = n.slice
            lit = isinstance(k, ast.Constant) and isinstance(k.value, str)
            listlit = (
                isinstance(k, ast.List)
                and all(
                    isinstance(e, ast.Constant) and isinstance(e.value, str)
                    for e in k.elts
                )
                and k.elts
            )
            store = isinstance(n.ctx, ast.Store)
            if lit or listlit:
                r["sub_write_literal" if store else "sub_read_literal"] += 1
            elif isinstance(k, (ast.Name, ast.Attribute, ast.Call, ast.BinOp)):
                r["sub_write_dynamic" if store else "sub_read_dynamic"] += 1
        if isinstance(n, ast.Call):
            fn = n.func.attr if isinstance(n.func, ast.Attribute) else None
            for kw in n.keywords or []:
                if kw.arg == "columns" and fn == "rename":
                    r["rename_kw"] += 1
                if kw.arg == "on" and fn in ("merge", "join"):
                    r["merge_on"] += 1
            if fn == "groupby" and n.args:
                r["groupby_keys"] += 1
            if fn == "agg" and n.args and isinstance(n.args[0], ast.Dict):
                r["agg_dict"] += 1
    return r


roots = sys.argv[1:]
files = []
for root in roots:
    for dp, _dn, fn in os.walk(root):
        if "__pycache__" in dp:
            continue
        for f in fn:
            if f.endswith(".py"):
                files.append(os.path.join(dp, f))
print(f"DENOMINATOR: {len(files)} .py files under {roots}")
tot = {}
perr = 0
for f in sorted(files):
    r = probe(f)
    if "parse_error" in r:
        perr += 1
        continue
    for k, v in r.items():
        if isinstance(v, int):
            tot[k] = tot.get(k, 0) + v
print(f"parse errors: {perr}")
print(json.dumps(tot, indent=2))
lit = tot.get("sub_read_literal", 0) + tot.get("sub_write_literal", 0)
dyn = tot.get("sub_read_dynamic", 0) + tot.get("sub_write_dynamic", 0)
den = lit + dyn
print(f"\nCOLUMN SUBSCRIPTS: {den} total | literal {lit} | dynamic {dyn}")
if den:
    print(f"STATICALLY RESOLVABLE: {100 * lit / den:.1f}%")
