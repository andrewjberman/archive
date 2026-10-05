"""IRPT_YCDGEN round 5 check h-5.AC1 (YCD-h-5). Run from the repository root. Prints 'h-5.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("h-5.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


cov = json.loads((MAPS / "overview_coverage.json").read_text(encoding="utf-8"))
held = [r for r in cov.get("elements", []) if r.get("class") == "HELD_DATA"]
bad = []
for r in held:
    f = r.get("feed") or {}
    if f.get("source") == "OPAL_HELD" and all(f.get(k) for k in ("table", "field", "key", "method")):
        continue
    if f.get("source") == "NOT_HELD" and str(f.get("reason") or "").strip():
        continue
    bad.append(r.get("id"))
from collections import Counter  # noqa: E402
counts = Counter((r.get("feed") or {}).get("source") for r in held)
verdict(bool(held) and not bad, "held=%d feeds=%s not 5.2-shaped=%d %s" % (len(held), dict(counts), len(bad), bad[:5]))
