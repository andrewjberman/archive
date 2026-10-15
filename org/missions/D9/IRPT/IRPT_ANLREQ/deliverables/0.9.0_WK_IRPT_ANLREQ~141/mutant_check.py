"""AR333-y-AC2: the one mutant. Copy resident_worker.py to a scratch folder (inside the worktree's .scratch, never the
product tree), make the producer list one-entry again (the base shape), and run the new r31 test file against the copy.

Prints MUTANT-FIRES only when the run FAILS and a producer-list case is among the failures; otherwise
MUTANT-SURVIVES <why> and exit 1. ASCII only.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # the worktree: deliverables/<serial> -> deliverables -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> ROOT
PKG = ROOT / "infra/aws/lambda/investor-reporting"
NEW = PKG / "reports/tests/test_resident_r31_source.py"
SRC = PKG / "ycharts/generate/resident_worker.py"
SCRATCH = ROOT / ".scratch/mutant_r31"
LIST_NEW = 'OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com", "fwd1-staff-r41a@opal.invalid")'
LIST_BASE = 'OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com",)'
DIRS = ["reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "_scope", "_ids", "_keys", "_authz",
        "intake", "ops"]

if not NEW.is_file() or not SRC.is_file():
    print("MUTANT-SURVIVES INPUT_ABSENT")
    sys.exit(1)
text = SRC.read_text(encoding="utf-8")
if text.count(LIST_NEW) != 1:
    print("MUTANT-SURVIVES NO_UNIQUE_LIST_LINE found=%d" % text.count(LIST_NEW))
    sys.exit(1)

SCRATCH.mkdir(parents=True, exist_ok=True)
mutant = SCRATCH / "resident_worker.py"
mutant.write_text(text.replace(LIST_NEW, LIST_BASE), encoding="utf-8")

# The driver loads the mutant under the name resident_worker BEFORE pytest imports the test module, so every
# `import resident_worker` (the test's own and the installer's) resolves to the copy. The package folders are put on
# the path the same way the sibling test modules do.
driver = (
    "import importlib.util, sys\n"
    "for rel in %r:\n"
    "    p = %r + '/' + rel\n"
    "    sys.path.insert(0, p)\n"
    "sys.path.insert(0, %r)\n"
    "spec = importlib.util.spec_from_file_location('resident_worker', %r)\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "sys.modules['resident_worker'] = mod\n"
    "spec.loader.exec_module(mod)\n"
    "import pytest\n"
    "sys.exit(pytest.main(['-q', '--color=no', '--tb=line', '-rf', '-p', 'no:cacheprovider', %r]))\n"
) % (DIRS, str(PKG), str(SCRATCH), str(mutant), str(NEW))

proc = subprocess.run([sys.executable, "-c", driver], cwd=str(PKG), capture_output=True, encoding="utf-8",
                      errors="replace", timeout=900)
out = proc.stdout + proc.stderr
failed = [ln for ln in out.splitlines() if ln.startswith("FAILED ")]
summary = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
print("MUTANT RUN rc=%d :: %s" % (proc.returncode, summary[-1] if summary else "(no summary line)"))
for ln in failed:
    print("  " + ln[:220])
producer_cases = ("test_the_producer_list_is_exactly", "test_producer_for_the_new_address",
                  "test_the_producer_list_holds_andrew")
if proc.returncode != 0 and any(any(c in ln for c in producer_cases) for ln in failed):
    print("MUTANT-FIRES")
    sys.exit(0)
print("MUTANT-SURVIVES rc=%d producer-list case not among the failures" % proc.returncode)
sys.exit(1)
