"""IRPT_YCDGEN round 4 check o-4.AC2 (YCD-o-4). Run from the repository root. Prints 'o-4.AC2 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("o-4.AC2 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(RESEARCH.parent / "session"))
sys.path.insert(0, str(RESEARCH.parent / "generate"))
sys.path.insert(0, str(ROOT / "lib"))
path = MAPS / "feed_probe_map.json"
if not path.is_file():
    verdict(False, "absent: " + path.relative_to(ROOT).as_posix())
import runner  # noqa: E402
doc = json.loads(path.read_text(encoding="utf-8"))
holdings = {"source_request": "REQ-x", "basis": "USD",
            "rows": [{"ticker": "T%02d" % i, "amount": "1"} for i in range(99)]}
try:
    planned = runner.plan_calls(doc, "P:1", {"start": "", "end": ""}, holdings=holdings)
except (ValueError, TypeError) as exc:
    verdict(False, "plan_calls refused: %s" % exc)
verdict(doc.get("schema") == "irpt-ycdgen-map-v1" and 1 <= len(planned) <= 6,
        "schema=%s requests planned for 99 holdings=%d (need 1..6)" % (doc.get("schema"), len(planned)))
