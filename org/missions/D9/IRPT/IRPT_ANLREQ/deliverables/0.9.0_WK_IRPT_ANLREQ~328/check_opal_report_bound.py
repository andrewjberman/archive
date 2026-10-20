#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-463: the Terraform change of this order is the one file, bounded per AMENDMENT 1.

Measured CUMULATIVELY from the cut commit (the commit that added this task order, e02d849d49) to the last commit
of this branch that edits infra/aws/terraform/investor-reporting/ops/iam.tf:
  - the only path changed in that range is ops/iam.tf;
  - deletions are 0 or 1;
  - when the deletion is 1, the deleted line is the old
        for family in concat([...], [local.original_holdings_family, local.vendor_pdf_family]) :
    line, and the one added line that replaces it is that same line with ", local.opal_report_family" appended
    inside the second list and nothing else changed.
Prints OPAL-REPORT-BOUND-OK numstat=<add>/<del> files=1 when that holds; otherwise OPAL-REPORT-BOUND-BAD <why>
and exits 1. Stdlib only, offline.
ASCII only.
"""

import os
import re
import subprocess
import sys

TF_PATH = "infra/aws/terraform/investor-reporting/ops/iam.tf"
TASK_ORDER = (
    "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/"
    "IRPT_ANLREQ.TO-AR-y-463.status-role-reads-the-opal-report-pdf-family-terraform-statement.md"
)
CUT_PREFIX = "e02d849d49"
NAMING_REL = "lib/opal_naming.py"
ORIG_LIST = "[local.original_holdings_family, local.vendor_pdf_family]"
NEW_LIST = "[local.original_holdings_family, local.vendor_pdf_family, local.opal_report_family]"
OLD_LINE_RE = re.compile(
    r"^\s*for family in concat\(\[.*\], \[local\.original_holdings_family, local\.vendor_pdf_family\]\) :\s*$"
)


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


def bad(why):
    print("OPAL-REPORT-BOUND-BAD " + why)
    return 1


def deletion_reasons(root, anchor, last):
    """Return the reasons the one deleted line is not the allowed replacement (empty when it is)."""
    diff = git(root, ["diff", "-U0", "--no-color", anchor, last, "--", TF_PATH])
    minus = []
    plus = []
    for line in diff.splitlines():
        if line.startswith("---") or line.startswith("+++") or line.startswith("\\"):
            continue
        if line.startswith("-"):
            minus.append(line[1:].rstrip("\r"))
        elif line.startswith("+"):
            plus.append(line[1:].rstrip("\r"))
    why = []
    if len(minus) != 1:
        return ["expected exactly one deleted line, found %d" % len(minus)]
    old = minus[0]
    if not OLD_LINE_RE.match(old):
        why.append("deleted line is not the old family-list concat line: %r" % old.strip())
    if old.count(ORIG_LIST) != 1:
        why.append("deleted line does not carry the second list exactly once")
    else:
        expected = old.replace(ORIG_LIST, NEW_LIST, 1).rstrip()
        if expected not in [p.rstrip() for p in plus]:
            why.append("no added line is the old line with ', local.opal_report_family' appended in the second list")
    return why


def main():
    sys.dont_write_bytecode = True
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    anchor = git(root, ["log", "--format=%H", "-1", "--diff-filter=A", "--", TASK_ORDER]).strip()
    if not anchor:
        return bad("no cut commit found for TO-AR-y-463")
    if not anchor.startswith(CUT_PREFIX):
        return bad("cut commit is %s, expected %s" % (anchor[:12], CUT_PREFIX))
    last = git(root, ["log", "--format=%H", "-1", anchor + "..HEAD", "--", TF_PATH]).strip()
    if not last:
        return bad("no Terraform edit commit after the cut touches %s" % TF_PATH)
    names = [n for n in git(root, ["diff", "--name-only", anchor, last]).splitlines() if n.strip()]
    if names != [TF_PATH]:
        return bad("paths changed from cut to last Terraform edit are %s, expected only %s" % (names, TF_PATH))
    rows = [r for r in git(root, ["diff", "--numstat", anchor, last]).splitlines() if r.strip()]
    if len(rows) != 1:
        return bad("numstat rows %d, expected 1" % len(rows))
    add, dele, path = rows[0].split("\t", 2)
    if path != TF_PATH or not add.isdigit() or not dele.isdigit():
        return bad("numstat row %r is not a counted %s change" % (rows[0], TF_PATH))
    if int(dele) not in (0, 1):
        return bad("cumulative deletions %s, allowed 0 or 1" % dele)
    if int(dele) == 1:
        why = deletion_reasons(root, anchor, last)
        if why:
            return bad("; ".join(why))
    print("OPAL-REPORT-BOUND-OK numstat=%d/%d files=1" % (int(add), int(dele)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
