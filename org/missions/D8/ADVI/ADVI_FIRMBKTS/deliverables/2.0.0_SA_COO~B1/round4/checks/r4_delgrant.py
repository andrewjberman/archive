"""ADVI_FIRMBKTS round 4 check for cell FB-g-25 (the act-0 grant gains one narrow s3:DeleteObject statement on the two
directories the stale-advisor cleanups delete under; the CTO's act-0 CTO half ADDENDUM 1 item 1), issuer 2.0.0_SA_COO~B1.

Reads the bd-pipeline root's iam.tf as TEXT (no provider, no AWS) and the module `opal_name` through `terraform console` on a
mirror tree for the directories the statement must name.

--arms grant [--root <tree>] [--base <ref>]  (5 arms)
  G1 the policy resource `aws_iam_role_policy.bd_exporter_advi_49f_platinum_canonical` holds the two base statements
     (`AdviPlatinumCanonicalObjects`, `AdviPlatinumCanonicalList`) unchanged and exactly ONE new statement
     `AdviPlatinumCanonicalDelete`, Effect Allow, Action exactly [ "s3:DeleteObject" ], no Condition-free bucket-wide resource.
  G2 that statement's Resource is exactly two entries, each `arn:aws:s3:::${...bucket}/${lookup(
     module.opal_name_platinum_grant.class_prefix, "<legacy prefix>")}*` for the legacy prefixes `platinum/advisors/` and
     `gold/entities/advisors/`, and no other key literal.
  G3 those two legacy prefixes are the directories the code deletes under: `D_04` lists `platinum/advisors/<id>/` for its
     departed advisors and `D_02` lists the advisor entity root derived from `advisor_book_key('_')`
     (`gold/entities/advisors/`), read from the tree's files.
  G4 the module's `class_prefix` for the firm resolves each of the two legacy prefixes to a canonical directory under its
     platinum prefix (printed).
  G5 DORMANT: against the base, every line of iam.tf is kept in order except comment lines; no other file under the
     bd-pipeline root changes.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import ast
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

ROOTDIR = "infra/aws/terraform/bd-pipeline"
IAM = ROOTDIR + "/iam.tf"
LEGACY = ["platinum/advisors/", "gold/entities/advisors/"]
GOLD = "data/black_diamond/scripts/gold"


def _text(root, ref, path):
    if ref:
        return ma._git(root, "show", "%s:%s" % (ref, path)).stdout
    return open(os.path.join(root, *path.split("/")), encoding="utf-8").read()


def _resource_block(text):
    m = re.search(r'resource\s+"aws_iam_role_policy"\s+"bd_exporter_advi_49f_platinum_canonical"\s*\{', text)
    if not m:
        return ""
    i, depth = m.end(), 1
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[m.start():i]


def _stmt_blocks(block):
    out = []
    for m in re.finditer(r'^\s*\{\s*\n(.*?)^\s*\}\s*,?\s*$', block, re.S | re.M):
        out.append(m.group(1))
    return out


def grant(root, base):
    res = []
    new = _text(root, None, IAM)
    old = _text(root, base, IAM)
    blk_n, blk_o = _resource_block(new), _resource_block(old)
    sn = re.findall(r'Sid\s*=\s*"([^"]+)"', blk_n)
    so = re.findall(r'Sid\s*=\s*"([^"]+)"', blk_o)
    kept = all(s in sn for s in so) and so == ["AdviPlatinumCanonicalObjects", "AdviPlatinumCanonicalList"]
    d_blk = ""
    m = re.search(r'\{\s*\n\s*Sid\s*=\s*"AdviPlatinumCanonicalDelete"(.*?)\n\s*\}', blk_n, re.S)
    if m:
        d_blk = m.group(1)
    act_ok = re.search(r'Action\s*=\s*\[\s*"s3:DeleteObject"\s*\]', d_blk) is not None
    eff_ok = re.search(r'Effect\s*=\s*"Allow"', d_blk) is not None
    ok1 = (sn == so + ["AdviPlatinumCanonicalDelete"]) and kept and act_ok and eff_ok
    # the two base statements byte-identical: compare the base block's statement text inside the new block
    for s in so:
        mo = re.search(r'Sid\s*=\s*"%s"(.*?)(?=\n\s*\},?\s*\n)' % s, blk_o, re.S)
        mn = re.search(r'Sid\s*=\s*"%s"(.*?)(?=\n\s*\},?\s*\n)' % s, blk_n, re.S)
        if not mo or not mn or mo.group(1) != mn.group(1):
            ok1 = False
    print("  G1 sids new=%s action ok=%s effect ok=%s" % (sn, act_ok, eff_ok))
    res.append(("G1 the policy gains exactly one Allow s3:DeleteObject statement, the two base statements unchanged", ok1))

    lookups = re.findall(r'lookup\(\s*module\.opal_name_platinum_grant\.class_prefix\s*,\s*"([^"]+)"\s*\)', d_blk)
    arns = re.findall(r'"arn:aws:s3:::\$\{module\.opal_name_platinum_grant\.bucket\}/\$\{lookup\([^)]*\)\}\*"', d_blk)
    other_literal = re.findall(r'"(?:advi|gold|platinum|irpt)/[^"]*"', re.sub(r'lookup\([^)]*\)', "", d_blk))
    ok2 = sorted(lookups) == sorted(LEGACY) and len(arns) == 2 and not other_literal and bool(d_blk)
    print("  G2 lookups=%s arns=%d other key literals=%s" % (lookups, len(arns), other_literal))
    res.append(("G2 the statement's two resources are generated through class_prefix, no other key literal", ok2))

    ok3 = True
    d04 = open(os.path.join(root, *(GOLD + "/D_04.client_portal_summary.py").split("/")), encoding="utf-8").read()
    ok3 = ok3 and "_list_prefix('platinum/advisors/')" in d04 and "f'platinum/advisors/{sid}/'" in d04
    lay = open(os.path.join(root, *(GOLD + "/lib/s3_layout.py").split("/")), encoding="utf-8").read()
    tree = ast.parse(lay)
    book = None
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "advisor_book_key":
            for r in ast.walk(n):
                if isinstance(r, ast.JoinedStr):
                    book = "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in r.values)
    root_dir = (book or "").rsplit("/", 2)[0] + "/" if book else None
    d02 = open(os.path.join(root, *(GOLD + "/D_02.advisor_client_detail.py").split("/")), encoding="utf-8").read()
    ok3 = ok3 and root_dir == "gold/entities/advisors/" and "advisor_book_key('_').rsplit('/', 2)[0] + '/'" in d02
    print("  G3 D_04 delete root literal ok=%s; D_02 advisor root=%s" % ("platinum/advisors/" in d04, root_dir))
    res.append(("G3 the two legacy prefixes are the directories the code deletes under", ok3))

    with tempfile.TemporaryDirectory() as td:
        head = ma._mirror(os.path.join(td, "head"), root, None)
        cp = (ma._eval(head, "local.class_prefix") or {}).get("49financial", {})
        pp = (ma._eval(head, "local.platinum_prefix") or {}).get("49financial", "\0")
    ok4 = all(cp.get(k, "").startswith(pp) and cp.get(k, "").endswith("/") for k in LEGACY)
    print("  G4 class_prefix: %s" % {k: cp.get(k) for k in LEGACY})
    res.append(("G4 the module resolves both legacy prefixes to canonical directories under the platinum prefix", ok4))

    strip = [ln for ln in old.splitlines() if not ln.strip().startswith("#")]
    cur = [ln for ln in new.splitlines() if not ln.strip().startswith("#")]
    i = 0
    for ln in cur:
        if i < len(strip) and ln == strip[i]:
            i += 1
    changed = ma._git(root, "diff", "--name-only", base, "HEAD", "--", ROOTDIR).stdout.split()
    changed += ma._git(root, "diff", "--name-only", "HEAD", "--", ROOTDIR).stdout.split()
    others = sorted({c for c in changed if c != IAM})
    print("  G5 base non-comment lines kept in order %d of %d; other root files changed: %s" % (i, len(strip), others))
    res.append(("G5 dormant: iam.tf keeps every base line in order and no other file of the root changes",
                i == len(strip) and not others))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("grant",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 DELETE GRANT: 0 of 5 arms")
        sys.exit(1)
    try:
        res = grant(root, ma._base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the files readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 DELETE GRANT: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
