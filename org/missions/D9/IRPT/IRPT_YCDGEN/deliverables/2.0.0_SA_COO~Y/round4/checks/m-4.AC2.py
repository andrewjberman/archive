"""IRPT_YCDGEN round 4 check m-4.AC2 (YCD-m-4). Run from the repository root. Prints 'm-4.AC2 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("m-4.AC2 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


NEED = {"comparison_map.json": 552 + 21, "multi_map.json": 394 + 29}
got = {}
for name, need in NEED.items():
    doc = json.loads((MAPS / name).read_text(encoding="utf-8"))
    got[name] = len(doc.get("elements", []))
verdict(all(got[n] >= need for n, need in NEED.items()), "elements %s (need comparison >= 573, multi >= 423)" % got)
