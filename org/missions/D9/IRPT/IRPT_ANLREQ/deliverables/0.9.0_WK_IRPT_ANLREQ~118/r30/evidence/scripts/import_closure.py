"""Scratch import-closure reader for the r28 resident package (outside the product tree). ASCII only.

usage: python -I import_closure.py <package root> <file relative to root> [<file> ...]
Lists every import statement (top-level and lazy) of each file, classifies it as stdlib, as a module the package
carries under one of the search roots the resident installs (resident_main.py and resident_installed.py), or as
ABSENT from the package. Prints one JSON document.
"""
import ast
import json
import os
import sys

ROOT = sys.argv[1]
FILES = sys.argv[2:]
# the search roots the installed resident puts on sys.path (resident_main.py: intake, ops, reports, _keys, _authz,
# _gate, ycharts/session, ycharts/extract; resident_installed.py adds _scope, _ids, _contracts, lib) plus the package root
SEARCH = ["", "intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract",
          "_scope", "_ids", "_contracts", "lib", "ycharts", "ycharts/generate", "ycharts/research"]
STDLIB = set(sys.stdlib_module_names)


def resolves(top, dotted):
    parts = dotted.split(".")
    for base in SEARCH:
        path = os.path.join(ROOT, *(base.split("/") if base else []), *parts)
        if os.path.isfile(path + ".py") or os.path.isfile(os.path.join(path, "__init__.py")) or os.path.isdir(path):
            return os.path.relpath(path, ROOT).replace(os.sep, "/")
    return None


report = {}
for rel in FILES:
    text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    tree = ast.parse(text)
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                rows.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                rows.append((node.lineno, "RELATIVE:" + "." * node.level + (node.module or "")))
            elif node.module:
                rows.append((node.lineno, node.module))
    out = []
    for lineno, name in sorted(rows):
        if name.startswith("RELATIVE:"):
            out.append({"line": lineno, "module": name, "class": "relative"})
            continue
        top = name.split(".")[0]
        if top in STDLIB:
            out.append({"line": lineno, "module": name, "class": "stdlib"})
            continue
        hit = resolves(top, name)
        out.append({"line": lineno, "module": name, "class": "in_package" if hit else "ABSENT", "where": hit})
    report[rel] = sorted(out, key=lambda r: r["line"])
print(json.dumps(report, indent=1))
