"""AR-y-466 bound check: the registry commit that adds ANALYSIS_AUDIT is one file, additions only.

Stdlib only, offline. The edit commit is the newest commit that changed infra/logic/registry/reporting_policies.json.
It is HEAD~1 when the edit is the last commit before the deliverables; a later deliverables commit moves HEAD
off the edit, so a literal HEAD~1 read would compare nothing. This check reads the edit commit itself.

It prints the commit, its subject and its numstat, then AUDIT-FAMILY-BOUND-OK numstat=<ins>/<del> files=<n>
only when deletions are 0, exactly one file changed in that commit, and the subject cites AR-y-466.
Otherwise it prints AUDIT-FAMILY-BOUND-BAD <why> and exits 1.
"""

import os
import subprocess
import sys

REGISTRY = "infra/logic/registry/reporting_policies.json"
CITE = "AR-y-466"


def git(root, *args):
    proc = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True,
                          encoding="utf-8", check=False)
    return proc.returncode, proc.stdout, proc.stderr


def find_root(start):
    cur = start
    for _ in range(12):
        if os.path.isfile(os.path.join(cur, REGISTRY)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def main():
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    if root is None:
        print("AUDIT-FAMILY-BOUND-BAD registry not found above this file")
        return 1
    rc, out, err = git(root, "log", "-1", "--format=%H", "--", REGISTRY)
    commit = out.strip()
    if rc != 0 or not commit:
        print("AUDIT-FAMILY-BOUND-BAD no commit touches %s (rc=%d %s)" % (REGISTRY, rc, err.strip()))
        return 1
    rc, subject, _ = git(root, "log", "-1", "--format=%s", commit)
    rc2, head, _ = git(root, "rev-parse", "HEAD")
    print("EDIT-COMMIT %s HEAD=%s" % (commit, head.strip()))
    print("SUBJECT %s" % subject.strip())
    rc, numstat, err = git(root, "show", "--numstat", "--format=", commit)
    if rc != 0:
        print("AUDIT-FAMILY-BOUND-BAD git show rc=%d %s" % (rc, err.strip()))
        return 1
    rows = [line.split("\t") for line in numstat.splitlines() if line.strip()]
    files = len(rows)
    ins = sum(int(r[0]) for r in rows if r[0].isdigit())
    dels = sum(int(r[1]) for r in rows if r[1].isdigit())
    print("NUMSTAT " + " ".join("%s %s %s" % (r[0], r[1], r[2]) for r in rows))
    if dels != 0:
        print("AUDIT-FAMILY-BOUND-BAD deletions=%d, the edit is additions only" % dels)
        return 1
    if files != 1 or rows[0][2] != REGISTRY:
        print("AUDIT-FAMILY-BOUND-BAD files changed=%d, expected exactly %s" % (files, REGISTRY))
        return 1
    if CITE not in subject:
        print("AUDIT-FAMILY-BOUND-BAD the edit subject does not cite %s" % CITE)
        return 1
    print("AUDIT-FAMILY-BOUND-OK numstat=%d/%d files=%d" % (ins, dels, files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
