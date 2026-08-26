"""Four candidate joinability numbers + the one nobody measured: ACTUAL JOINS.

CORRECTED 2026-08-26 ~15:1xZ: the instance index originally globbed
org/**/deliverables/*.json while the 147-key CEILING figure came from a BROAD
org/**/*.json sweep. Two different populations inside one report -- the ceiling
counted instances the join could not see, so ACTUAL came out 68 when it is 78.
3.0.0_SA_CVO measured 78 independently and was right. ONE INDEX, ONE POPULATION.
"""
from __future__ import annotations

import collections
import json
import pathlib
import re

ROOT = pathlib.Path(".")
DOMAIN = sorted(ROOT.glob("org/tier2_senior/*/task_orders/*.md"))
SHAPE = re.compile(r"^[A-Z][A-Z0-9_]{2,}")


def tag(t, n):
    m = re.search(r"<%s>(.*?)</%s>" % (n, n), t, re.S)
    return " ".join(m.group(1).split()) if m else ""


def attr(t):
    m = re.search(r'<task_order[^>]*\bid="([^"]+)"', t)
    return m.group(1) if m else ""


# instance index
inst = collections.defaultdict(list)
for p in ROOT.glob("org/**/*.json"):   # BROAD: instances also live outside deliverables/
    try:
        d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    if isinstance(d, dict) and d.get("to_id"):
        inst[d["to_id"]].append(p)

n_attr = n_any = n_shaped = 0
join_shaped = join_any = 0
joined_only_unshaped = []
for f in DOMAIN:
    t = f.read_text(encoding="utf-8", errors="replace")
    a, ti, i = attr(t), tag(t, "to_id"), tag(t, "id")
    if a:
        n_attr += 1
    any_id = ti or i or a
    if any_id:
        n_any += 1
    # my shipped-corrected resolver: to_id tag, else <id>/attr gated on project-code SHAPE
    shaped = ti if ti else (i or a if SHAPE.match((i or a).upper()) else "")
    if shaped:
        n_shaped += 1
        if shaped in inst:
            join_shaped += 1
    if any_id and any_id in inst:
        join_any += 1
        if not shaped or shaped not in inst:
            joined_only_unshaped.append((f.name, any_id))

n = len(DOMAIN)
print("DENOMINATOR: %d TO files (declared domain)" % n)
print()
print("FOUR CANDIDATE NUMBERS -- each answers a DIFFERENT question:")
print("  id= ATTRIBUTE only ................ %5d  %5.1f%%   (my shipped census -- wrong field)" % (n_attr, 100.0 * n_attr / n))
print("  DECLARED id of PROJECT-CODE SHAPE .. %5d  %5.1f%%   (my correction @1c4dbf6bfc)" % (n_shaped, 100.0 * n_shaped / n))
print("  ANY DECLARED id, any shape ......... %5d  %5.1f%%   (CVO's read)" % (n_any, 100.0 * n_any / n))
print("  parse_to_file non-empty ............ %5d  %5.1f%%   (TRAP: manufactures from FILENAME)" % (n, 100.0))
print()
print("THE NUMBER NONE OF US MEASURED -- joins ACTUALLY ACHIEVED against %d instance to_ids:" % len(inst))
print("  joins using SHAPE-GATED declared id . %5d  %5.1f%% of %d" % (join_shaped, 100.0 * join_shaped / n, n))
print("  joins using ANY declared id ......... %5d  %5.1f%% of %d" % (join_any, 100.0 * join_any / n, n))
print("  joins the shape gate COSTS .......... %5d" % (join_any - join_shaped))
for nm, tid in joined_only_unshaped[:10]:
    print("      %-58s id=%s" % (nm[:58], tid))
