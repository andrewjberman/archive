#!/usr/bin/env python3
"""AR331-y-AC2 (TO-AR-y-331): the one mutant that must fail the new route test file.

Copies the investor-reporting tree to a scratch folder OUTSIDE the product tree (under the worktree's .scratch/, which is
gitignored), makes `OwnedAnalysisReader.commentary_pdf` resolve the report's own protected PDF (the `pdf` shape) in the COPY,
and runs the new test file against the copy. A control run on the unmutated copy must pass first, so a failure is the
mutant's and not the copy's. Prints MUTANT-FIRES only when the mutant run FAILS (exit 0); otherwise MUTANT-SURVIVES (exit 1).
ASCII only. The repository root is derived from this file's location.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]  # deliverables/<serial> -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> root
INV = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
SCRATCH = ROOT / ".scratch" / "mutant_check"
NEW_TEST = Path("ops") / "tests" / "test_commentary_pdf_route.py"

MUTANT = '''

# MUTANT (AR331-y-AC2): commentary_pdf resolves the report's own protected PDF, the `pdf` shape.
def _mutant_commentary_pdf(self, principal, request_id, *, signer, data_firm=None):
    return self.pdf(principal, request_id, signer=signer, data_firm=data_firm)


OwnedAnalysisReader.commentary_pdf = _mutant_commentary_pdf
'''


def run_new_tests(copy_root):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "--tb=line",
           str(copy_root / NEW_TEST)]
    proc = subprocess.run(cmd, cwd=str(copy_root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    text = proc.stdout.decode("utf-8", "replace")
    tail = [line for line in text.splitlines() if line.strip()][-1:] or ["(no output)"]
    return proc.returncode, tail[0]


COPIED = ("docs/contracts/investor-reporting", "data/firm_registry.json", "infra/aws/lambda/ci")


def main():
    if SCRATCH.exists():
        shutil.rmtree(str(SCRATCH))
    # The copy keeps the repository's depth (the tests find docs/ and data/ by their depth below the root), so the
    # investor-reporting tree sits at the same relative path under the scratch root.
    copy_root = SCRATCH / "infra" / "aws" / "lambda" / "investor-reporting"
    shutil.copytree(str(INV), str(copy_root), ignore=shutil.ignore_patterns("__pycache__"))
    for rel in COPIED:
        source, dest = ROOT / rel, SCRATCH / rel
        if source.is_dir():
            shutil.copytree(str(source), str(dest), ignore=shutil.ignore_patterns("__pycache__"))
        elif source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(source), str(dest))
    rc_control, last_control = run_new_tests(copy_root)
    print("CONTROL (unmutated copy): rc=%d  %s" % (rc_control, last_control))
    if rc_control != 0:
        print("MUTANT-SURVIVES control copy does not pass; the mutant run would prove nothing")
        return 1
    target = copy_root / "ops" / "owned_report.py"
    with open(str(target), "a", encoding="utf-8", newline="\n") as handle:
        handle.write(MUTANT)
    print("MUTANT applied to copy: " + os.path.relpath(str(target), str(ROOT)).replace(os.sep, "/"))
    rc_mutant, last_mutant = run_new_tests(copy_root)
    print("MUTANT run: rc=%d  %s" % (rc_mutant, last_mutant))
    if rc_mutant != 0:
        print("MUTANT-FIRES")
        return 0
    print("MUTANT-SURVIVES the new test file passed against the mutant")
    return 1


if __name__ == "__main__":
    sys.exit(main())
