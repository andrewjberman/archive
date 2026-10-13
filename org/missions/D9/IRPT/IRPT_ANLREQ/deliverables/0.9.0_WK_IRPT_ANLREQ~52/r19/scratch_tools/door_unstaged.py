"""Every top-level import in the door closure that is neither stdlib, nor a staged flat module, nor a known third-party package.

Usage: python door_unstaged.py <scratch_root>
"""
import ast
import json
import os
import sys

SCR = sys.argv[1]
FLAT = os.path.join(SCR, "lambda_flat")
man = json.load(open(os.path.join(SCR, "tools", "tree_manifest.json"), encoding="utf-8"))
flat = set(p[:-3] for p in os.listdir(FLAT) if p.endswith(".py"))
stdlib = set(sys.stdlib_module_names)
third_party = {"boto3", "botocore", "jsonschema", "pyarrow", "pdfminer", "pdfplumber"}
leftover = {}
seen = {}
for member in man["door_closure"]:
    tree = ast.parse(open(os.path.join(FLAT, member), encoding="utf-8", errors="replace").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods = [node.module]
        else:
            continue
        for mod in mods:
            top = mod.split(".")[0]
            if top in flat or top in stdlib:
                continue
            if top in third_party:
                seen.setdefault(top, set()).add(member)
                continue
            leftover.setdefault(top, set()).add("%s:%d" % (member, node.lineno))
print("door closure members: %d" % len(man["door_closure"]))
print("third-party imports reached from the closure (module -> members): %s" % {k: sorted(v) for k, v in sorted(seen.items())})
print("UNSTAGED, non-stdlib, non-third-party imports in the closure: %s" % (sorted(leftover.items()) or "none"))
