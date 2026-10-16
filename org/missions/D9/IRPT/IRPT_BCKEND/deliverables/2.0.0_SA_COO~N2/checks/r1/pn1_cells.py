"""IRPT_BCKEND workstream ~PN round 1 (issuer 2.0.0_SA_COO~N2) -- the checks of the BUILD cell IB-pn-1.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.

  IBN1-AC1  the feed script executes at module level when its file sits two directories below the filesystem root (the
            runner layout /tmp/orion_gold_scripts/); at base the line `_HERE.parents[2]` raises IndexError
  IBN1-AC2  in a flat directory holding the script, INF_B_00.canonical_holdings.py, rate_limiter.py and jwt_freshness.py
            (the runner sync result) source_prefixes() returns the bucket and the two prefixes; at base BUILDER_PATH
            points at a sibling scripts/gold/ directory that the flat layout does not have
  IBN1-AC3  the new tests (at least 4) and the feed's three existing test files pass, and the worker's record names
            only paths inside the grant
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

F = "data/inf/manual_api/"
SCRIPT = F + "pull_inflection_scope_account_returns.py"
NEW_TEST = F + "test_scope_feed_runner_layout.py"
EXISTING = [F + "test_pull_inflection_scope_account_returns.py", F + "test_scope_feed_daily_factor.py",
            F + "test_scope_feed_day_complete.py"]
SLOT = 480
RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~%d/IBN1-1_record.json" % SLOT
ALLOWED = {SCRIPT, NEW_TEST, "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pn-1.scope-feed-runner-layout.md"}
SYNCED = ["data/inf/scripts/gold", "data/inf/manual_api", "data/inf/scripts/silver", "data/inf/scripts/bronze"]
FLAT_EXTRA = ["lib/trading_calendar.py"]
SMOKE_AC1 = r"""
import sys
src_path, flat = sys.argv[1], sys.argv[2]
sys.path.insert(0, flat)
fake = "/orion_gold_scripts/pull_inflection_scope_account_returns.py"
source = open(src_path, encoding="utf-8").read()
exec(compile(source, fake, "exec"), {"__file__": fake, "__name__": "runner_layout_smoke"})
print("EXEC-OK")
"""
SMOKE_AC2 = r"""
import importlib.util, sys
script = sys.argv[1]
sys.path.insert(0, sys.argv[2])
spec = importlib.util.spec_from_file_location("runner_layout_flat", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
bucket, accounts, positions = module.source_prefixes()
assert all(isinstance(v, str) and v for v in (bucket, accounts, positions)), (bucket, accounts, positions)
print("PREFIXES-OK")
"""


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def flat_dir(root, tmp):
    """What the runner's sync_scripts() leaves in /tmp/orion_gold_scripts: every non-test .py of the four synced code
    folders (code/gold, code/manual_api, code/silver, code/bronze) flattened by basename, plus trading_calendar.py
    (the apply uploads it beside the feed script). First file wins on a basename collision."""
    flat = Path(tmp) / "orion_gold_scripts"
    flat.mkdir()
    for folder in SYNCED:
        for src in sorted((root / folder).rglob("*.py")):
            if src.name.startswith("test_") or "tests" in src.relative_to(root).parts or "__pycache__" in src.parts:
                continue
            if not (flat / src.name).exists():
                shutil.copy(src, flat / src.name)
    for rel in FLAT_EXTRA:
        src = root / rel
        if not src.is_file():
            fail("flat", "missing source %s" % rel)
        shutil.copy(src, flat / src.name)
    return flat


def run_py(code, args, cwd):
    return subprocess.run([sys.executable, "-I", "-c", code] + args, cwd=cwd, capture_output=True, text=True, timeout=100)


def ac1(root):
    with tempfile.TemporaryDirectory() as tmp:
        flat = flat_dir(root, tmp)
        out = run_py(SMOKE_AC1, [str(flat / Path(SCRIPT).name), str(flat)], str(flat))
    if out.returncode != 0 or "EXEC-OK" not in out.stdout:
        fail("IBN1-AC1", (out.stderr.strip().splitlines() or ["no output"])[-1])


def ac2(root):
    with tempfile.TemporaryDirectory() as tmp:
        flat = flat_dir(root, tmp)
        out = run_py(SMOKE_AC2, [str(flat / Path(SCRIPT).name), str(flat)], str(flat))
    if out.returncode != 0 or "PREFIXES-OK" not in out.stdout:
        fail("IBN1-AC2", (out.stderr.strip().splitlines() or ["no output"])[-1])


def ac3(root):
    new = root / NEW_TEST
    if not new.is_file():
        fail("IBN1-AC3", "new test file absent")
    count = new.read_text(encoding="utf-8").count("\ndef test_")
    if count < 4:
        fail("IBN1-AC3", "new test file holds %d tests, need at least 4" % count)
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", NEW_TEST] + EXISTING, cwd=str(root),
                         capture_output=True, text=True, timeout=110)
    if out.returncode != 0:
        fail("IBN1-AC3", "pytest rc=%d: %s" % (out.returncode, (out.stdout.strip().splitlines() or ["no output"])[-1]))
    record = root / RECORD
    if not record.is_file():
        fail("IBN1-AC3", "record absent: " + RECORD)
    data = json.loads(record.read_text(encoding="utf-8"))
    outside = [p for p in data.get("changed_paths", []) if p not in ALLOWED]
    if outside or SCRIPT not in data.get("changed_paths", []):
        fail("IBN1-AC3", "changed_paths outside the grant or missing the script: %s" % outside)


CHECKS = {"IBN1-AC1": ac1, "IBN1-AC2": ac2, "IBN1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn1_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
