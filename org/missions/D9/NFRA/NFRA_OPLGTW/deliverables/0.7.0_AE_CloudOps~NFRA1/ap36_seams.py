#!/usr/bin/env python
"""OG-ap-36 Phase A step 2 prep: seam enumeration (read-only). Every app/lib module a taken app file imports (and every app module a taken TEST imports),
printed as IN-TAKE-LIST / IN-BASE(identical to trunk) / IN-BASE(differs, not taken: STOP-class) / ABSENT-AT-BASE(STOP-class).
usage: python ap28_seams.py <live_ref> <trunk_sha> <out.json>   (repository root)"""
from __future__ import annotations

import ast
import json
import subprocess
import sys

LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
APP = ["tools", "client_core", "client_adapter_bd49f"]
TESTS = ["test_og_en21", "test_og_en22", "test_og_en23", "test_og_en24", "test_og_db3"]
take = {G + "app/%s.py" % m for m in APP}
tests = {G + "tests/%s.py" % t for t in TESTS}


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


trunk_files = ls(TRUNK, G + "app/") | ls(TRUNK, G + "tests/") | {"lib/trading_calendar.py", "lib/opal_naming.py"}
live_files = ls(LIVE, G + "app/") | ls(LIVE, G + "tests/") | {"lib/trading_calendar.py", "lib/opal_naming.py"}
absent_tests = sorted(t for t in tests if t not in trunk_files)
tests_present = {t for t in tests if t in trunk_files}


def imports_of(p, src):
    tree = ast.parse(src)
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name)
        elif isinstance(n, ast.ImportFrom):
            base = ("." * n.level) + (n.module or "")
            if n.module is None or n.level:
                for a in n.names:
                    mods.add(base + a.name)
            else:
                mods.add(n.module)
                for a in n.names:
                    mods.add(n.module + "." + a.name)
    out = []
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
        hit = next((c for c in cand if c in trunk_files), None)
        if hit:
            out.append(hit)
    return sorted(set(out))


rows, stop = [], []
for p in sorted(take | tests_present):
    if not p.endswith(".py"):
        continue
    src = blob(TRUNK, p)
    if src is None:
        continue
    for hit in imports_of(p, src):
        if hit in take:
            cls = "IN-TAKE-LIST"
        elif hit in live_files and blob(LIVE, hit) == blob(TRUNK, hit):
            cls = "IN-BASE (identical to trunk)"
        elif hit == "lib/trading_calendar.py":
            cls = "IN-BASE (differs from trunk; the base's calendar ships)"
        elif hit in live_files:
            cls = "IN-BASE (DIFFERS from trunk, not named) -> STOP"
            stop.append((p.replace(G, ""), hit.replace(G, "")))
        else:
            cls = "ABSENT-AT-BASE and not in take-list -> STOP"
            stop.append((p.replace(G, ""), hit.replace(G, "")))
        rows.append((p.replace(G, ""), hit.replace(G, ""), cls))

seen = {}
for r in rows:
    seen.setdefault((r[1], r[2]), []).append(r[0])
print("take: %d app/ref files, %d test files named (%d present at trunk); trunk=%s live=%s" % (len(take), len(tests), len(tests_present), TRUNK[:10], LIVE[:10]))
print("named tests ABSENT at trunk: %s" % (absent_tests or "none"))
for (hit, cls), by in sorted(seen.items()):
    print("  seam %-52s %-58s (imported by %d)" % (hit, cls, len(by)))
print("importer-edges: %d, distinct seams: %d" % (len(rows), len(seen)))
unnamed = []
for p in sorted(trunk_files):
    if not p.startswith(G + "app/") or p in take:
        continue
    a, b = blob(LIVE, p), blob(TRUNK, p)
    if a != b:
        unnamed.append((p.replace(G, ""), "absent-at-live" if a is None else "changed"))
print("app files that differ live->trunk and are NOT taken (%d):" % len(unnamed))
for p, w in unnamed:
    print("  %s  [%s]" % (p, w))
print("STOP-class edges: %d" % len(stop))
for s in stop:
    print("  STOP", s)
json.dump({"trunk": TRUNK, "live": LIVE, "stop": stop, "absent_tests": absent_tests, "unnamed_differing": unnamed, "edges": len(rows), "distinct": len(seen)}, open(OUT, "w"), indent=1)
