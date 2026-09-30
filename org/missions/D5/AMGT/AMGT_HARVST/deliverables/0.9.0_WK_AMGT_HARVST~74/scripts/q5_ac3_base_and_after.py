"""HVST-q-5 AC3 helper: runs the AC3 pytest command at the pinned base ff4405d3d5 (a `git archive` extract of lib/, pytest.ini, infra/logic, org/standards, integrations/bloomberg
under .scratch/) and at this worktree's HEAD, and prints both counts and `N failed`.
Read-only over the repo apart from the temporary extract, which it removes."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "ff4405d3d5"
REPO = Path(__file__).resolve()
while not (REPO / "lib" / "research" / "harvest").is_dir():
    REPO = REPO.parent
CMD = [sys.executable, "-m", "pytest", "lib/research/harvest/tests/", "lib/research/api/tests/test_timeline_routes.py",
       "-q", "--tb=line", "-p", "no:cacheprovider"]


def run(cwd):
    out = subprocess.run(CMD, cwd=str(cwd), capture_output=True, text=True, timeout=850).stdout
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    tail = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed)", ln)][-1:]
    counts = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|error|errors|skipped)", tail[0])} if tail else {}
    return counts, (tail[0] if tail else "(no summary line)")


wt = REPO / ".scratch" / "q5_base_tree"
shutil.rmtree(str(wt), ignore_errors=True)
wt.mkdir(parents=True)
try:
    tar = subprocess.run(["git", "-C", str(REPO), "archive", BASE, "lib", "pytest.ini", "infra/logic", "org/standards", "integrations/bloomberg"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(wt)], input=tar, check=True)
    base_counts, base_line = run(wt)
finally:
    shutil.rmtree(str(wt), ignore_errors=True)
after_counts, after_line = run(REPO)
print("BASE  %s: %s" % (BASE, base_line))
print("AFTER HEAD: %s" % after_line)
for name, c in (("base", base_counts), ("after", after_counts)):
    print("%s: %d passed, %d failed, %d error" % (name, c.get("passed", 0), c.get("failed", 0), c.get("error", 0) + c.get("errors", 0)))
print("%d failed" % after_counts.get("failed", 0))
