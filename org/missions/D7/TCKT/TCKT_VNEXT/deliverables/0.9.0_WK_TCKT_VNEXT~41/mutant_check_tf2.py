"""TCKT_VNEXT R18-tf-2 / TO-R18-L2 criterion R18L2-AC2 -- the one mutant that must FIRE.

The mutant removes the firm fence on the attachment key at CREATE (the line that refuses a key outside the ticket firm's own
prefix), so a key under another firm's prefix is admitted. It copies infra/aws/lambda/ticket_center/ (lambda_function.py and
tests/) into a scratch folder under the worktree's .scratch/ (gitignored, outside infra/), mutates ONLY the copy, runs the new
trade-form test file against the copy under pytest, and prints MUTANT-FIRES only when that run FAILS and the cross-firm CREATE
test is among the failures. Otherwise it prints MUTANT-SURVIVES and exits 1. The product tree is read, never written.

Run:  python <worktree>/org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~41/mutant_check_tf2.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]   # <worktree>/org/missions/D7/TCKT/TCKT_VNEXT/deliverables/<serial>/ -> <worktree>
SRC = ROOT / "infra" / "aws" / "lambda" / "ticket_center"
ANCHOR = ('    if not isinstance(key, str) or not key.startswith(key_tpl.format(firm=firm)):'
          '   # the firm fence on CREATE (C-FENCE)\n')
MUTANT_LINE = '    if False:  # MUTANT R18L2-AC2: the CREATE firm fence on the attachment key removed\n'
FENCE_TEST = "test_create_with_a_key_under_another_firms_prefix_is_refused"
TEST_FILE = os.path.join("tests", "test_trade_form_attachment.py")


def _survive(reason):
    print("MUTANT-SURVIVES: " + reason)
    sys.exit(1)


def main():
    if not (SRC / "lambda_function.py").is_file() or not (SRC / TEST_FILE).is_file():
        _survive("product tree not found at %s" % SRC)
    text = (SRC / "lambda_function.py").read_text(encoding="utf-8")
    if text.count(ANCHOR) != 1:
        _survive("anchor for the CREATE firm fence found %d times (expected 1); mutation not applied" % text.count(ANCHOR))
    scratch_root = ROOT / ".scratch"
    scratch_root.mkdir(exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="mutant_R18L2_", dir=str(scratch_root)))
    try:
        dst = scratch / "ticket_center"
        shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        (dst / "lambda_function.py").write_text(text.replace(ANCHOR, MUTANT_LINE), encoding="utf-8")
        run = subprocess.run(
            [sys.executable, "-m", "pytest", str(dst / TEST_FILE), "-q", "-p", "no:cacheprovider", "--color=no"],
            cwd=str(scratch), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        out = (run.stdout or "") + (run.stderr or "")
        failed = [ln for ln in out.splitlines() if ln.startswith("FAILED ")]
        summary = [ln for ln in out.splitlines() if " passed" in ln or " failed" in ln or " error" in ln][-1:]
        print("pytest rc=%d on the mutant copy; %s" % (run.returncode, summary[0] if summary else "no summary line"))
        for ln in failed:
            print("  " + ln)
        if run.returncode == 0:
            _survive("the new test file passed on the mutant: the CREATE firm fence does not bind")
        if not any(FENCE_TEST in ln for ln in failed):
            _survive("the run failed, but not on the cross-firm CREATE test %s" % FENCE_TEST)
        print("MUTANT-FIRES: the cross-firm CREATE test %s fails when the firm fence is removed" % FENCE_TEST)
        sys.exit(0)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
