"""AC2 (TO TCKT_VNEXT.TO-R18-TR2): the one mutant that must fire.

Copies main.tf to a fresh folder OUTSIDE the worktree (a tempfile directory), adds a second address to
meeting_request.primary, runs tf_shape_check_mt2.py on the copy, and prints MUTANT-FIRES only when the checker prints
TF-SHAPE-BAD with exit 1 (else MUTANT-SURVIVES, exit 1). The unmutated file is checked first: if it is not
TF-SHAPE-OK the mutant result is meaningless and the script stops with BASELINE-BAD.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
CHECKER = os.path.join(HERE, "tf_shape_check_mt2.py")
MAIN_TF = os.path.join(ROOT, "infra", "aws", "terraform", "ticket-center", "main.tf")
OLD = 'primary    = ["jeanette@opalinvest.com"]'
NEW = 'primary    = ["jeanette@opalinvest.com", "manav@opalinvest.com"]'


def run_checker(path):
    proc = subprocess.run([sys.executable, CHECKER, path], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=110)
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def main():
    rc, out = run_checker(MAIN_TF)
    if rc != 0 or not out.startswith("TF-SHAPE-OK "):
        print("BASELINE-BAD unmutated main.tf did not pass: rc=%d %s" % (rc, out))
        sys.exit(1)

    with open(MAIN_TF, encoding="utf-8") as fh:
        text = fh.read()
    if text.count(OLD) != 1:
        print("BASELINE-BAD expected the meeting primary line exactly once, found %d" % text.count(OLD))
        sys.exit(1)
    mutated = text.replace(OLD, NEW)

    scratch = tempfile.mkdtemp(prefix="tf_mutant_mt2_")
    try:
        copy = os.path.join(scratch, "main.tf")
        with open(copy, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(mutated)
        rc, out = run_checker(copy)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if rc == 1 and out.startswith("TF-SHAPE-BAD "):
        print("MUTANT-FIRES checker rc=1: " + out)
        sys.exit(0)
    print("MUTANT-SURVIVES checker rc=%d: %s" % (rc, out))
    sys.exit(1)


if __name__ == "__main__":
    main()
