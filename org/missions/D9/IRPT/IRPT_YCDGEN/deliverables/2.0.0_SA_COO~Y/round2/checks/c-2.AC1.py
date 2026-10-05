"""IRPT_YCDGEN round 2 check c-2.AC1 (YCD-c-2). Run from the repository root. Prints 'c-2.AC1 RESULT: PASS|FAIL <why>'."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("c-2.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
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


IDS = ['p12.e04', 'p2.e08', 'p2.e09', 'p2.e10', 'p2.e11', 'p2.e12', 'p2.e13', 'p2.e14', 'p2.e15', 'p2.e20', 'p2.e21', 'p2.e22', 'p2.e23', 'p2.e24', 'p2.e25', 'p2.e26', 'p3.e02', 'p3.e03', 'p3.e04', 'p3.e05', 'p3.e06', 'p3.e07', 'p3.e09', 'p3.e10', 'p3.e11', 'p3.e12', 'p3.e13', 'p3.e14', 'p3.e15', 'p3.e16', 'p3.e17', 'p3.e19', 'p3.e20', 'p3.e21', 'p3.e22', 'p3.e23', 'p4.e01', 'p4.e02', 'p4.e03', 'p4.e04', 'p4.e05', 'p4.e06', 'p4.e07', 'p4.e08', 'p4.e09', 'p4.e10', 'p4.e11', 'p4.e12', 'p4.e13', 'p4.e14', 'p4.e15', 'p4.e16', 'p4.e17', 'p4.e18', 'p4.e19', 'p4.e20', 'p4.e21', 'p4.e22', 'p4.e23', 'p4.e24', 'p4.e25', 'p4.e26', 'p4.e27', 'p4.e28', 'p4.e29', 'p4.e30', 'p4.e31', 'p4.e32', 'p4.e33', 'p4.e34', 'p4.e35', 'p4.e36', 'p4.e37', 'p4.e38', 'p4.e39', 'p4.e40', 'p4.e41', 'p4.e42', 'p4.e43', 'p4.e44', 'p4.e45', 'p4.e46', 'p4.e47', 'p4.e48', 'p4.e49', 'p4.e50', 'p4.e51', 'p4.e52', 'p4.e53', 'p4.e54', 'p4.e55', 'p4.e56', 'p4.e57', 'p4.e58', 'p4.e59', 'p4.e60', 'p4.e61', 'p4.e62', 'p5.e02', 'p5.e03', 'p5.e04', 'p5.e05', 'p5.e06', 'p5.e07', 'p5.e08', 'p5.e09', 'p5.e10', 'p5.e11', 'p5.e12', 'p5.e13', 'p5.e14', 'p5.e15', 'p5.e17', 'p5.e18', 'p5.e19', 'p5.e20', 'p5.e21', 'p5.e22', 'p5.e23', 'p5.e25', 'p5.e26', 'p5.e27', 'p5.e28', 'p5.e29', 'p5.e30', 'p5.e31', 'p5.e32', 'p6.e02', 'p6.e03', 'p6.e04', 'p6.e05', 'p6.e06', 'p6.e07', 'p6.e08', 'p6.e09', 'p6.e10', 'p6.e11', 'p6.e12', 'p6.e13', 'p6.e14', 'p6.e15', 'p6.e16', 'p6.e17', 'p6.e18', 'p6.e22', 'p7.e02', 'p7.e03', 'p7.e04', 'p7.e05', 'p7.e06', 'p7.e07', 'p7.e08', 'p7.e10', 'p7.e11', 'p7.e12', 'p7.e13', 'p8.e02', 'p8.e03', 'p8.e04', 'p8.e05', 'p8.e06', 'p8.e07', 'p8.e08', 'p8.e09', 'p8.e10', 'p8.e11', 'p8.e12', 'p8.e13', 'p8.e14', 'p8.e15', 'p8.e16', 'p8.e17', 'p8.e18', 'p8.e19', 'p8.e20', 'p8.e21']
CLASSES = {"HELD_DATA", "OTHER_ENDPOINT", "BUILDER_ONLY"}
path = MAPS / "overview_coverage.json"
if not path.is_file():
    verdict(False, "absent: " + path.relative_to(ROOT).as_posix())
doc = json.loads(path.read_text(encoding="utf-8"))
rows = doc.get("elements", [])
got = [r.get("id") for r in rows]
bad = [r.get("id") for r in rows if r.get("class") not in CLASSES or not str(r.get("reason") or "").strip()]
probe = MAPS / "coverage_probe_map.json"
calls = {c.get("name") for c in json.loads(probe.read_text(encoding="utf-8")).get("calls", [])} if probe.is_file() else set()
dangling = [r.get("id") for r in rows if r.get("class") == "OTHER_ENDPOINT" and (r.get("via") or {}).get("call") not in calls]
ok = (doc.get("schema") == "irpt-ycdgen-coverage-v1" and sorted(got) == sorted(IDS) and len(got) == len(set(got))
      and not bad and not dangling)
verdict(ok, "schema=%s ids=%d/%d exact=%s bad=%s dangling=%s" % (doc.get("schema"), len(set(got) & set(IDS)), len(IDS),
        sorted(got) == sorted(IDS), bad[:5], dangling[:5]))
