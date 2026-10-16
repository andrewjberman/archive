"""AC2 (TO TCKT_VNEXT.TO-R19-TR): the one mutant that must fire.

Copies infra/aws/terraform/ticket-center/main.tf to a scratch folder outside the product paths (<worktree>/.scratch/r19tr_mutant/,
gitignored) with "ALL" added to the ANALYST_INTAKE_ALLOWED_FIRMS value, runs tf_shape_check_r19.py on the copy, and prints
MUTANT-FIRES only when the checker prints TF-SHAPE-BAD (exit 0). Otherwise MUTANT-SURVIVES (exit 1). The unmutated file must pass
the checker first, so a mutant that fires on a broken baseline cannot count.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
REL = "infra/aws/terraform/ticket-center/main.tf"
CHECKER = os.path.join(HERE, "tf_shape_check_r19.py")
GOOD_LINE = '    ANALYST_INTAKE_ALLOWED_FIRMS = "49financial,inflection,cottonwood"'
MUT_LINE = '    ANALYST_INTAKE_ALLOWED_FIRMS = "49financial,inflection,cottonwood,ALL"'
SCRATCH = os.path.join(ROOT, ".scratch", "r19tr_mutant")


def run_checker(path):
    proc = subprocess.run([sys.executable, CHECKER, path], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def main():
    real = os.path.join(ROOT, REL)
    rc, out = run_checker(real)
    if rc != 0 or not out.startswith("TF-SHAPE-OK"):
        print("MUTANT-SURVIVES baseline checker did not pass on the unmutated file: rc=%d %s" % (rc, out))
        sys.exit(1)
    with open(real, "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    hits = [i for i, line in enumerate(lines) if line == GOOD_LINE]
    if len(hits) != 1:
        print("MUTANT-SURVIVES mutation anchor found %d times, expected 1" % len(hits))
        sys.exit(1)
    lines[hits[0]] = MUT_LINE
    os.makedirs(SCRATCH, exist_ok=True)
    mutant = os.path.join(SCRATCH, "main.tf")
    with open(mutant, "wb") as fh:
        fh.write("\n".join(lines).encode("utf-8"))
    rc2, out2 = run_checker(mutant)
    if rc2 == 1 and out2.startswith("TF-SHAPE-BAD"):
        print("MUTANT-FIRES checker rc=1: " + out2)
        sys.exit(0)
    print("MUTANT-SURVIVES checker rc=%d: %s" % (rc2, out2))
    sys.exit(1)


if __name__ == "__main__":
    main()
