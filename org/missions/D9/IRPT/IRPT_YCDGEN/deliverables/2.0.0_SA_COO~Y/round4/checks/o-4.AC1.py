"""IRPT_YCDGEN round 4 check o-4.AC1 (YCD-o-4). Run from the repository root. Prints 'o-4.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("o-4.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


SOURCES = {"OPAL_HELD", "YCHARTS_SECURITY", "NONE"}
cov = json.loads((MAPS / "overview_coverage.json").read_text(encoding="utf-8"))
probe_path = MAPS / "feed_probe_map.json"
calls = {c.get("name") for c in json.loads(probe_path.read_text(encoding="utf-8")).get("calls", [])} if probe_path.is_file() else set()
held = [r for r in cov.get("elements", []) if r.get("class") == "HELD_DATA"]
bad = []
for r in held:
    f = r.get("feed")
    if not isinstance(f, dict) or f.get("source") not in SOURCES:
        bad.append(r.get("id"))
    elif f["source"] == "OPAL_HELD" and not (f.get("table") and f.get("field") and f.get("key")):
        bad.append(r.get("id"))
    elif f["source"] == "YCHARTS_SECURITY" and f.get("call") not in calls:
        bad.append(r.get("id"))
    elif f["source"] == "NONE" and not str(f.get("reason") or "").strip():
        bad.append(r.get("id"))
from collections import Counter  # noqa: E402
counts = Counter((r.get("feed") or {}).get("source") for r in held)
verdict(bool(held) and not bad, "held=%d feeds=%s unfed/bad=%d %s" % (len(held), dict(counts), len(bad), bad[:5]))
