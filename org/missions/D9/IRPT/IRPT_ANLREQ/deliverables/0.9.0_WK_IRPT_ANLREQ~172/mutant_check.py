"""AR380-y-AC3 (the one mutant that fails): copies fwd1_advisor.py and test_fwd1_advisor.py to a scratch folder OUTSIDE the
product tree, removes the allowedFirmIds list from the users item, runs the copy's offline tests and prints MUTANT-FIRES only
when they FAIL (else MUTANT-SURVIVES, exit 1). The unmutated copy is run first as a positive control and must PASS.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = '"allowedFirmIds": {"L": [{"S": FIRM}]},'


def run_tests(folder):
    proc = subprocess.run([sys.executable, os.path.join(folder, "test_fwd1_advisor.py")],
                          cwd=folder, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main():
    with open(os.path.join(HERE, "fwd1_advisor.py"), "r", encoding="utf-8") as fh:
        source = fh.read()
    if source.count(TARGET) != 1:
        print("MUTANT-BAD marker found %d times, want 1" % source.count(TARGET))
        return 1
    scratch = tempfile.mkdtemp(prefix="fwd1_advisor_mutant_")
    try:
        shutil.copy(os.path.join(HERE, "test_fwd1_advisor.py"), os.path.join(scratch, "test_fwd1_advisor.py"))
        clean_dir = os.path.join(scratch, "clean")
        mut_dir = os.path.join(scratch, "mutant")
        os.mkdir(clean_dir)
        os.mkdir(mut_dir)
        for folder in (clean_dir, mut_dir):
            shutil.copy(os.path.join(scratch, "test_fwd1_advisor.py"), os.path.join(folder, "test_fwd1_advisor.py"))
        with open(os.path.join(clean_dir, "fwd1_advisor.py"), "w", encoding="utf-8") as fh:
            fh.write(source)
        with open(os.path.join(mut_dir, "fwd1_advisor.py"), "w", encoding="utf-8") as fh:
            fh.write(source.replace(TARGET, ""))
        rc_clean, out_clean = run_tests(clean_dir)
        if rc_clean != 0:
            print("MUTANT-BAD positive control failed: rc=%d %s" % (rc_clean, out_clean))
            return 1
        print("POSITIVE-CONTROL unmutated copy PASSES: rc=0 %s" % out_clean)
        rc_mut, out_mut = run_tests(mut_dir)
        if rc_mut == 0:
            print("MUTANT-SURVIVES allowedFirmIds list removed: tests still pass (rc=0) %s" % out_mut)
            return 1
        print("MUTANT-FIRES allowedFirmIds list removed: tests rc=%d %s" % (rc_mut, out_mut))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
