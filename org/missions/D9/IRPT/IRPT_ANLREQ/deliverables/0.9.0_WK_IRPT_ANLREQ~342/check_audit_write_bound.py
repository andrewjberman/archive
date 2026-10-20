#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-468: the Terraform edit is the only infra/ change since the cut.

Prints AUDIT-WRITE-BOUND-OK numstat=<add>/<del> files=1 only when git diff --numstat from the cut commit to
HEAD, restricted to infra/, lists exactly one path, infra/aws/terraform/investor-reporting/ycharts/resident.tf,
with 0 deletions. Otherwise prints AUDIT-WRITE-BOUND-BAD <paths> and exits 1.
The cut is the commit that added the task order (git log --diff-filter=A on the order file path; the
commit message does not carry the id). Stdlib only, offline. ASCII only.
"""

import os
import subprocess
import sys

TF_PATH = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
TASK_ORDER = ("org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/"
              "IRPT_ANLREQ.TO-AR-y-468.resident-role-writes-the-analysis-audit-terraform-statement.md")
NAMING_REL = "lib/opal_naming.py"


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, NAMING_REL)) and os.path.isdir(os.path.join(cur, "infra")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("AUDIT-WRITE-BOUND-BAD no worktree root above %s" % start)
        cur = parent


def git(root, args):
    proc = subprocess.run(["git"] + args, cwd=root, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit("AUDIT-WRITE-BOUND-BAD git rc=%d %s" % (proc.returncode, proc.stderr.strip()))
    return proc.stdout


def main():
    sys.dont_write_bytecode = True
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    anchor = git(root, ["log", "--format=%H", "-1", "--diff-filter=A", "--", TASK_ORDER])
    anchor = anchor.strip()
    if not anchor:
        print("AUDIT-WRITE-BOUND-BAD no cut commit found for TO-AR-y-468")
        return 1
    rows = []
    for line in git(root, ["diff", "--numstat", anchor + "..HEAD", "--", "infra/"]).splitlines():
        if line.strip():
            add, dele, path = line.split("\t", 2)
            rows.append((add, dele, path))
    ok = len(rows) == 1 and rows[0][2] == TF_PATH and rows[0][1] == "0" and rows[0][0].isdigit()
    if not ok:
        print("AUDIT-WRITE-BOUND-BAD " + " ".join("%s(+%s,-%s)" % (p, a, d) for a, d, p in rows))
        return 1
    print("AUDIT-WRITE-BOUND-OK numstat=%s/%s files=1" % (rows[0][0], rows[0][1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
