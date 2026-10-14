"""AR336-y-AC2 checker (written by 0.9.0_WK_IRPT_ANLREQ~143). ASCII only.

Copies reports/build_resident_package.py to a scratch folder OUTSIDE the product tree (the worktree's .scratch/, which is
git-ignored) with the `packager` binding line removed and the commentary key kept. Runs the new test file against that
copy through the IRPT_R31_BUILDER hook. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES, exit 1.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WT = next(p for p in HERE.parents if (p / ".tools").is_dir() and (p / "org").is_dir())
BUILDER_REL = "infra/aws/lambda/investor-reporting/reports/build_resident_package.py"
NEW_REL = "infra/aws/lambda/investor-reporting/reports/tests/test_resident_r31_packager_bindings.py"
SCRATCH = WT / ".scratch" / "r31_mutant"
PACKAGER_LINE = '    "packager": '


def main():
    lines = (WT / BUILDER_REL).read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [line for line in lines if not line.startswith(PACKAGER_LINE)]
    if len(lines) - len(kept) != 1:
        print("MUTANT-SURVIVES the builder has %d packager lines, expected exactly 1" % (len(lines) - len(kept)))
        return 1
    SCRATCH.mkdir(parents=True, exist_ok=True)
    mutant = SCRATCH / "build_resident_package.py"
    mutant.write_text("".join(kept), encoding="utf-8")
    env = dict(os.environ, MSYS_NO_PATHCONV="1", IRPT_R31_BUILDER=str(mutant), PYTHONPATH=str(SCRATCH))
    proc = subprocess.run([sys.executable, "-m", "pytest", str(WT / NEW_REL), "-q", "-p", "no:cacheprovider",
                           "--color=no", "--tb=line"],
                          capture_output=True, text=True, env=env, cwd=str(WT), timeout=600)
    text = proc.stdout + proc.stderr
    summary = [line for line in text.splitlines() if re.search(r"\b(passed|failed|errors?)\b", line)]
    last = summary[-1].strip() if summary else "UNPARSED"
    match = re.search(r"(\d+) failed", last)
    failed = int(match.group(1)) if match else 0
    if proc.returncode != 0 and failed >= 1:
        print("MUTANT-FIRES packager line removed from the scratch copy; new file: " + last)
        return 0
    print("MUTANT-SURVIVES rc=%s new file: %s" % (proc.returncode, last))
    return 1


if __name__ == "__main__":
    sys.exit(main())
