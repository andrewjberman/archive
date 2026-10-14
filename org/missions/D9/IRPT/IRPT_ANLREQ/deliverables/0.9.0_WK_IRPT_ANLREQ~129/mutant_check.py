"""AR319-y-AC2 mutant check (cell AR-y-319).

Undoes the WRITER fix on a scratch copy outside the product tree (home_firm_id kept for every class), then runs the
new test file against that copy. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES, exit 1.
The product tree is only read.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[7]
PRODUCT = REPO / "infra" / "aws" / "lambda" / "investor-reporting"
CONTRACTS = REPO / "docs" / "contracts" / "investor-reporting"
TEST_REL = Path("_scope") / "tests" / "test_ordinary_owner_composition.py"
FIX = (
    '        if owner.get("principal_class") != "OPAL_GLOBAL":\n'
    '            owner.pop("home_firm_id", None)\n'
)


def main():
    if not (REPO / "infra").is_dir() or not (REPO / "org").is_dir():
        print("MUTANT-SURVIVES repository root not derived from the script path")
        return 1
    source = (PRODUCT / "_scope" / "interactive_access.py").read_text(encoding="utf-8")
    if source.count(FIX) != 1:
        print("MUTANT-SURVIVES undo anchor not found exactly once in _scope/interactive_access.py")
        return 1
    scratch = Path(tempfile.mkdtemp(prefix="ar319_mutant_"))
    try:
        tree = scratch / "repo"
        copy = tree / "infra" / "aws" / "lambda" / "investor-reporting"
        shutil.copytree(PRODUCT, copy, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(CONTRACTS, tree / "docs" / "contracts" / "investor-reporting")
        (tree / "data").mkdir()
        shutil.copy2(REPO / "data" / "firm_registry.json", tree / "data" / "firm_registry.json")
        (copy / "_scope" / "interactive_access.py").write_text(source.replace(FIX, ""), encoding="utf-8")
        run = subprocess.run(
            [sys.executable, "-m", "pytest", str(TEST_REL), "-q", "-p", "no:cacheprovider", "--color=no"],
            cwd=str(copy), capture_output=True, text=True, timeout=120)
        tail = [line for line in run.stdout.splitlines() if line.strip()][-1:] or ["no output"]
        if run.returncode != 0:
            print("MUTANT-FIRES writer undone in a scratch copy: new test file rc=%d; %s"
                  % (run.returncode, tail[0]))
            return 0
        print("MUTANT-SURVIVES writer undone in a scratch copy but new test file rc=0; %s" % tail[0])
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
