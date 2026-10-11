"""ADVI_FIRMBKTS round 4 check for cell FB-g-35 (c290: the account's SNS SMS preferences gain `default_sms_type = "Transactional"`;
the CTO's ruling AMENDMENT 6, msg 4021), issuer 2.0.0_SA_COO~B1.

Reads the one resource as TEXT (no provider, no AWS).

--arms pref [--root <tree>] [--base <ref>]  (4 arms)
  T1 `resource "aws_sns_sms_preferences" "account"` carries `default_sms_type = "Transactional"` exactly once.
  T2 the resource's other attributes are the base's, character for character (`monthly_spend_limit`,
     `delivery_status_iam_role_arn`, `delivery_status_success_sampling_rate`, `depends_on`).
  T3 DORMANT: every base line of the file is kept in order (comment lines excepted) and no other file of the
     `inf-pipeline` root changes.
  T4 `terraform fmt -check` reads clean on the file.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOTDIR = "infra/aws/terraform/inf-pipeline"
FILE = ROOTDIR + "/inf-ops-alerts-sms-delivery-status.tf"


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def _block(text):
    m = re.search(r'resource\s+"aws_sns_sms_preferences"\s+"account"\s*\{', text)
    if not m:
        return ""
    i, depth = m.end(), 1
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[m.start():i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("pref",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base", default="HEAD~1")
    a = ap.parse_args()
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    res = []
    new = open(os.path.join(root, *FILE.split("/")), encoding="utf-8").read()
    old = _git(root, "show", "%s:%s" % (a.base, FILE))
    bn, bo = _block(new), _block(old)
    ok1 = len(re.findall(r'^\s*default_sms_type\s*=\s*"Transactional"\s*$', bn, re.M)) == 1
    print("  T1 default_sms_type lines=%d" % len(re.findall(r"default_sms_type", bn)))
    res.append(("T1 the preferences carry default_sms_type = Transactional exactly once", ok1))

    def attrs(b):
        out = {}
        for ln in b.splitlines():
            m = re.match(r"^\s*(monthly_spend_limit|delivery_status_iam_role_arn|delivery_status_success_sampling_rate)"
                         r"\s*=\s*(.+?)\s*$", ln)
            if m:
                out[m.group(1)] = m.group(2)
        return out
    dep_n = re.search(r"depends_on\s*=\s*\[(.*?)\]", bn, re.S)
    dep_o = re.search(r"depends_on\s*=\s*\[(.*?)\]", bo, re.S)
    ok2 = bool(bo) and attrs(bn) == attrs(bo) and len(attrs(bo)) == 3 and dep_n and dep_o and \
        re.sub(r"\s+", "", dep_n.group(1)) == re.sub(r"\s+", "", dep_o.group(1))
    print("  T2 other attributes equal base: %s" % (attrs(bn) == attrs(bo)))
    res.append(("T2 the resource's other attributes are the base's", bool(ok2)))

    so = [ln for ln in old.splitlines() if not ln.strip().startswith("#")]
    sn = [ln for ln in new.splitlines() if not ln.strip().startswith("#")]
    i = 0
    for ln in sn:
        if i < len(so) and ln == so[i]:
            i += 1
    changed = _git(root, "diff", "--name-only", a.base, "HEAD", "--", ROOTDIR).split() + \
        _git(root, "diff", "--name-only", "HEAD", "--", ROOTDIR).split()
    others = sorted({x for x in changed if x != FILE})
    print("  T3 base lines kept %d of %d; other files changed: %s" % (i, len(so), others))
    res.append(("T3 dormant: base lines kept in order and no other file of the root changes", i == len(so) and not others))

    tf = shutil.which("terraform")
    rc = subprocess.run([tf, "fmt", "-check", os.path.join(root, *FILE.split("/"))], capture_output=True, text=True,
                        timeout=60).returncode if tf else 1
    print("  T4 fmt rc=%d" % rc)
    res.append(("T4 terraform fmt reads clean", rc == 0))
    for n, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    k = sum(1 for _, ok in res if ok)
    print("ROUND 4 SMS TYPE: %d of 4 arms" % k)
    return 0 if k == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
