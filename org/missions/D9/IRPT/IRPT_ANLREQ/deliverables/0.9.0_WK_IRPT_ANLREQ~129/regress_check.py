"""AR319-y-AC3 regression check (cell AR-y-319).

Runs _scope/tests/test_ordinary_viewer.py (the ordinary-viewer authorizer, which the writer fix must not touch) and
the whole _scope/tests folder. Prints REGRESSION-OK only when the authorizer file has 43 passed and 0 failed AND the
folder's failing test ids equal the base's recorded baseline; otherwise REGRESSION-BAD <why>, exit 1.
The product tree is only read.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[7]
PRODUCT = REPO / "infra" / "aws" / "lambda" / "investor-reporting"
# The base (HEAD 1b9c92aa4a) folder run: 1 failed, 276 passed. The one failure is the known test_resolve.py baseline.
BASE_FAILING = {
    "_scope/tests/test_resolve.py::test_every_trusted_header_is_actually_injected_at_the_line_it_claims",
}
AUTHORIZER_FILE = "_scope/tests/test_ordinary_viewer.py"
EXPECTED_AUTHORIZER_PASSED = 43


def run_pytest(*args):
    return subprocess.run([sys.executable, "-m", "pytest", *args, "-q", "-rfE", "-p", "no:cacheprovider",
                           "--color=no"], cwd=str(PRODUCT), capture_output=True, text=True, timeout=120)


def main():
    if not (REPO / "infra").is_dir() or not (REPO / "org").is_dir():
        print("REGRESSION-BAD repository root not derived from the script path")
        return 1
    auth = run_pytest(AUTHORIZER_FILE)
    m = re.search(r"(\d+) passed", auth.stdout.splitlines()[-1] if auth.stdout.strip() else "")
    failed = re.search(r"(\d+) failed", auth.stdout.splitlines()[-1] if auth.stdout.strip() else "")
    passed = int(m.group(1)) if m else 0
    if auth.returncode != 0 or failed or passed != EXPECTED_AUTHORIZER_PASSED:
        print("REGRESSION-BAD ordinary_viewer rc=%d passed=%d failed=%s" % (auth.returncode, passed,
              failed.group(1) if failed else 0))
        return 1
    folder = run_pytest("_scope/tests")
    failing = {line.split(" ", 1)[1].split(" - ")[0].replace("\\", "/").strip()
               for line in folder.stdout.splitlines() if line.startswith("FAILED ")}
    if failing != BASE_FAILING:
        print("REGRESSION-BAD scope_tests failing ids differ from base: new=%s gone=%s"
              % (sorted(failing - BASE_FAILING), sorted(BASE_FAILING - failing)))
        return 1
    summary = [line for line in folder.stdout.splitlines() if line.strip()][-1]
    print("REGRESSION-OK ordinary_viewer %d passed, 0 failed; scope_tests failing ids equal base (%d): %s"
          % (passed, len(failing), summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
