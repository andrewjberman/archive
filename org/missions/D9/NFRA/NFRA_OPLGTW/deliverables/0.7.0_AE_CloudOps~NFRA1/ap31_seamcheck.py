#!/usr/bin/env python
"""OG-ap-31 Phase A: for each STOP-class seam edge (a taken file imports a module that differs live->trunk and is NOT taken), compare the NAMES the importer uses
from that module, as AST dumps, at the live ref and at trunk_sha. Read-only.
usage: python ap31_seamcheck.py <live_ref> <trunk_sha> <out.json>   (repository root)
Equal dumps for every name the importer uses = the base file satisfies the taken file; a name that differs or is missing = STOP."""
from __future__ import annotations

import ast
import json
import subprocess
import sys

LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
EDGES = [("app/data_entitlement.py", "app/tools.py"), ("app/server.py", "app/yearinreview_view.py"),
         ("tests/test_og_en8.py", "app/tools.py"), ("tests/test_opal_discover.py", "app/destructive_ops.py")]


def blob(ref, p):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, G + p)], capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def top_defs(src):
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[n.name] = ast.dump(n)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.dump(n.value)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            out[n.target.id] = ast.dump(n)
    return out


def used_names(src, mod):
    """Names the importer takes from `mod` (module path relative to app/): from-imports, plus attribute uses of an imported module alias."""
    tree = ast.parse(src)
    dotted = "app." + mod[len("app/"):-3].replace("/", ".")
    leaf = dotted.rsplit(".", 1)[-1]
    names, aliases = set(), set()
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            m = ("." * n.level) + (n.module or "")
            if (n.module or "").lstrip(".") in (dotted, leaf) or (n.level and (n.module or "") == leaf):
                for a in n.names:
                    names.add(a.name)
            elif (n.module in ("app", None) or m in (".", "app")) and any(a.name == leaf for a in n.names):
                for a in n.names:
                    if a.name == leaf:
                        aliases.add(a.asname or a.name)
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name == dotted:
                    aliases.add(a.asname or a.name)
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in aliases:
            names.add(n.attr)
    return sorted(names), sorted(aliases)


rows, stop = [], 0
for imp, mod in EDGES:
    src = blob(TRUNK, imp)
    names, aliases = used_names(src, mod)
    a, b = blob(LIVE, mod), blob(TRUNK, mod)
    da, db = top_defs(a), top_defs(b)
    detail, bad = [], []
    for nm in names:
        if nm not in da:
            bad.append((nm, "missing at live"))
        elif nm not in db:
            bad.append((nm, "missing at trunk"))
        elif da[nm] != db[nm]:
            bad.append((nm, "DIFFERS live vs trunk"))
        detail.append(nm)
    rows.append({"importer": imp, "module": mod, "names_used": detail, "aliases": aliases, "bad": bad})
    stop += len(bad)
    print("%-34s -> %-28s names used %2d %s; unsatisfied %d %s" % (imp, mod, len(detail), detail[:6], len(bad), bad))
print("unsatisfied names in total: %d" % stop)
json.dump({"live": LIVE, "trunk": TRUNK, "rows": rows, "unsatisfied": stop}, open(OUT, "w"), indent=1)
