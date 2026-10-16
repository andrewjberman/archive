#!/usr/bin/env python
"""OG-ap-23 Phase A step 2 prep: seam enumeration (read-only). Every app/lib module a taken file imports,
printed as IN-TAKE-LIST / IN-BASE(unchanged) / IN-BASE(differs, not taken: STOP-class) / MISSING."""
from __future__ import annotations

import ast
import json
import subprocess
import sys

LIVE = "d577e0e7297b3ecba183023d8374855a93f148a7"
TRUNK = sys.argv[1]
G = "infra/aws/ec2/opal-gateway/"


def git(*a):
    r = subprocess.run(["git"] + list(a), capture_output=True)
    return r.returncode, r.stdout


def ls(ref, pre):
    rc, out = git("ls-tree", "-r", "--name-only", ref, "--", pre)
    assert rc == 0
    return set(out.decode().split())


def blob(ref, p):
    rc, out = git("show", ref + ":" + p)
    return out if rc == 0 else None


trunk_files = ls(TRUNK, G + "app/") | ls(TRUNK, G + "tests/") | {"lib/opal_naming.py", "lib/trading_calendar.py"}
live_files = ls(LIVE, G + "app/") | ls(LIVE, G + "tests/") | {"lib/trading_calendar.py"}

whole = ["client_core", "client_role", "etfs_rivals", "etfs_rivals_flow", "etfs_silver", "portal_served",
         "portal_json_served", "admin_gateway_breakdown", "admin_people", "mdpf_classification"]
whole += ["client_adapter_" + n for n in
          ("schwab", "bd49f", "orion", "eclipse", "bdcottonwood", "smartx", "commonwealth")]
take = {G + "app/%s.py" % m for m in whole}
take |= {G + "app/refs/partner_roster.json", "lib/opal_naming.py"}
for t in sorted(trunk_files):
    b = t.rsplit("/", 1)[-1]
    if t.startswith(G + "tests/") and (
            (b.startswith("test_og_") and b[len("test_og_"):-3] in (
                "cl1", "cl2", "cl3", "cl4", "cl5", "cl6", "cl7", "cl8", "rv1", "rv2", "ch1", "gp1", "gf1", "sv1", "sv2", "ac2"))
            or b in (
            "test_admin_gateway_breakdown.py", "test_admin_people.py", "test_positioning_extension.py")):
        take.add(t)
hunk = {G + "app/tools.py", G + "app/destructive_ops.py", G + "app/data_entitlement.py",
        G + "tests/test_entitlement_admin.py", G + "tests/test_data_entitlement_family.py",
        G + "app/integrations/portal_index/integration.py", G + "deploy-to-ec2.sh"}

# report take paths absent at trunk (a named file that does not exist)
absent = sorted(p for p in take if p not in trunk_files and p != G + "app/refs/partner_roster.json"
                and blob(TRUNK, p) is None)

differs_unnamed = []
for p in sorted(trunk_files):
    if not p.startswith(G + "app/"):
        continue
    if p in take or p in hunk:
        continue
    a, b = blob(LIVE, p), blob(TRUNK, p)
    if a != b:
        differs_unnamed.append((p, "absent-at-live" if a is None else "changed"))

rows, stop = [], []
for p in sorted(take | hunk):
    src = blob(TRUNK, p)
    if src is None or not p.endswith(".py"):
        continue
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        stop.append((p, "syntax %s" % e))
        continue
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name)
        elif isinstance(n, ast.ImportFrom):
            base = ("." * n.level) + (n.module or "")
            if n.module is None or n.level:
                for a in n.names:
                    mods.add(base + a.name if not base.endswith(".") else base + a.name)
            else:
                mods.add(n.module)
                for a in n.names:
                    mods.add(n.module + "." + a.name)
    for m in sorted(mods):
        mm = m.lstrip(".")
        cand = []
        if mm.startswith("app."):
            cand = [G + mm.replace(".", "/") + ".py", G + mm.replace(".", "/") + "/__init__.py"]
        elif m.startswith("."):
            d = p.rsplit("/", 1)[0]
            cand = [d + "/" + mm.replace(".", "/") + ".py", d + "/" + mm.replace(".", "/") + "/__init__.py"]
        elif mm.split(".")[0] == "lib":
            cand = [mm.replace(".", "/") + ".py"]
        if not cand:
            continue
        hit = next((c for c in cand if c in trunk_files), None)
        if hit is None:
            continue  # attribute import off a module (app.x.name) or a stdlib/3rd-party: no file
        if hit in take or hit in hunk:
            cls = "IN-TAKE-LIST"
        elif hit in live_files and blob(LIVE, hit) == blob(TRUNK, hit):
            cls = "IN-BASE (identical to trunk)"
        elif hit == "lib/trading_calendar.py":
            # not taken (the base's calendar ships); safe only if every name the take files call exists at base
            cls = "IN-BASE (differs from trunk; called names prev_trading_day, trading_days_behind exist at base)"
        elif hit in live_files:
            cls = "IN-BASE (DIFFERS from trunk, not named) -> STOP"
            stop.append((p, hit))
        else:
            cls = "ABSENT-AT-BASE and not in take-list -> STOP"
            stop.append((p, hit))
        rows.append((p.replace(G, ""), hit.replace(G, ""), cls))

seen = set()
print("taken files: %d whole/test/lib/ref, %d by hunk; trunk=%s live=%s" % (len(take), len(hunk), TRUNK[:10], LIVE[:10]))
print("named take paths not found at trunk: %s" % (absent or "none"))
for r in rows:
    k = (r[1], r[2])
    if k in seen:
        continue
    seen.add(k)
    print("  seam %-48s %s" % (r[1], r[2]))
print("importer-edges: %d, distinct seams: %d" % (len(rows), len(seen)))
print("app files that differ live->trunk and are NOT named (%d):" % len(differs_unnamed))
for p, w in differs_unnamed:
    print("  %s  [%s]" % (p.replace(G, ""), w))
print("STOP-class edges: %d" % len(stop))
for s in stop:
    print("  STOP", s)
json.dump({"trunk": TRUNK, "live": LIVE, "stop": stop, "absent": absent,
           "unnamed_differing": differs_unnamed}, open(sys.argv[2], "w"), indent=1)
