"""c6_tools.py -- MX-c-6 AC3 instrument: every tool a `needs:` entry names is a tool the gateway classifies, so no
entry points at a name that does not exist (C2, C3).

The registered set is the gateway's OWN classified set, `TOOL_CLASSES` in app/data_entitlement.py: the string members
of its NATIVE_TOOLS, INTEGRATION_TOOLS, INDEX_TOOLS and SCHWAB_TOOLS frozensets, read by AST (no import, no env). A need
with tool null is not counted. Offline, read-only.
Usage: python c6_tools.py <gateway_root>
"""
import ast
import os
import sys

import yaml

gw = sys.argv[1]
SETS = ("NATIVE_TOOLS", "INTEGRATION_TOOLS", "INDEX_TOOLS", "SCHWAB_TOOLS")
reg, seen = set(), set()
tree = ast.parse(open(os.path.join(gw, "app", "data_entitlement.py"), encoding="utf-8").read())
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in SETS for t in node.targets):
        seen |= {t.id for t in node.targets if isinstance(t, ast.Name)}
        for sub in ast.walk(node.value):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                reg.add(sub.value)
cat = yaml.safe_load(open(os.path.join(gw, "app", "refs", "DATA_CATALOG.yaml"), encoding="utf-8"))
named = [(str(n.get("id")), str(n["tool"])) for n in (cat.get("needs") or [])
         if isinstance(n, dict) and n.get("tool")]
unknown = [(i, t) for i, t in named if t not in reg]
for i, t in unknown:
    print("UNKNOWN: %s names %s" % (i, t))
print("classified tool sets read %d of %d; registered tools %d; needs naming a tool %d; unknown %d"
      % (len(seen), len(SETS), len(reg), len(named), len(unknown)))
sys.exit(0 if len(seen) == len(SETS) and named and not unknown else 1)
