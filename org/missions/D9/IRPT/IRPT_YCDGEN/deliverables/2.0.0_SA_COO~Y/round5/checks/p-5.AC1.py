"""IRPT_YCDGEN round 5 check p-5.AC1 (YCD-p-5). Run from the repository root. Prints 'p-5.AC1 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("p-5.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)
sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(RESEARCH.parent / "session"))
sys.path.insert(0, str(RESEARCH.parent / "generate"))
sys.path.insert(0, str(ROOT / "lib"))


import runner  # noqa: E402
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
holdings = {"source_request": "REQ-x", "basis": "USD",
            "rows": [{"ticker": "T%02d" % i, "amount": "1"} for i in range(99)]}
planned = runner.plan_calls(doc, "P:1", {"start": "", "end": ""}, holdings=holdings)
read = {e["source"].get("call") for e in doc["elements"] if isinstance(e.get("source"), dict)}
unread = [c["name"] for c in doc["calls"] if c["name"] not in read]
verdict(1 <= len(planned) <= 12 and not unread,
        "overview_map plans %d requests for 99 holdings (need 1..12); calls read by no element: %d %s" % (
            len(planned), len(unread), unread[:5]))
