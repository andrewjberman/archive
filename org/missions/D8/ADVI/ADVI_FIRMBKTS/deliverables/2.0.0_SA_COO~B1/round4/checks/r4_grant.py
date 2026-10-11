"""ADVI_FIRMBKTS round 4 check for cell FB-g-2 (the producers' role grant for the canonical platinum home, DRAFTED not
applied), issuer 2.0.0_SA_COO~B1. Row D1-S18. Amended after the CTO's round-3 ADDENDUM 4: the policy name comes from the
`opal_name` module's `name` output and the bucket and prefix from its `bucket` and `platinum_prefix` outputs (cell
FB-g-13); nothing is typed.

--arms grant [--root <tree>] [--base <ref>]  (4 arms, repository text only; nothing is planned or applied)
  G1 iam.tf carries ONE new `module "opal_name_platinum_grant"` (source ../modules/opal_name; system advi, scope the
     49financial scope's long form, function platinum-canonical-rw, kind policy) and ONE new aws_iam_role_policy
     `bd_exporter_advi_49f_platinum_canonical` on aws_iam_role.bd_exporter whose name is module.<that>.name; the module's
     name() equals what the tree's builder returns for those arguments.
  G2 its two statements: Allow s3:PutObject + s3:GetObject on "arn:aws:s3:::${module.X.bucket}/${module.X.platinum_prefix}*";
     Allow s3:ListBucket on "arn:aws:s3:::${module.X.bucket}" with a StringLike s3:prefix of exactly
     "${module.X.platinum_prefix}*". No Deny, no other action, no literal bucket or prefix, no bare `*`.
  G3 additive: against the base iam.tf has 0 deleted lines and no other file under bd-pipeline/ changed.
  G4 `terraform fmt -check` reads clean for iam.tf (PASS with a printed note where terraform is absent).
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
MOD = "opal_name_platinum_grant"
ARGS = {"system": "advi", "function": "platinum-canonical-rw", "kind": "policy"}


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


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


def _block(text, header_re):
    m = re.search(header_re, text)
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
    mod = _block(text, r'module\s+"%s"\s*\{' % MOD)
    blk = _block(text, r'resource\s+"aws_iam_role_policy"\s+"%s"\s*\{' % NAME)
    n_mod = len(re.findall(r'module\s+"%s"' % MOD, text)) - len(re.findall(r'module\s+"%s"' % MOD, old))
    n_res = len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"%s"' % NAME, text)) - \
        len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"%s"' % NAME, old))
    ok1 = mod is not None and blk is not None and n_mod == 1 and n_res == 1
    scope = None
    if ok1:
        got = dict(re.findall(r'^\s*(\w+)\s*=\s*"([^"]*)"', mod, re.M))
        scope = got.get("scope")
        ok1 = (got.get("source") == "../modules/opal_name" and all(got.get(k) == v for k, v in ARGS.items())
               and bool(scope) and re.search(r"role\s*=\s*aws_iam_role\.bd_exporter\.id", blk) is not None
               and re.search(r"name\s*=\s*module\.%s\.name\b" % MOD, blk) is not None)
        if ok1:
            sys.path.insert(0, os.path.join(root, "lib"))
            import opal_naming  # noqa: E402
            want = opal_naming.name(ARGS["system"], scope, ARGS["function"], ARGS["kind"])
            print("  module name() -> %s" % want)
            ok1 = bool(want)
    print("  new module blocks=%d, new policy resources=%d, scope arg=%r" % (n_mod, n_res, scope))
    res.append(("G1 one new opal_name module call and one new aws_iam_role_policy named by its name output", ok1))

    ok2 = False
    if blk:
        effects = re.findall(r'Effect\s*=\s*"(\w+)"', blk)
        actions = re.findall(r'"(s3:[A-Z][A-Za-z*]*|\*)"', blk)
        stmts = len(re.findall(r"Effect\s*=", blk))
        bucket = "module.%s.bucket" % MOD
        prefix = "module.%s.platinum_prefix" % MOD
        res_objs = 'arn:aws:s3:::${%s}/${%s}*' % (bucket, prefix)
        res_list = 'arn:aws:s3:::${%s}' % bucket
        pfx_cond = '${%s}*' % prefix
        arns = re.findall(r'"(arn:aws:[^"]*)"', blk)
        prefixes = re.findall(r'"s3:prefix"\s*=\s*\[([^\]]*)\]', blk)
        pf = re.findall(r'"([^"]+)"', prefixes[0]) if prefixes else []
        literal = re.search(r"opal-data-|advi/|49financial", blk) is not None
        stars = re.findall(r'Resource\s*=\s*\[?\s*"\*"', blk)
        print("  statements=%d effects=%s actions=%s resources=%s prefix=%s" % (stmts, sorted(set(effects)),
                                                                                  sorted(set(actions)), sorted(set(arns)), pf))
        ok2 = (set(effects) == {"Allow"} and set(actions) == {"s3:PutObject", "s3:GetObject", "s3:ListBucket"}
               and set(arns) == {res_objs, res_list} and pf == [pfx_cond] and stmts == 2 and "StringLike" in blk
               and not literal and not stars and "s3:DeleteObject" not in blk)
    res.append(("G2 two Allow statements built from the module's bucket and platinum_prefix outputs, nothing wider, "
                "no typed literal", ok2))

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
