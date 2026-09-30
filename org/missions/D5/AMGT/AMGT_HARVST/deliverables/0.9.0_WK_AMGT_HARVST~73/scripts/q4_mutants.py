"""q4 mutants -- each mutant is chatter_axis.py with ONE textual change, loaded in place of the
real module for a fresh pytest run of test_q4_rank_declared_set.py. The unmutated source must
pass the file (control); each mutant must FAIL it. Nothing on disk is modified.

  M1_all_names_hold      restores the all-names rule: ANY coverage-excluded name HOLDs the generation
  M2_score_found_only    scores an article from a publisher outside the declared set
  M3_floor_off_by_one    HOLDs only below 9, so 9 eligible names rank
  M4_quiet_before_eligible  a name with no coverage is read as quiet: eligibility skipped
"""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
SRC = os.path.join(ROOT, "lib", "research", "metrics", "chatter_axis.py")
TEST = "lib/research/metrics/tests/test_q4_rank_declared_set.py"

MUTANTS = [
    ("M1_all_names_hold",
     "if len(eligible_keys) < eligible_floor:",
     "if len(eligible_keys) < eligible_floor or coverage_excluded:"),
    ("M2_score_found_only",
     'if key not in keys or row.get("publisher") not in wanted:',
     "if key not in keys:"),
    ("M3_floor_off_by_one",
     "if len(eligible_keys) < eligible_floor:",
     "if len(eligible_keys) < eligible_floor - 1:"),
    ("M4_quiet_before_eligible",
     "        if wanted and all(day_codes == wanted for day_codes in per_day):\n            eligible.append(key)\n"
     "        elif not any(per_day):\n            excluded[key] = REASON_NOT_SEARCHED\n",
     "        if wanted and all(day_codes == wanted for day_codes in per_day):\n            eligible.append(key)\n"
     "        elif not any(per_day):\n            eligible.append(key)\n"),
]

RUNNER = r'''
import sys, types, importlib.util
sys.path.insert(0, %(root)r)
import lib.research.metrics as pkg
src = open(%(src)r, encoding="utf-8").read()
old, new = %(old)r, %(new)r
if old:
    assert src.count(old) == 1, "mutation site count %%d" %% src.count(old)
    src = src.replace(old, new)
name = "lib.research.metrics.chatter_axis"
mod = types.ModuleType(name)
mod.__file__ = %(src)r
mod.__package__ = "lib.research.metrics"
sys.modules[name] = mod
pkg.chatter_axis = mod
exec(compile(src, %(src)r, "exec"), mod.__dict__)
import pytest
sys.exit(pytest.main(["-q", "--tb=line", "-p", "no:cacheprovider", %(test)r]))
'''


def run(label, old, new):
    code = RUNNER % {"root": ROOT, "src": SRC, "old": old, "new": new, "test": TEST}
    proc = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    tail = [line for line in proc.stdout.splitlines() if line.strip()][-1:]
    failed = [line for line in proc.stdout.splitlines() if line.startswith("FAILED") or "FAILED" in line[:12]]
    print("%s rc=%d %s" % (label, proc.returncode, tail[0] if tail else proc.stderr[-200:]))
    for line in failed[:6]:
        print("    " + line[:160])
    return proc.returncode


def main():
    control = run("CONTROL_unmutated", "", "")
    results = {label: run(label, old, new) for label, old, new in MUTANTS}
    killed = [label for label, rc in results.items() if rc != 0]
    print("MUTANTS killed %d of %d; control rc=%d" % (len(killed), len(MUTANTS), control))
    return 0 if control == 0 and len(killed) == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
