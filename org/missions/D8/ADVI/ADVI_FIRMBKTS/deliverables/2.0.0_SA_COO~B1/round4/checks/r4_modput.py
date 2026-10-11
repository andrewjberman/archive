"""ADVI_FIRMBKTS round 4 check for cell FB-g-23 (a scoped fence-exemption row may name s3:PutObject; the module renders its
Deny side only and NEVER an Allow for a write action; the CTO's round-3 ADDENDUM 11), issuer 2.0.0_SA_COO~B1.

Evaluates the module `infra/aws/terraform/modules/opal_name` with `terraform console` and `terraform plan` (no provider, no
AWS) over MIRROR trees built from git objects and fixture registries; nothing under the checkout is touched. It reuses the
helpers of r4_modallow.py (same directory).

--arms put [--root <tree>] [--base <ref>]  (5 arms)
  P1 the real registry: `fence_scoped_statements` and `fence_scoped_allow_statements` are identical in the base and the tree
     for every bucket (printed).
  P2 a fixture scoped row (actions GetObject + PutObject; prefix a `/`-ending prefix): the Deny `AnyOtherAction` statement's
     NotAction holds BOTH actions, the `ObjectsOutsidePrefix` Deny's Action holds BOTH and its NotResource the prefix with `*`.
  P3 the same row renders an Allow `AllowScopedExemption1Objects` whose Action is EXACTLY ["s3:GetObject"] (no PutObject), and
     a row whose actions are ["s3:PutObject"] ONLY renders NO Allow statement at all.
  P4 refusals: actions with `s3:PutObjectAcl`, `s3:DeleteObject`, `s3:PutObjectTagging` or `s3:*` are each refused (plan exit
     non-zero); a grants row naming `s3:PutObject` is refused (an Allow-only row stays read-only).
  P5 the real registry plans clean in the tree's module (plan exit 0).
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

BUCKET = ma.BUCKET
PFX = "advi/49financial/platinum/advisors/"


def _lst(x):
    return x if isinstance(x, list) else [x]


def put(root, base):
    res = []
    real = open(os.path.join(root, *ma.REGF.split("/")), encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as td:
        def mir(name, ref, text=None):
            return ma._mirror(os.path.join(td, name), root, ref, text)

        head = mir("head", None)
        basem = mir("base", base)
        same = True
        for expr in ("local.fence_scoped_statements", "local.fence_scoped_allow_statements"):
            b = ma._eval(basem, expr)
            h = ma._eval(head, expr)
            if expr.endswith("allow_statements") and b is None:
                b = {k: [] for k in (h or {})}
            same = same and b is not None and b == h
        print("  P1 real registry identical in base and tree=%s" % same)
        res.append(("P1 the real registry renders identically (Deny and Allow)", same))

        m2 = mir("p2", None, ma._reg(real, {"actions": ["s3:GetObject", "s3:PutObject"], "prefix": PFX}))
        deny = {s.get("Sid"): s for s in (((ma._eval(m2, "local.fence_scoped_statements") or {}).get(BUCKET)) or [])}
        d_any = deny.get("DenyScopedExemption1AnyOtherAction", {})
        d_obj = deny.get("DenyScopedExemption1ObjectsOutsidePrefix", {})
        ok2 = (sorted(_lst(d_any.get("NotAction", []))) == ["s3:GetObject", "s3:PutObject"]
               and sorted(_lst(d_obj.get("Action", []))) == ["s3:GetObject", "s3:PutObject"]
               and _lst(d_obj.get("NotResource", [])) == ["arn:aws:s3:::%s/%s*" % (BUCKET, PFX)])
        print("  P2 deny sids=%s" % sorted(deny.keys()))
        res.append(("P2 a Get+Put row renders both actions on the Deny side", ok2))

        al = ((ma._eval(m2, "local.fence_scoped_allow_statements") or {}).get(BUCKET)) or []
        a_obj = {s.get("Sid"): s for s in al}.get("AllowScopedExemption1Objects", {})
        m3 = mir("p3", None, ma._reg(real, {"actions": ["s3:PutObject"], "prefix": PFX}))
        al3 = ((ma._eval(m3, "local.fence_scoped_allow_statements") or {}).get(BUCKET))
        ok3 = _lst(a_obj.get("Action", [])) == ["s3:GetObject"] and al3 == [] and len(al) == 1
        print("  P3 allow actions=%s; put-only row allow=%s" % (a_obj.get("Action"), al3))
        res.append(("P3 no Allow is ever rendered for a write action", ok3))

        bad = [("PutObjectAcl", {"scoped": {"actions": ["s3:PutObjectAcl"], "prefix": PFX}}),
               ("DeleteObject", {"scoped": {"actions": ["s3:DeleteObject"], "prefix": PFX}}),
               ("PutObjectTagging", {"scoped": {"actions": ["s3:PutObjectTagging"], "prefix": PFX}}),
               ("s3:*", {"scoped": {"actions": ["s3:*"], "prefix": PFX}}),
               ("grants Put", {"grants": [{"actions": ["s3:PutObject"], "keys": [PFX + "a.json"]}]})]
        refused = 0
        for i, (label, kw) in enumerate(bad):
            m = mir("bad%d" % i, None, ma._reg(real, kw.get("scoped"), kw.get("grants")))
            rc, _ = ma._plan(m)
            if rc != 0:
                refused += 1
            else:
                print("    NOT REFUSED: %s" % label)
        print("  refused %d of %d" % (refused, len(bad)))
        res.append(("P4 PutObjectAcl, DeleteObject, PutObjectTagging, s3:* and a grants Put are refused", refused == len(bad)))

        rc5, _ = ma._plan(head)
        print("  P5 real registry plan rc=%d" % rc5)
        res.append(("P5 the real registry plans clean in the tree's module", rc5 == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("put",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 MODULE PUT: 0 of 5 arms")
        sys.exit(1)
    try:
        res = put(root, ma._base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the module and registry rendered", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 MODULE PUT: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
