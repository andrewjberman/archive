"""ADVI_FIRMBKTS round 4 check for cell FB-g-21 (the opal_name module renders a bucket-policy ALLOW beside each scoped Deny
row, from the SAME registry row, and an Allow-only `grants` row; a scoped row's prefix list may carry an exact OBJECT KEY;
the CTO's round-3 ADDENDUM 10), issuer 2.0.0_SA_COO~B1.

The module `infra/aws/terraform/modules/opal_name` reads infra/logic/registry/exemptions.json at plan time. This check
evaluates its locals with `terraform console` and `terraform plan` (no provider, no AWS) over MIRROR trees built from git
objects (the base commit's module and registry; the tree's module) and fixture registries, so nothing under the checkout is
touched.

--arms render [--root <tree>] [--base <ref>]  (5 arms)
  R1 the real registry: the Deny statements (`fence_scoped_statements`) are identical in the base and the tree for every
     bucket (printed), a string-prefix fixture row renders the SAME Deny statements in both (byte-identical for a `/`-ending
     prefix), AND the tree's `fence_scoped_allow_statements` is the empty list for every bucket.
  R2 a fixture scoped row (actions GetObject + ListBucket; prefix list = [a `/`-ending prefix, an exact object key]):
     the Deny NotResource and StringNotLike carry the prefix with `*` and the key WITHOUT `*`; one Allow statement
     `AllowScopedExemption1Objects` (Principal the row's ARN, Action GetObject, Resource the prefix with `*` and the exact key
     ARN) and one `AllowScopedExemption1Listing` (Action ListBucket, Resource the bucket ARN, StringLike s3:prefix the same
     patterns); no other Allow.
  R3 a fixture `grants` row (actions GetObject, keys = [one object key]) renders ONE Allow `AllowGrant1Objects` (Principal the
     row's ARN, Resource the exact key ARN), no Deny, and does not enter fence_exemption_arns.
  R4 malformed fixtures are REFUSED (plan exits non-zero): a prefix entry holding `*`, an empty entry, an entry with a
     leading `/`, an empty prefix list; a grants row with a wildcard key, a key ending `/`, an empty keys list, an action
     outside [s3:GetObject], a wildcard principal, or an unknown row key.
  R5 the real registry plans clean in the tree's module (plan exit 0).
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

MOD = "infra/aws/terraform/modules/opal_name"
REGF = "infra/logic/registry/exemptions.json"
BUCKET = "opal-data-49financial"
PRINC = "arn:aws:iam::313476888478:role/r4-modallow-fixture-role"
DIR = "irpt/49financial/gold/holdings_performance_daily/"
KEY = "advi/49financial/platinum/49financial/ownership_map.json"
ROW = {"principal": PRINC, "arn": PRINC, "reason": "r4_modallow fixture", "signoff_ref": "fixture"}


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


def _mirror(dest, root, ref, registry_text=None):
    mod = os.path.join(dest, *MOD.split("/"))
    os.makedirs(mod, exist_ok=True)
    os.makedirs(os.path.join(dest, "infra", "logic", "registry"), exist_ok=True)
    names = _git(root, "ls-tree", "--name-only", ref or "HEAD", MOD + "/").stdout.split()
    for n in names:
        if not n.endswith(".tf"):
            continue
        if ref:
            data = _git(root, "show", "%s:%s" % (ref, n)).stdout
        else:
            data = open(os.path.join(root, *n.split("/")), encoding="utf-8").read()
        open(os.path.join(mod, os.path.basename(n)), "w", encoding="utf-8", newline="\n").write(data)
    if registry_text is None:
        registry_text = (_git(root, "show", "%s:%s" % (ref, REGF)).stdout if ref else
                         open(os.path.join(root, *REGF.split("/")), encoding="utf-8").read())
    open(os.path.join(dest, *REGF.split("/")), "w", encoding="utf-8", newline="\n").write(registry_text)
    return mod


def _tf(args, cwd, stdin=None):
    r = subprocess.run(["terraform"] + args, cwd=cwd, capture_output=True, text=True, input=stdin, timeout=110)
    return r.returncode, r.stdout, r.stderr


_inited = set()


def _init(mod):
    if mod not in _inited:
        _tf(["init", "-backend=false", "-input=false", "-no-color"], mod)
        _inited.add(mod)


def _eval(mod, expr):
    _init(mod)
    rc, out, err = _tf(["console", "-no-color"], mod, stdin="jsonencode(%s)\n" % expr)
    if rc:
        return None
    try:
        s = out.strip().splitlines()[-1].strip()
        if s.startswith('"') and s.endswith('"'):
            s = json.loads(s)
        return json.loads(s)
    except (ValueError, IndexError):
        return None


def _plan(mod):
    _init(mod)
    rc, out, err = _tf(["plan", "-input=false", "-no-color"], mod)
    return rc, out + err


def _reg(real_text, scoped=None, grants=None):
    d = json.loads(real_text)
    if scoped is not None:
        d["exemptions"].setdefault(BUCKET, []).append(dict(ROW, **scoped))
    if grants is not None:
        d.setdefault("grants", {})[BUCKET] = [dict(ROW, **g) for g in grants]
    return json.dumps(d, indent=2)


def _by_sid(stmts):
    return {s.get("Sid"): s for s in stmts if isinstance(s, dict)}


def _lst(x):
    return x if isinstance(x, list) else [x]


def render(root, base):
    res = []
    real = open(os.path.join(root, *REGF.split("/")), encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as td:
        def mir(name, ref, text=None):
            return _mirror(os.path.join(td, name), root, ref, text)

        head = mir("head", None)
        # R1
        b = _eval(mir("base", base), "local.fence_scoped_statements")
        h = _eval(head, "local.fence_scoped_statements")
        ha = _eval(head, "local.fence_scoped_allow_statements")
        fs_b = _eval(mir("fs_base", base, _reg(real, {"actions": ["s3:GetObject"], "prefix": DIR})),
                     "local.fence_scoped_statements")
        fs_h = _eval(mir("fs_head", None, _reg(real, {"actions": ["s3:GetObject"], "prefix": DIR})),
                     "local.fence_scoped_statements")
        same = b is not None and b == h
        fix_same = fs_b is not None and fs_b == fs_h and bool(fs_b.get(BUCKET))
        allow_empty = ha is not None and all(v == [] for v in ha.values()) and len(ha) > 0
        print("  real buckets=%s deny identical=%s; string-prefix fixture identical=%s (%d statements); allow output "
              "empty for all=%s" % (sorted((h or {}).keys()), same, fix_same, len((fs_h or {}).get(BUCKET, [])),
                                    allow_empty))
        res.append(("R1 real registry Deny identical, string-prefix fixture Deny identical, allow output empty",
                    same and fix_same and allow_empty))

        # R2
        m2 = mir("r2", None, _reg(real, {"actions": ["s3:GetObject", "s3:ListBucket"], "prefix": [DIR, KEY]}))
        deny = _by_sid(((_eval(m2, "local.fence_scoped_statements") or {}).get(BUCKET)) or [])
        allow_l = ((_eval(m2, "local.fence_scoped_allow_statements") or {}).get(BUCKET)) or []
        allow = _by_sid(allow_l)
        a_obj = "arn:aws:s3:::%s/%s*" % (BUCKET, DIR)
        k_obj = "arn:aws:s3:::%s/%s" % (BUCKET, KEY)
        d_obj = deny.get("DenyScopedExemption1ObjectsOutsidePrefix", {})
        d_lst = deny.get("DenyScopedExemption1ListingOutsidePrefix", {})
        al_o = allow.get("AllowScopedExemption1Objects", {})
        al_l = allow.get("AllowScopedExemption1Listing", {})
        ok2 = (
            sorted(_lst(d_obj.get("NotResource", []))) == sorted([a_obj, k_obj])
            and sorted(_lst((d_lst.get("Condition", {}).get("StringNotLike", {}) or {}).get("s3:prefix", [])))
            == sorted([DIR + "*", KEY])
            and (al_o.get("Principal") or {}).get("AWS") == PRINC and al_o.get("Effect") == "Allow"
            and _lst(al_o.get("Action", [])) == ["s3:GetObject"]
            and sorted(_lst(al_o.get("Resource", []))) == sorted([a_obj, k_obj])
            and (al_l.get("Principal") or {}).get("AWS") == PRINC and al_l.get("Effect") == "Allow"
            and _lst(al_l.get("Action", [])) == ["s3:ListBucket"]
            and _lst(al_l.get("Resource", [])) == ["arn:aws:s3:::%s" % BUCKET]
            and sorted(_lst((al_l.get("Condition", {}).get("StringLike", {}) or {}).get("s3:prefix", [])))
            == sorted([DIR + "*", KEY])
            and len(allow_l) == 2
        )
        print("  R2 allow sids=%s deny NotResource=%s" % (sorted(allow.keys()), d_obj.get("NotResource")))
        res.append(("R2 a prefix list with an exact key renders the Deny and one Allow per class from the same row", ok2))

        # R3
        m3 = mir("r3", None, _reg(real, None, [{"actions": ["s3:GetObject"], "keys": [KEY]}]))
        a3 = ((_eval(m3, "local.fence_scoped_allow_statements") or {}).get(BUCKET)) or []
        d3 = ((_eval(m3, "local.fence_scoped_statements") or {}).get(BUCKET)) or []
        arns3 = ((_eval(m3, "local.fence_exemption_arns") or {}).get(BUCKET)) or []
        g1 = _by_sid(a3).get("AllowGrant1Objects", {})
        ok3 = (len(a3) == 1 and (g1.get("Principal") or {}).get("AWS") == PRINC and g1.get("Effect") == "Allow"
               and _lst(g1.get("Action", [])) == ["s3:GetObject"] and _lst(g1.get("Resource", [])) == [k_obj]
               and d3 == [] and PRINC not in arns3)
        print("  R3 allow=%d deny=%d in exemption arns=%s" % (len(a3), len(d3), PRINC in arns3))
        res.append(("R3 a grants row renders one Allow on the exact key, no Deny, no exemption", ok3))

        # R4
        bad = [
            ("prefix entry with *", dict(scoped={"actions": ["s3:GetObject"], "prefix": ["a/", "b/*"]})),
            ("empty prefix entry", dict(scoped={"actions": ["s3:GetObject"], "prefix": [""]})),
            ("leading slash entry", dict(scoped={"actions": ["s3:GetObject"], "prefix": ["/a/b.json"]})),
            ("empty prefix list", dict(scoped={"actions": ["s3:GetObject"], "prefix": []})),
            ("grant wildcard key", dict(grants=[{"actions": ["s3:GetObject"], "keys": ["a/*"]}])),
            ("grant key ending slash", dict(grants=[{"actions": ["s3:GetObject"], "keys": ["a/b/"]}])),
            ("grant empty keys", dict(grants=[{"actions": ["s3:GetObject"], "keys": []}])),
            ("grant write action", dict(grants=[{"actions": ["s3:PutObject"], "keys": [KEY]}])),
            ("grant wildcard principal", dict(grants=[{"actions": ["s3:GetObject"], "keys": [KEY],
                                                        "principal": "*", "arn": "*"}])),
            ("grant unknown key", dict(grants=[{"actions": ["s3:GetObject"], "keys": [KEY], "prefix": "a/"}])),
        ]
        refused = 0
        for i, (label, kw) in enumerate(bad):
            m = mir("bad%d" % i, None, _reg(real, kw.get("scoped"), kw.get("grants")))
            rc, _ = _plan(m)
            if rc != 0:
                refused += 1
            else:
                print("    NOT REFUSED: %s" % label)
        print("  malformed fixtures refused: %d of %d" % (refused, len(bad)))
        res.append(("R4 every malformed prefix entry and grants row is refused", refused == len(bad)))

        # R5
        rc5, _ = _plan(head)
        print("  real registry plan rc=%d" % rc5)
        res.append(("R5 the real registry plans clean in the tree's module", rc5 == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("render",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = _root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 MODULE ALLOW: 0 of 5 arms")
        sys.exit(1)
    try:
        res = render(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the module and registry rendered", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 MODULE ALLOW: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
