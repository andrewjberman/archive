"""ADVI_FIRMBKTS round 4 check for cell FB-g-6 (the WAF ACL reconcile, row D1-S12), issuer 2.0.0_SA_COO~B1.

--arms waf [--root <tree>] [--base <ref>]  (3 arms, repository text; the live plan is a separate criterion)
  A1 the only file changed under infra/aws/terraform/portal-auth/ is waf-cloudfront.tf (against the base).
  A2 rule semantics unchanged: the ACL resource's six rule blocks are identical to the base's after the lines that name
     `version` are removed (names, priorities, actions, override_action count{}, statements, visibility).
  A3 `terraform fmt -check` reads clean for the file (PASS with a printed note where terraform is absent).
The base is the merge-base of the tree's HEAD and the primary checkout's HEAD unless --base is given. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOTDIR = "infra/aws/terraform/portal-auth"
F = ROOTDIR + "/waf-cloudfront.tf"


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


def _rules(text):
    m = re.search(r'resource\s+"aws_wafv2_web_acl"\s+"opal_cloudfront_protection"\s*\{', text)
    if not m:
        return None
    depth, i = 1, m.end()
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    body = text[m.end():i]
    out, pos = [], 0
    while True:
        r = re.search(r"^\s*rule\s*\{", body[pos:], re.M)
        if not r:
            break
        start = pos + r.end()
        d, j = 1, start
        while j < len(body) and d:
            d += {"{": 1, "}": -1}.get(body[j], 0)
            j += 1
        blk = body[start:j]
        lines = [ln.strip() for ln in blk.splitlines() if ln.strip() and not ln.strip().startswith("#")
                 and not re.match(r"version\b", ln.strip())]
        out.append(lines)
        pos = j
    return out


def waf(root, base):
    res = []
    num = _git(root, "diff", "--numstat", base, "HEAD", "--", ROOTDIR).stdout.strip().splitlines()
    wt = _git(root, "diff", "--numstat", "HEAD", "--", ROOTDIR).stdout.strip().splitlines()
    files = sorted({ln.split("\t")[2] for ln in num + wt if ln.strip()})
    print("  changed under portal-auth/: %s" % files)
    res.append(("A1 waf-cloudfront.tf is the only portal-auth file changed", files == [F]))
    old = _git(root, "show", "%s:%s" % (base, F)).stdout
    new = open(os.path.join(root, F), encoding="utf-8").read()
    ro, rn = _rules(old), _rules(new)
    same = ro is not None and rn is not None and len(ro) == len(rn) == 6 and ro == rn
    print("  rule blocks base=%s head=%s identical apart from version lines: %s"
          % (len(ro or []), len(rn or []), same))
    res.append(("A2 the ACL's six rule blocks are unchanged apart from lines naming version", same))
    tf = shutil.which("terraform")
    if tf:
        r = subprocess.run([tf, "fmt", "-check", "-diff", os.path.join(root, F)], capture_output=True, text=True)
        print("  terraform fmt -check rc=%d" % r.returncode)
        ok3 = r.returncode == 0
    else:
        print("  terraform not on PATH: fmt arm skipped")
        ok3 = True
    res.append(("A3 terraform fmt -check reads clean for waf-cloudfront.tf", ok3))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("waf",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = waf(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (F, type(e).__name__, str(e)[:160]))
        res = [("waf-cloudfront.tf readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 WAF: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
