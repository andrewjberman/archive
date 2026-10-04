"""IRPT_YCDGEN round 1 check m-1.AC1 (YCD-m-1). Run from the repository root. Prints 'm-1.AC1 RESULT: PASS|FAIL <why>'."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"


def verdict(ok, why):
    print("m-1.AC1 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


def pytest_count(test_file, minimum):
    path = RESEARCH / "tests" / test_file
    if not path.is_file():
        verdict(False, "absent: %s" % path.relative_to(ROOT).as_posix())
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(path)],
                         capture_output=True, text=True, timeout=110)
    tail = (out.stdout.strip().splitlines() or [""])[-1]
    passed = int((re.search(r"(\d+) passed", tail) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", tail) or [0, 0])[1]) + int((re.search(r"(\d+) error", tail) or [0, 0])[1])
    verdict(out.returncode == 0 and failed == 0 and passed >= minimum, "%d passed, %d failed (need >= %d): %s" % (
        passed, failed, minimum, tail[:160]))

path = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"
if not path.is_file():
    verdict(False, "absent: overview_map.json")
doc = json.loads(path.read_text(encoding="utf-8"))
calls = {c.get("name") for c in doc.get("calls") or []}
els = doc.get("elements") or []
pages = (doc.get("source_pdf") or {}).get("pages")
bad = []
if doc.get("schema") != "irpt-ycdgen-map-v1" or doc.get("template_id") != "14141822":
    bad.append("schema/template")
if not calls or not els or not isinstance(pages, int) or pages < 1:
    bad.append("empty calls, elements or pages")
ids = [e.get("id") for e in els]
if len(set(ids)) != len(ids):
    bad.append("duplicate ids")
for e in els:
    src = e.get("source")
    if not (src == "BUILDER_ONLY" or (isinstance(src, dict) and src.get("call") in calls and src.get("field"))):
        bad.append("source of %s" % e.get("id"))
    if e.get("kind") not in ("number", "table", "chart", "text") or e.get("claim") not in ("inferred", "measured"):
        bad.append("kind/claim of %s" % e.get("id"))
if isinstance(pages, int) and {e.get("page") for e in els} != set(range(1, pages + 1)):
    bad.append("pages without elements")
figure = re.compile(r"\$\s?\d|\d+\.\d{2,}|\d+(\.\d+)?\s?%")
def strings(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)
    elif isinstance(x, str):
        yield x
leaks = [s for s in strings(doc) if figure.search(s)]
if leaks:
    bad.append("%d figure-shaped strings" % len(leaks))
verdict(not bad, "%d elements, %d calls, %s pages; problems: %s" % (len(els), len(calls), pages, bad[:6] or "none"))
