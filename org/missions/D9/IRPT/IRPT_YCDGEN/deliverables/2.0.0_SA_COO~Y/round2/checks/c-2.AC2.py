"""IRPT_YCDGEN round 2 check c-2.AC2 (YCD-c-2). Run from the repository root. Prints 'c-2.AC2 RESULT: PASS|FAIL <why>'."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("c-2.AC2 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


def pytest_k(test_file, keyword, minimum):
    path = RESEARCH / "tests" / test_file
    if not path.is_file():
        verdict(False, "absent: %s" % path.relative_to(ROOT).as_posix())
    args = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", str(path)]
    if keyword:
        args += ["-k", keyword]
    out = subprocess.run(args, capture_output=True, text=True, timeout=110)
    tail = (out.stdout.strip().splitlines() or [""])[-1]
    passed = int((re.search(r"(\d+) passed", tail) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", tail) or [0, 0])[1]) + int((re.search(r"(\d+) error", tail) or [0, 0])[1])
    return out.returncode == 0 and failed == 0 and passed >= minimum, "%d passed, %d failed (need >= %d, -k %r): %s" % (
        passed, failed, minimum, keyword, tail[:140])


sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(RESEARCH.parent / "session"))
sys.path.insert(0, str(RESEARCH.parent / "generate"))
sys.path.insert(0, str(ROOT / "lib"))
path = MAPS / "coverage_probe_map.json"
if not path.is_file():
    verdict(False, "absent: " + path.relative_to(ROOT).as_posix())
import runner  # noqa: E402
doc = json.loads(path.read_text(encoding="utf-8"))
try:
    planned = runner.plan_calls(doc, "P:1", {"start": "", "end": ""})
except ValueError as exc:
    verdict(False, "plan_calls refused: %s" % exc)
verdict(doc.get("schema") == "irpt-ycdgen-map-v1" and len(planned) >= 1,
        "schema=%s planned=%d (GET or the admitted POST only)" % (doc.get("schema"), len(planned)))
