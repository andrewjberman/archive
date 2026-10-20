"""IRPT_ANLREQ AR-y-423 (AR423-y-AC3): the write bound of this worker branch.

Takes the branch point `git merge-base HEAD box/dell2`, lists the paths changed between it and HEAD, drops the paths under
org/ (the worker's record), and passes only when what remains is exactly the three product files and the two new test files.
Stdlib only. Prints O5B-BOUND-OK files=5 (rc 0), or O5B-BOUND-BAD <paths> (rc 1).
"""
import subprocess
import sys
from pathlib import Path

EXPECTED = (
    "infra/aws/lambda/investor-reporting/ycharts/research/opal_packager.py",
    "infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py",
    "infra/aws/lambda/investor-reporting/reports/resident_installed.py",
    "infra/aws/lambda/investor-reporting/ycharts/research/tests/test_opal_packager_ready.py",
    "infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_package_on_ready.py",
)


def git(cwd, *args):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit("O5B-BOUND-BAD git-rc=%d" % proc.returncode)
    return proc.stdout


def main():
    here = str(Path(__file__).resolve().parent)
    top = git(here, "rev-parse", "--show-toplevel").strip()
    base = git(top, "merge-base", "HEAD", "box/dell2").strip()
    changed = sorted(p.strip() for p in git(top, "diff", "--name-only", base, "HEAD").splitlines()
                     if p.strip() and not p.strip().startswith("org/"))
    if changed == sorted(EXPECTED):
        print("O5B-BOUND-OK files=%d" % len(changed))
        return 0
    print("O5B-BOUND-BAD " + " ".join(changed))
    return 1


if __name__ == "__main__":
    sys.exit(main())
