"""IRPT_YCDGEN round 5 check p-5.AC3 (YCD-p-5). Run from the repository root. Prints 'p-5.AC3 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("p-5.AC3 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


WANT = {"p7.e02": "alpha_", "p7.e03": "beta_", "p7.e05": "sharpe_", "p7.e06": "sortino_",
        "p7.e07": "max_drawdown_", "p7.e08": "var_monthly_"}
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
by_id = {e["id"]: e for e in doc["elements"]}
bad = []
for eid, prefix in WANT.items():
    src = (by_id.get(eid) or {}).get("source")
    if not isinstance(src, dict) or not src.get("statistic") or not src.get("columns") or not all(
            str(c).startswith(prefix) for c in src["columns"]):
        bad.append(eid)
verdict(not bad, "p7 statistic elements wired to 4.3 ids: %d of 6; not: %s" % (6 - len(bad), bad))
