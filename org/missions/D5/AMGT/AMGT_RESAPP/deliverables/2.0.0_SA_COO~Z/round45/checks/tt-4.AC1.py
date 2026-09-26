"""AMGT_RESAPP round 45, AMGT-tt-4 AC1 -- the fourteen unmarked and the nine carried rows, measured.
Reads deliverables/0.9.0_WK_AMGT_RESAPP~165/CARRIED_ROWS.json: {"rows": [...]}, one per id of the 22 below, W130-S1 FIRST. Each row
carries id, disposition (must equal what .tools/surprise-row-gate.py's _latest_dispositions reads for it NOW), owner, closes_when
(one sentence), and, for every row whose disposition is not terminal, measured_now {command, rc, excerpt} -- the row's own claim
re-run against the world today. usage (repo root): python <this>"""
import importlib.util
import json
import sys
from pathlib import Path

P = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~165/CARRIED_ROWS.json")
UNMARKED = ["W130-S1", "W135-S1", "W136-S1", "W137-S1", "W137-S2", "W138-S1", "W140-S1", "W140-S2", "W141-S1", "W144-S1",
            "W146-S1", "W148-S1", "W150-S1", "W152-S1"]
CARRIED = ["Z-S236", "Z-S237", "Z-S238", "Z-S248", "Z-S251", "Z-S255", "Z-W158-S1", "Z-S276", "W130-S1"]
WANT = list(dict.fromkeys("AMGT_RESAPP-" + x for x in UNMARKED + CARRIED))
TERMINAL = {"GRADUATED", "DISMISSED_WITH_REASON"}
spec = importlib.util.spec_from_file_location("srg", ".tools/surprise-row-gate.py")
srg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srg)
latest, _unknown, nfiles, note = srg._latest_dispositions(".", "AMGT_RESAPP")
if latest is None:
    print("FAIL: the resolver could not run: %s" % note)
    sys.exit(1)
if not P.exists():
    print("FAIL: no table at %s (resolver read %d files, %d items)" % (P, nfiles, len(latest)))
    sys.exit(1)
rows = json.loads(P.read_text(encoding="utf-8")).get("rows") or []
ids = [r.get("id") for r in rows]
bad = []
if not rows or ids[0] != "AMGT_RESAPP-W130-S1":
    bad.append("the first row is %r, not AMGT_RESAPP-W130-S1" % (ids[0] if ids else None))
for r in rows:
    i = r.get("id")
    if r.get("disposition") != latest.get(i):
        bad.append("%s: disposition %r, resolver reads %r" % (i, r.get("disposition"), latest.get(i)))
    for f in ("owner", "closes_when"):
        if not str(r.get(f) or "").strip():
            bad.append("%s: %s empty" % (i, f))
    if latest.get(i) not in TERMINAL:
        mn = r.get("measured_now") or {}
        if not str(mn.get("command") or "").strip() or not isinstance(mn.get("rc"), int):
            bad.append("%s: open row with no measured_now command+rc" % i)
open_n = sum(1 for i in WANT if latest.get(i) not in TERMINAL)
print("rows %d of %d; missing %s; extra %s; open by the resolver %d; defects %d (resolver: %d files, %d items)" % (
    len(set(ids) & set(WANT)), len(WANT), sorted(set(WANT) - set(ids)), sorted(set(ids) - set(WANT)), open_n, len(bad), nfiles, len(latest)))
for b in bad[:12]:
    print("  " + b)
sys.exit(0 if set(ids) == set(WANT) and len(ids) == len(WANT) and not bad else 1)
