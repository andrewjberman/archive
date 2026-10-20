"""AR-y-478 offline bound check: the Terraform edits of this worker stay inside the cell's write grant.

Stdlib only, offline, git read only. Between the base commit 680818fdb3e and this worker's last Terraform edit commit:
resident.tf has additions only (deletions 0), exactly one new file under the ycharts tree is added
(resident_audit_policy.tf), and no other file under infra/ was changed by this worker's own commits. Trunk-side commits
merged into the branch are in the base of the comparison; only commits whose author is this serial are the worker's own.

Prints AUDIT-MANAGED-BOUND-OK resident_tf=<additions>/<deletions> new_files=<n> others=<n> (rc 0), or
AUDIT-MANAGED-BOUND-BAD <why> (rc 1).
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
SERIAL = "0.9.0_WK_IRPT_ANLREQ~349"
BASE_COMMIT = "680818fdb3e"
YCHARTS = "infra/aws/terraform/investor-reporting/ycharts"
RESIDENT = YCHARTS + "/resident.tf"
NEW_FILE = YCHARTS + "/resident_audit_policy.tf"


def git(args):
    proc = subprocess.run(["git"] + args, cwd=str(ROOT), capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError("git %s rc=%d: %s" % (" ".join(args), proc.returncode,
                                                  proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8")


def own_commits():
    out = git(["log", "--format=%H", "--reverse", "--fixed-strings", "--author=" + SERIAL,
               BASE_COMMIT + "..HEAD"])
    return [c for c in out.split() if c]


def infra_files(commit):
    out = git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", "infra"])
    return [f for f in out.split("\n") if f]


def check():
    commits = own_commits()
    if not commits:
        return False, "no commit by %s between %s and HEAD" % (SERIAL, BASE_COMMIT)
    touched = [(c, infra_files(c)) for c in commits]
    touched = [(c, files) for c, files in touched if files]
    if not touched:
        return False, "no Terraform edit commit by %s" % SERIAL
    last = touched[-1][0]
    others = set()
    for _commit, files in touched:
        for f in files:
            if f not in (RESIDENT, NEW_FILE):
                others.add(f)
    numstat = git(["diff", "--numstat", BASE_COMMIT, last, "--", RESIDENT]).split()
    if len(numstat) < 2:
        return False, "resident.tf has no diff between %s and %s" % (BASE_COMMIT, last)
    adds, dels = int(numstat[0]), int(numstat[1])
    added = [ln.split("\t", 1)[1] for ln in
             git(["diff", "--name-status", "--diff-filter=A", BASE_COMMIT, last, "--", YCHARTS]).splitlines()
             if "\t" in ln]
    problems = []
    if dels != 0:
        problems.append("resident.tf has %d deletions against %s" % (dels, BASE_COMMIT))
    if added != [NEW_FILE]:
        problems.append("new files under ycharts are %s, want [%s]" % (added, NEW_FILE))
    if others:
        problems.append("other infra files changed by own commits: %s" % sorted(others))
    if problems:
        return False, "; ".join(problems)
    return True, "resident_tf=%d/%d new_files=%d others=%d" % (adds, dels, len(added), len(others))


def main():
    try:
        ok, detail = check()
    except RuntimeError as exc:
        print("AUDIT-MANAGED-BOUND-BAD " + str(exc))
        return 1
    if ok:
        print("AUDIT-MANAGED-BOUND-OK " + detail)
        return 0
    print("AUDIT-MANAGED-BOUND-BAD " + detail)
    return 1


if __name__ == "__main__":
    sys.exit(main())
