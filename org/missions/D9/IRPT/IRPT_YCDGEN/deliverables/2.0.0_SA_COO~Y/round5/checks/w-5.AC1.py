"""IRPT_YCDGEN round 5 check w-5.AC1 (YCD-w-5). Run from the repository root. Prints 'w-5.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("w-5.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


cov = json.loads((MAPS / "overview_coverage.json").read_text(encoding="utf-8"))
ids = [r.get("id") for r in cov.get("elements", []) if r.get("class") == "HELD_DATA"]
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
by_id = {e["id"]: e for e in doc["elements"]}
bad = [i for i in ids if not (isinstance((by_id.get(i) or {}).get("source"), dict)
                              and by_id[i]["source"].get("computed") == "OPAL_HELD" and by_id[i]["source"].get("group"))]
verdict(bool(ids) and not bad, "HELD_DATA elements sourced OPAL_HELD with a group: %d of %d; not: %s" % (
    len(ids) - len(bad), len(ids), bad[:5]))
