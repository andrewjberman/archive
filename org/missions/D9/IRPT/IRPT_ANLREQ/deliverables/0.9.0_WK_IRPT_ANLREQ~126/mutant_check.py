"""AR-y-316 mutant check (criterion AR316-y-AC2).

Copies the ticket_center tree (lambda_function.py and tests/) into a scratch folder OUTSIDE the product tree
(<worktree>/.scratch/mutant/), first runs the new test file against the UNMUTATED copy as a positive control, then
neutralises the owner check in the copy (the call that sets owner_refusal is replaced by None) and runs the same test
file again. Prints MUTANT-FIRES only when the mutated run FAILS with test failures (pytest rc 1 and a "failed" summary);
prints MUTANT-SURVIVES otherwise (exit 1). The product tree is never written.

Run from anywhere:
    python C:/dev/wk-irpt-anlreq-126/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~126/mutant_check.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]          # worktree root: .../org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>/
SRC = ROOT / "infra" / "aws" / "lambda" / "ticket_center"
SCRATCH = ROOT / ".scratch" / "mutant" / "ticket_center"
NEW_TEST = "test_submit_input_owner.py"
CALL = 'owner_refusal = _check_input_owner(actor, firm, attachment["input_id"])'
MUTANT_CALL = "owner_refusal = None  # MUTANT: the owner check is neutralised"


def fresh_copy():
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SRC, SCRATCH, ignore=shutil.ignore_patterns("__pycache__"))
    return SCRATCH


def run_new_tests(copy_dir):
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(copy_dir / "tests" / NEW_TEST), "-q", "-p", "no:cacheprovider", "--color=no"],
        cwd=str(copy_dir), capture_output=True, text=True, timeout=110)
    out = proc.stdout + proc.stderr
    summary = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed)", ln)]
    failed = [ln for ln in out.splitlines() if ln.startswith("FAILED ")]
    return proc.returncode, (summary[-1] if summary else "no summary"), failed


def main():
    copy_dir = fresh_copy()
    lam = copy_dir / "lambda_function.py"
    original = lam.read_text(encoding="utf-8")
    if original.count(CALL) != 1:
        print(f"MUTANT-SURVIVES: the call site is not found exactly once in the copy (count={original.count(CALL)})")
        return 1

    rc0, sum0, _ = run_new_tests(copy_dir)
    print(f"CONTROL unmutated copy: rc={rc0} | {sum0}")
    if rc0 != 0:
        print("MUTANT-SURVIVES: the positive control does not pass on the unmutated copy, so the mutant run proves nothing")
        return 1

    lam.write_text(original.replace(CALL, MUTANT_CALL), encoding="utf-8")
    rc1, sum1, failed = run_new_tests(copy_dir)
    print(f"MUTANT owner check neutralised: rc={rc1} | {sum1}")
    for ln in failed[:12]:
        print("  " + ln)
    if rc1 == 1 and any("failed" in ln for ln in [sum1]):
        print("MUTANT-FIRES")
        return 0
    print("MUTANT-SURVIVES")
    return 1


if __name__ == "__main__":
    sys.exit(main())
