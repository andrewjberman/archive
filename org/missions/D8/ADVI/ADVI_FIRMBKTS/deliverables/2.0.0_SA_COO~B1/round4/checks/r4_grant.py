"""ADVI_FIRMBKTS round 4 check for cell FB-g-2 (the producers' role grant for the canonical platinum home, DRAFTED not
applied), issuer 2.0.0_SA_COO~B1. Row D1-S18.

--arms grant [--root <tree>] [--base <ref>]  (4 arms, repository text only; nothing is planned or applied)
  G1 iam.tf carries exactly one NEW aws_iam_role_policy named `bd_exporter_advi_49f_platinum_canonical` attached to
     aws_iam_role.bd_exporter.
  G2 its statements are exactly: Allow s3:PutObject + s3:GetObject on arn:aws:s3:::opal-data-49financial/advi/49financial/
     platinum/* ; Allow s3:ListBucket on arn:aws:s3:::opal-data-49financial under a StringLike s3:prefix condition naming
     only advi/49financial/platinum/*. No Deny, no other action, no other resource, no bare `*`.
  G3 additive: against the base, iam.tf has 0 deleted lines and no other file under bd-pipeline/ changed.
  G4 `terraform fmt -check` reads clean for iam.tf (skipped as PASS only where terraform is absent and printed).
The base is the merge-base of the tree's HEAD and the primary checkout's HEAD unless --base is given. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

IAM = "infra/aws/terraform/bd-pipeline/iam.tf"
ROOTDIR = "infra/aws/terraform/bd-pipeline"
NAME = "bd_exporter_advi_49f_platinum_canonical"
RES = "arn:aws:s3:::opal-data-49financial/advi/49financial/platinum/*"
BUCKET = "arn:aws:s3:::opal-data-49financial"
PFX = "advi/49financial/platinum/*"


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True)


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _base(root, arg):
    if arg:
        return arg
    wl = _git(root, "worktree", "list", "--porcelain").stdout.split("\n")
    primary = next((ln.split()[1] for ln in wl if ln.startswith("HEAD ")), "")
    return _git(root, "merge-base", "HEAD", primary).stdout.strip()


def _block(text, name):
    m = re.search(r'resource\s+"aws_iam_role_policy"\s+"%s"\s*\{' % re.escape(name), text)
    if not m:
        return None
    depth, i = 1, m.end()
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[m.start():i]


def grant(root, base):
    res = []
    text = open(os.path.join(root, IAM), encoding="utf-8").read()
    old = _git(root, "show", "%s:%s" % (base, IAM)).stdout
    blk = _block(text, NAME)
    new_count = len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"%s"' % NAME, text))
    old_count = len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"%s"' % NAME, old))
    ok1 = blk is not None and new_count == 1 and old_count == 0 and \
        re.search(r"role\s*=\s*aws_iam_role\.bd_exporter\.id", blk) is not None
    print("  policy resources named %s: base=%d now=%d" % (NAME, old_count, new_count))
    res.append(("G1 exactly one new aws_iam_role_policy %s on aws_iam_role.bd_exporter" % NAME, ok1))

    ok2 = False
    if blk:
        effects = re.findall(r'Effect\s*=\s*"(\w+)"', blk)
        actions = re.findall(r'"(s3:[A-Z][A-Za-z*]*|\*)"', blk)
        arns = re.findall(r'"(arn:aws:[^"]*)"', blk)
        stars = re.findall(r'Resource\s*=\s*\[?\s*"\*"', blk)
        prefixes = re.findall(r'"s3:prefix"\s*=\s*\[([^\]]*)\]', blk)
        pf = re.findall(r'"([^"]+)"', prefixes[0]) if prefixes else []
        stmts = len(re.findall(r"Effect\s*=", blk))
        print("  statements=%d effects=%s actions=%s resources=%s prefix=%s" % (stmts, sorted(set(effects)),
                                                                                  sorted(set(actions)),
                                                                                  sorted(set(arns)), pf))
        ok2 = (set(effects) == {"Allow"} and set(actions) == {"s3:PutObject", "s3:GetObject", "s3:ListBucket"}
               and set(arns) == {RES, BUCKET} and not stars and pf == [PFX] and stmts == 2
               and "StringLike" in blk and "s3:DeleteObject" not in blk)
    res.append(("G2 two Allow statements: Put and Get on the canonical prefix, List scoped to it, nothing wider",
                ok2))

    num = _git(root, "diff", "--numstat", base, "HEAD", "--", ROOTDIR).stdout.strip().splitlines()
    wt = _git(root, "diff", "--numstat", "HEAD", "--", ROOTDIR).stdout.strip().splitlines()
    rows = [ln.split("\t") for ln in num + wt if ln.strip()]
    files = sorted({r[2] for r in rows})
    dels = sum(int(r[1]) for r in rows if r[2] == IAM and r[1].isdigit())
    print("  changed under bd-pipeline/: %s; iam.tf deleted lines=%d" % (files, dels))
    res.append(("G3 additive: iam.tf deletes 0 lines and no other bd-pipeline file changed",
                files == [IAM] and dels == 0))

    tf = shutil.which("terraform")
    if tf:
        r = subprocess.run([tf, "fmt", "-check", "-diff", os.path.join(root, IAM)], capture_output=True, text=True)
        print("  terraform fmt -check rc=%d" % r.returncode)
        ok4 = r.returncode == 0
    else:
        print("  terraform not on PATH: fmt arm skipped")
        ok4 = True
    res.append(("G4 terraform fmt -check reads clean for iam.tf", ok4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("grant",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = grant(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (IAM, type(e).__name__, str(e)[:160]))
        res = [("iam.tf readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 GRANT: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
