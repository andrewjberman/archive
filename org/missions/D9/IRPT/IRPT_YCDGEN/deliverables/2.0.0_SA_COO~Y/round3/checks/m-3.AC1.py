"""IRPT_YCDGEN round 3 check m-3.AC1 (YCD-m-3). Run from the repository root. Prints 'm-3.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("m-3.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)




bad = []
for name, kind in (("comparison_map.json", "COMPARISON"), ("multi_map.json", "MULTI")):
    path = MAPS / name
    if not path.is_file():
        verdict(False, "absent: " + path.relative_to(ROOT).as_posix())
    doc = json.loads(path.read_text(encoding="utf-8"))
    pages = int((doc.get("source_pdf") or {}).get("pages") or 0)
    seen = {e.get("page") for e in doc.get("elements", [])}
    missing = [p for p in range(1, pages + 1) if p not in seen]
    if doc.get("schema") != "irpt-ycdgen-map-v1" or doc.get("report_type") != kind or pages < 1 or missing:
        bad.append((name, doc.get("report_type"), pages, missing[:5]))
verdict(not bad, "maps: %s" % (bad or "both present, every page of each source PDF holds an element"))
