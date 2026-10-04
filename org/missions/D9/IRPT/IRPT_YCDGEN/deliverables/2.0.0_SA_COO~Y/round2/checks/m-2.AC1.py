"""IRPT_YCDGEN round 2 check m-2.AC1 (YCD-m-2). Run from the repository root. Prints 'm-2.AC1 RESULT: PASS|FAIL <why>'."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("m-2.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
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


WANT = [(3, "stock style"), (3, "market classification"), (3, "region"), (5, "stock sector")]
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
charts = [(e["page"], e["label"].lower()) for e in doc["elements"] if e.get("kind") == "chart"]
missing = [w for w in WANT if not any(p == w[0] and w[1] in label for p, label in charts)]
verdict(not missing, "chart elements missing: %s (charts on p3/p5: %d)" % (missing, sum(1 for p, _ in charts if p in (3, 5))))
