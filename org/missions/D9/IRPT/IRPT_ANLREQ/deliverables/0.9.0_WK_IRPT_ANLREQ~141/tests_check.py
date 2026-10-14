"""AR333-y-AC1: run the new r31 source test file and the neighbouring resident/producer/bindings/installed/build tests.

Prints TESTS-OK only when the new file has every case it defines passing (0 skipped) and every other file has 0 failed
and 0 errors. Otherwise prints TESTS-BAD <why> and exits 1. ASCII only.
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # the worktree: deliverables/<serial> -> deliverables -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> ROOT
PKG = ROOT / "infra/aws/lambda/investor-reporting"
NEW = PKG / "reports/tests/test_resident_r31_source.py"
NAMES = ("resident", "producer", "bindings", "installed", "build")
SUMMARY = re.compile(r"(\d+) (passed|failed|errors?|skipped)")


def bad(why):
    print("TESTS-BAD " + why)
    sys.exit(1)


def run(files):
    cmd = [sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider"] + [str(f) for f in files]
    proc = subprocess.run(cmd, cwd=str(PKG), capture_output=True, text=True, timeout=900)
    lines = [ln for ln in (proc.stdout + proc.stderr).splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    for number, kind in SUMMARY.findall(lines[-1] if lines else ""):
        counts["errors" if kind.startswith("error") else kind] += int(number)
    return proc.returncode, counts, lines[-1] if lines else "(no summary line)"


def case_count(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return sum(1 for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))


if not NEW.is_file():
    bad("NEW_FILE_ABSENT " + str(NEW))
new_cases = case_count(NEW)
rc_new, new_counts, new_line = run([NEW])
print("NEW FILE " + str(NEW.relative_to(ROOT)) + " cases=" + str(new_cases) + " :: " + new_line)
if new_counts["passed"] != new_cases or new_counts["failed"] or new_counts["errors"] or new_counts["skipped"]:
    bad("NEW_NOT_ALL_PASSING passed=%d of %d failed=%d errors=%d skipped=%d" % (
        new_counts["passed"], new_cases, new_counts["failed"], new_counts["errors"], new_counts["skipped"]))

others = []
for folder in (PKG / "ycharts/generate/tests", PKG / "reports/tests"):
    for path in sorted(folder.glob("test_*.py")):
        if path == NEW:
            continue
        if any(token in path.name for token in NAMES):
            others.append(path)
print("OTHER TEST FILES (%d), one pytest process each (a shared process hits the pre-existing 'entry' module collision):"
      % len(others))
o_total = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
for path in others:
    rc_o, o_counts, o_line = run([path])
    print("  " + str(path.relative_to(ROOT)).replace("\\", "/") + " :: " + o_line)
    for key in o_total:
        o_total[key] += o_counts[key]
print("OTHERS TOTAL passed=%d failed=%d errors=%d skipped=%d" % (
    o_total["passed"], o_total["failed"], o_total["errors"], o_total["skipped"]))
if o_total["failed"] or o_total["errors"]:
    bad("OTHERS_FAILED failed=%d errors=%d" % (o_total["failed"], o_total["errors"]))
print("TESTS-OK %d new, %d others, 0 failed" % (new_counts["passed"], o_total["passed"]))
sys.exit(0)
