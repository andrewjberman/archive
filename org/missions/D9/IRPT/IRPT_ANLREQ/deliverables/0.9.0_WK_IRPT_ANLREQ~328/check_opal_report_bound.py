#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-463: the Terraform change of this order is the one file, with no deletions.

Measures git diff --numstat from the cut commit (the commit that added this task order) to HEAD, restricted to
infra/. Prints OPAL-REPORT-BOUND-OK numstat=<add>/<del> files=1 only when exactly one path changed,
infra/aws/terraform/investor-reporting/ops/iam.tf, with 0 deletions. Otherwise prints OPAL-REPORT-BOUND-BAD with the
measured rows and exits 1. The cell's own edit (the family list of the existing statement) replaces one existing
line, so git counts one deletion; the check reports that count and does not relax the 0-deletion bound.
Stdlib only, offline.
ASCII only.
"""

import os
import subprocess
import sys

TF_PATH = "infra/aws/terraform/investor-reporting/ops/iam.tf"
TASK_ORDER = (
    "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/"
    "IRPT_ANLREQ.TO-AR-y-463.status-role-reads-the-opal-report-pdf-family-terraform-statement.md"
)
NAMING_REL = "lib/opal_naming.py"


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, NAMING_REL)) and os.path.isdir(os.path.join(cur, "infra")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("OPAL-REPORT-BOUND-BAD no worktree root above %s" % start)
        cur = parent


def git(root, args):
    proc = subprocess.run(["git"] + args, cwd=root, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit("OPAL-REPORT-BOUND-BAD git rc=%d %s" % (proc.returncode, proc.stderr.strip()))
    return proc.stdout


def main():
    sys.dont_write_bytecode = True
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    anchor = git(root, ["log", "--format=%H", "-1", "--diff-filter=A", "--", TASK_ORDER]).strip()
    if not anchor:
        print("OPAL-REPORT-BOUND-BAD no cut commit found for TO-AR-y-463")
        return 1
    rows = []
    for line in git(root, ["diff", "--numstat", anchor + "..HEAD", "--", "infra/"]).splitlines():
        if line.strip():
            add, dele, path = line.split("\t", 2)
            rows.append((add, dele, path))
    total_add = sum(int(a) for a, _, _ in rows if a.isdigit())
    total_del = sum(int(d) for _, d, _ in rows if d.isdigit())
    ok = len(rows) == 1 and rows[0][2] == TF_PATH and rows[0][1] == "0" and rows[0][0].isdigit()
    if not ok:
        print("OPAL-REPORT-BOUND-BAD numstat=%d/%d files=%d cut=%s rows=%s" % (
            total_add, total_del, len(rows), anchor[:12],
            " ".join("%s(+%s,-%s)" % (p, a, d) for a, d, p in rows)))
        return 1
    print("OPAL-REPORT-BOUND-OK numstat=%d/%d files=1" % (total_add, total_del))
    return 0


if __name__ == "__main__":
    sys.exit(main())
