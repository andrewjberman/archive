"""IRPT_YCDGEN round 5 check m-5.AC1 (YCD-m-5). Run from the repository root. Prints 'm-5.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("m-5.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


placeholders, nodata = [], False
for name in ("comparison_map.json", "multi_map.json"):
    doc = json.loads((MAPS / name).read_text(encoding="utf-8"))
    for e in doc["elements"]:
        label = str(e.get("label") or "").strip()
        if label == "row" or label.endswith(": row"):
            placeholders.append("%s:%s" % (name.split("_")[0], e["id"]))
        if name == "multi_map.json" and e.get("page") == 9 and "no data available" in (
                label + " " + str(e.get("note") or "")).lower():
            nodata = True
verdict(not placeholders and nodata, "placeholder 'row' labels: %d %s; Multi p9 'No data available' row listed: %s" % (
    len(placeholders), placeholders[:7], nodata))
