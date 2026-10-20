#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-468: the bound of this order's Terraform edits, measured from the trunk commit merged in.

AMENDMENT 2 (trunk 00f56f44ba): the bound is git diff --numstat 5143b9b2565 <last Terraform edit commit> over
infra/. It must list exactly one path, infra/aws/terraform/investor-reporting/ycharts/resident.tf, with exactly
one deleted line, and that deleted line must be, by text, the old KMS encryption-context line; the added line
must be the same line with ", local.resident_audit_write_prefixes" inserted inside its concat and nothing else.
Prints AUDIT-WRITE-BOUND-OK numstat=<add>/1 files=1 only then; otherwise AUDIT-WRITE-BOUND-BAD <detail> (rc 1).
Stdlib only, offline (git is read). ASCII only.
"""

import os
import subprocess
import sys

TF_PATH = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
TRUNK_BASE = "5143b9b2565"
NAMING_REL = "lib/opal_naming.py"
OLD_KMS = ('StringLike   = { "kms:EncryptionContext:aws:s3:arn" = concat(local.resident_write_prefixes, '
           'local.resident_read_prefixes, local.ycdgen_opal_report_prefixes) }')
NEW_KMS = OLD_KMS.replace("local.ycdgen_opal_report_prefixes)",
                          "local.ycdgen_opal_report_prefixes, local.resident_audit_write_prefixes)")


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
    last = git(root, ["log", "--format=%H", "-1", "--", TF_PATH]).strip()
    if not last:
        print("AUDIT-WRITE-BOUND-BAD no Terraform edit commit found for %s" % TF_PATH)
        return 1
    rows = []
    for line in git(root, ["diff", "--numstat", TRUNK_BASE, last, "--", "infra/"]).splitlines():
        if line.strip():
            add, dele, path = line.split("\t", 2)
            rows.append((add, dele, path))
    if len(rows) != 1 or rows[0][2] != TF_PATH or rows[0][1] != "1" or not rows[0][0].isdigit():
        print("AUDIT-WRITE-BOUND-BAD " + " ".join("%s(+%s,-%s)" % (p, a, d) for a, d, p in rows))
        return 1
    removed, added = [], []
    for line in git(root, ["diff", "-U0", TRUNK_BASE, last, "--", TF_PATH]).splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    if len(removed) != 1 or removed[0].strip() != OLD_KMS:
        print("AUDIT-WRITE-BOUND-BAD the deleted line is not the old KMS line (%d deleted line(s))" % len(removed))
        return 1
    if [line.strip() for line in added].count(NEW_KMS) != 1:
        print("AUDIT-WRITE-BOUND-BAD no added line is the old KMS line with the audit prefixes appended")
        return 1
    print("AUDIT-WRITE-BOUND-OK numstat=%s/%s files=1" % (rows[0][0], rows[0][1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
