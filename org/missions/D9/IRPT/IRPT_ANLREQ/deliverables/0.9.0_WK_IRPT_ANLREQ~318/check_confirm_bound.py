"""AR-y-440 bound check: the change stays inside the door's confirm module and its new test file.

Lists the committed product paths changed since the cut commit (the commit whose message names worker slot 318).
Paths under org/ are the worker's own record (order, deliverables, surprise channel) and are not product paths.
Prints CONFIRM-BOUND-OK files=<n> only when every product path is under PREFIX and 2 <= n <= 6; otherwise prints
CONFIRM-BOUND-BAD <paths> and exits 1. Stdlib only; read-only git.
"""
import os
import subprocess
import sys

PREFIX = "infra/aws/lambda/investor-reporting/ycharts/generate/"
CUT_MESSAGE = "to worker slot 318"
RECORD_PREFIX = "org/"
MIN_FILES = 2
MAX_FILES = 6


def git(args, cwd):
    proc = subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True)
    if proc.returncode != 0:
        print("CONFIRM-BOUND-BAD git rc=%d %s" % (proc.returncode, proc.stderr.strip()))
        sys.exit(1)
    return proc.stdout


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    top = git(["rev-parse", "--show-toplevel"], here).strip()
    cut = git(["log", "--format=%H", "--fixed-strings", "--grep=" + CUT_MESSAGE, "-1"], top).strip()
    if not cut:
        print("CONFIRM-BOUND-BAD no cut commit names '%s'" % CUT_MESSAGE)
        return 1
    changed = [p for p in git(["diff", "--name-only", "--no-renames", cut, "HEAD"], top).splitlines() if p]
    product = [p for p in changed if not p.startswith(RECORD_PREFIX)]
    bad = [p for p in product if not p.startswith(PREFIX)]
    count = len(product)
    if bad or not MIN_FILES <= count <= MAX_FILES:
        print("CONFIRM-BOUND-BAD " + " ".join(bad or product) + " (files=%d)" % count)
        return 1
    print("CONFIRM-BOUND-OK files=%d" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
