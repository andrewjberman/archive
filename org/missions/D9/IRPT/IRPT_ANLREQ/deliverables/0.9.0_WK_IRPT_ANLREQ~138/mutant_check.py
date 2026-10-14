#!/usr/bin/env python3
"""AR330-y-AC2 (IRPT_ANLREQ.TO-AR-y-330): the one mutant. A scratch copy of the research modules (OUTSIDE the product
tree: .scratch/) carries COMMENTARY_DISCLAIMER set back to the base text; the new test file runs against that copy,
with the copy pre-loaded as the `layout_overview` module. Prints MUTANT-FIRES only when the run FAILS, and only when
case (a), which asserts the constant itself, is among the failures; otherwise MUTANT-SURVIVES and exit 1.
A lone copy of layout_overview.py cannot run: load_brand reads HERE/brand (layout_overview.py:77), so the copy carries
the research modules and brand/ beside it."""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # deliverables/<serial>/ -> ... -> worktree root
RESEARCH = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research"
TEST = RESEARCH / "tests" / "test_commentary_disclaimer_pending.py"
BASE = "6abbfec7cf49384fd99ba5b734567f184f9a997a"
REL = "infra/aws/lambda/investor-reporting/ycharts/research/layout_overview.py"
NEW_LINE = 'COMMENTARY_DISCLAIMER = "[Opal disclaimer pending approval]"'
SCRATCH = ROOT / ".scratch" / "ar330_mutant"

DRIVER = '''import importlib.util, os, sys
scratch_research, test_file = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("layout_overview", os.path.join(scratch_research, "layout_overview.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules["layout_overview"] = mod
sys.path.insert(0, scratch_research)
spec.loader.exec_module(mod)
print("MUTANT-LOADED", mod.__file__, repr(mod.COMMENTARY_DISCLAIMER))
import pytest
sys.exit(pytest.main(["-q", "-rA", "-p", "no:cacheprovider", "--color=no", test_file]))
'''


def base_block():
    text = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (BASE, REL)], capture_output=True, text=True,
                          timeout=60, check=True).stdout
    lines = text.splitlines(keepends=True)
    start = [i for i, ln in enumerate(lines) if ln.startswith("COMMENTARY_DISCLAIMER = (")]
    if len(start) != 1:
        raise SystemExit("MUTANT-SURVIVES base constant not found")
    end = start[0]
    while 'ratification.")' not in lines[end]:
        end += 1
    return "".join(lines[start[0]:end + 1])


def main():
    old = base_block()
    if SCRATCH.exists():
        shutil.rmtree(str(SCRATCH))
    shutil.copytree(str(RESEARCH), str(SCRATCH / "research"),
                    ignore=shutil.ignore_patterns("tests", "__pycache__"))
    target = SCRATCH / "research" / "layout_overview.py"
    text = target.read_text(encoding="utf-8")
    if text.count(NEW_LINE + "\n") != 1:
        print("MUTANT-SURVIVES anchor not found once in the copy: %d" % text.count(NEW_LINE + "\n"))
        return 1
    target.write_text(text.replace(NEW_LINE + "\n", old), encoding="utf-8")
    driver = SCRATCH / "drive_mutant.py"
    driver.write_text(DRIVER, encoding="utf-8")
    p = subprocess.run([sys.executable, str(driver), str(SCRATCH / "research"), str(TEST)], cwd=str(SCRATCH),
                       capture_output=True, text=True, timeout=300)
    out = p.stdout + p.stderr
    loaded = [ln for ln in out.splitlines() if ln.startswith("MUTANT-LOADED")]
    failed = [ln for ln in out.splitlines() if ln.startswith("FAILED ")]
    print("PROOF-LOADED-COPY:", loaded[0] if loaded else "NOT-LOADED")
    for ln in failed:
        print("RUN:", ln)
    names_a = [ln for ln in failed if "::test_a_" in ln]
    if p.returncode != 0 and names_a and loaded and str(SCRATCH) in loaded[0]:
        print("MUTANT-FIRES rc=%d failed=%d (case a among them)" % (p.returncode, len(failed)))
        return 0
    print("MUTANT-SURVIVES rc=%d failed=%d case_a_failed=%s loaded=%s" % (
        p.returncode, len(failed), bool(names_a), bool(loaded)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
