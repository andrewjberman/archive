"""IRPT_YCDGEN round 3 check w-3.AC1 (YCD-w-3). Run from the repository root. Prints 'w-3.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("w-3.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)




METHODS = {"WEIGHTED_MEAN", "WEIGHTED_MEAN_SLEEVE", "HARMONIC_WEIGHTED_MEAN", "SUM", "BUY_AND_HOLD", "OWN_SERIES"}
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
cov = json.loads((MAPS / "overview_coverage.json").read_text(encoding="utf-8"))
calls = {c["name"]: c for c in doc["calls"]}
expand = {n for n, c in calls.items() if isinstance(c.get("expand"), dict) and c["expand"].get("over") == "holdings"}
src = {e["id"]: e.get("source") for e in doc["elements"]}
classes = {}
for r in cov["elements"]:
    classes.setdefault(r["class"], []).append(r["id"])
bad = []
for i in classes.get("HELD_DATA", []):
    s = src.get(i)
    if not (isinstance(s, dict) and s.get("computed") in METHODS - {"OWN_SERIES"} and s.get("call") in expand):
        bad.append(i)
for i in classes.get("OWN_SERIES", []):
    s = src.get(i)
    if not (isinstance(s, dict) and s.get("computed") == "OWN_SERIES" and s.get("call") in calls):
        bad.append(i)
for i in classes.get("OTHER_ENDPOINT", []):
    s = src.get(i)
    if not (isinstance(s, dict) and s.get("call") in calls and not s.get("computed")):
        bad.append(i)
ids = [r["id"] for r in cov["elements"]]
ok = (len(expand) >= 2 and bool(classes.get("OWN_SERIES")) and not bad and len(ids) == len(set(ids)) == 176)
verdict(ok, "expand calls=%d own_series=%d held=%d other=%d unwired=%d %s rows=%d" % (
    len(expand), len(classes.get("OWN_SERIES", [])), len(classes.get("HELD_DATA", [])), len(classes.get("OTHER_ENDPOINT", [])),
    len(bad), bad[:5], len(ids)))
