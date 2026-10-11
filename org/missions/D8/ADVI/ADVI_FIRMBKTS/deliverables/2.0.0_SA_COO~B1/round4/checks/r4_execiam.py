"""ADVI_FIRMBKTS round 4 check for cell FB-g-28 (act 4b's identity side: the exec-summary generator's narrow Put at the
canonical home; the CTO's round-3 ADDENDUM 11), issuer 2.0.0_SA_COO~B1.

Reads infra/aws/terraform/exec-summary/iam.tf as TEXT and the module through `terraform console` (no provider, no AWS).

--arms iam [--root <tree>] [--base <ref>]  (5 arms)
  I1 iam.tf declares a NEW resource `aws_iam_role_policy.exec_summary_canonical_put` on `aws_iam_role.exec_summary_generator`
     whose name comes from a `opal_name` module call (kind policy, scope 49financial), never a typed string.
  I2 that policy holds ONE statement: Effect Allow, Action exactly ["s3:PutObject"] (no PutObjectAcl, no Get, no Delete),
     Resource exactly one ARN built as `arn:aws:s3:::${...bucket}/${lookup(...class_prefix, "platinum/advisors/")}*/exec_summary.json`.
  I3 the module resolves `class_prefix["platinum/advisors/"]` and `bucket` for scope 49financial (printed), so the ARN reads
     `arn:aws:s3:::opal-data-49financial/advi/49financial/platinum/advisors/*/exec_summary.json`.
  I4 DORMANT: every base line of iam.tf is kept in order (comments excepted), the existing policy resource is unchanged,
     and no other file of the root changes.
  I5 `terraform fmt -check` reads clean on iam.tf.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

ROOTDIR = "infra/aws/terraform/exec-summary"
IAM = ROOTDIR + "/iam.tf"
RES = "aws_iam_role_policy"


def _text(root, ref, path):
    if ref:
        return ma._git(root, "show", "%s:%s" % (ref, path)).stdout
    return open(os.path.join(root, *path.split("/")), encoding="utf-8").read()


def _block(text, rtype, name):
    m = re.search(r'resource\s+"%s"\s+"%s"\s*\{' % (rtype, name), text)
    if not m:
        return ""
    i, depth = m.end(), 1
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[m.start():i]


def iam(root, base):
    res = []
    new, old = _text(root, None, IAM), _text(root, base, IAM)
    blk = _block(new, RES, "exec_summary_canonical_put")
    mod_name = re.search(r'name\s*=\s*module\.([A-Za-z0-9_]+)\.name', blk)
    role_ok = "aws_iam_role.exec_summary_generator" in blk
    mod_blk = ""
    if mod_name:
        mm = re.search(r'module\s+"%s"\s*\{(.*?)\n\}' % mod_name.group(1), new, re.S)
        mod_blk = mm.group(1) if mm else ""
    mod_ok = ('scope' in mod_blk and '"49financial"' in mod_blk and re.search(r'kind\s*=\s*"policy"', mod_blk) is not None
              and "../modules/opal_name" in mod_blk)
    ok1 = bool(blk) and role_ok and bool(mod_name) and mod_ok
    print("  I1 resource=%s role ok=%s module=%s module ok=%s" % (bool(blk), role_ok,
                                                                   mod_name.group(1) if mod_name else None, mod_ok))
    res.append(("I1 a new policy resource named by an opal_name module call, on the generator role", ok1))

    stmts = re.findall(r'Sid\s*=\s*"([^"]+)"', blk)
    act = re.search(r'Action\s*=\s*\[\s*"s3:PutObject"\s*\]', blk) is not None
    eff = re.search(r'Effect\s*=\s*"Allow"', blk) is not None
    arns = re.findall(r'"arn:aws:s3:::\$\{module\.%s\.bucket\}/\$\{lookup\(module\.%s\.class_prefix,\s*"platinum/advisors/"\)\}\*/exec_summary\.json"'
                      % (re.escape(mod_name.group(1)) if mod_name else "_", re.escape(mod_name.group(1)) if mod_name else "_"),
                      blk)
    no_acl = "PutObjectAcl" not in blk and "DeleteObject" not in blk and "GetObject" not in blk
    ok2 = bool(blk) and len(stmts) == 1 and act and eff and len(arns) == 1 and no_acl
    print("  I2 statements=%s action ok=%s effect ok=%s arns=%d no acl/delete/get=%s" % (
        stmts, act, eff, len(arns), no_acl))
    res.append(("I2 one Allow statement, s3:PutObject only, one generated exec_summary.json ARN", ok2))

    with tempfile.TemporaryDirectory() as td:
        head = ma._mirror(os.path.join(td, "head"), root, None)
        cp = (ma._eval(head, "local.class_prefix") or {}).get("49financial", {})
    directory = cp.get("platinum/advisors/", "")
    arn = "arn:aws:s3:::%s/%s*/exec_summary.json" % (ma.BUCKET, directory)
    print("  I3 resolved ARN: %s" % arn)
    res.append(("I3 the module resolves the canonical advisors directory under the bucket",
                directory == "advi/49financial/platinum/advisors/"))

    strip_o = [ln for ln in old.splitlines() if not ln.strip().startswith("#")]
    cur = [ln for ln in new.splitlines() if not ln.strip().startswith("#")]
    i = 0
    for ln in cur:
        if i < len(strip_o) and ln == strip_o[i]:
            i += 1
    changed = ma._git(root, "diff", "--name-only", base, "HEAD", "--", ROOTDIR).stdout.split()
    changed += ma._git(root, "diff", "--name-only", "HEAD", "--", ROOTDIR).stdout.split()
    others = sorted({c for c in changed if c != IAM})
    same_res = _block(old, RES, "exec_summary_generator") == _block(new, RES, "exec_summary_generator") != ""
    print("  I4 base lines kept %d of %d; existing policy unchanged=%s; other files: %s" % (i, len(strip_o), same_res,
                                                                                         others))
    res.append(("I4 dormant: base lines kept, the existing policy unchanged, no other file changes",
                i == len(strip_o) and same_res and not others))

    tf = shutil.which("terraform")
    rc = subprocess.run([tf, "fmt", "-check", os.path.join(root, *IAM.split("/"))], capture_output=True,
                        text=True, timeout=60).returncode if tf else 1
    print("  I5 fmt rc=%d" % rc)
    res.append(("I5 terraform fmt reads clean", rc == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("iam",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 EXEC IAM: 0 of 5 arms")
        sys.exit(1)
    try:
        res = iam(root, ma._base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the files readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 EXEC IAM: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
