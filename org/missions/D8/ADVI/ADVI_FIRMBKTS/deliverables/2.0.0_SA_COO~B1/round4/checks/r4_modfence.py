"""ADVI_FIRMBKTS round 4 check for cell FB-g-19 (a scoped fence-exemption row's `prefix` takes a string or a LIST; the CTO's
round-3 ADDENDUM 9), issuer 2.0.0_SA_COO~B1.

The module `infra/aws/terraform/modules/opal_name` renders scoped exemption rows into Deny statements from
infra/logic/registry/exemptions.json (read at plan time). This check evaluates the module with `terraform console` and
`terraform plan` (no provider, no AWS) over a MIRROR tree built from git objects (the base commit's module and registry, the
tree's module and registry) and fixture registries, so nothing under the checkout is touched.

--arms render [--root <tree>] [--base <ref>]  (4 arms)
  R1 DIFF 0: the base module and the tree's module render the SAME `fence_scoped_statements` for the real registry
     (every bucket printed; a row with a string prefix renders byte-identically).
  R2 a fixture row whose prefix is a LIST of two prefixes renders: NotResource over BOTH prefixes for the object
     statement, and the listing statement's StringNotLike over both patterns; the BASE module refuses that fixture
     (the control: it is a new capability, not a pre-existing one).
  R3 a fixture row whose prefix list holds `*`, an empty string, a prefix not ending in `/`, or an empty list is REFUSED
     by the tree's module (plan exits non-zero naming the registry).
  R4 the real registry plans clean in the tree's module (plan exit 0).
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
FIX_PRINCIPAL = "arn:aws:iam::313476888478:role/r4-modfence-fixture-role"


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
    """dest/infra/aws/terraform/modules/opal_name/*.tf and dest/infra/logic/registry/exemptions.json, from `ref` (None: the
    working tree), with the registry replaced by registry_text when given."""
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


def _render(mod):
    _tf(["init", "-backend=false", "-input=false", "-no-color"], mod)
    rc, out, err = _tf(["console", "-no-color"], mod, stdin="jsonencode(local.fence_scoped_statements)\n")
    if rc:
        return None, err.strip()[:200]
    try:
        s = out.strip().splitlines()[-1].strip()
        if s.startswith('"') and s.endswith('"'):
            s = json.loads(s)
        return json.loads(s), ""
    except (ValueError, IndexError):
        return None, out.strip()[:200]


def _plan(mod):
    _tf(["init", "-backend=false", "-input=false", "-no-color"], mod)
    rc, out, err = _tf(["plan", "-input=false", "-no-color"], mod)
    return rc, (out + err)


def _fixture(real_text, prefix):
    d = json.loads(real_text)
    d["exemptions"].setdefault(BUCKET, []).append({
        "principal": FIX_PRINCIPAL, "arn": FIX_PRINCIPAL, "reason": "r4_modfence fixture", "signoff_ref": "fixture",
        "actions": ["s3:GetObject"], "prefix": prefix})
    return json.dumps(d, indent=2)


def render(root, base):
    res = []
    real = open(os.path.join(root, *REGF.split("/")), encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as td:
        base_mod = _mirror(os.path.join(td, "base"), root, base)
        head_mod = _mirror(os.path.join(td, "head"), root, None)
        b, be = _render(base_mod)
        h, he = _render(head_mod)
        same = b is not None and h is not None and b == h
        print("  buckets rendered base=%s head=%s; identical=%s %s" % (
            sorted((b or {}).keys()), sorted((h or {}).keys()), same, be or he))
        res.append(("R1 diff 0: the base and the tree render the same fence_scoped_statements for the real registry", same))

        pfx = ["irpt/49financial/gold/holdings_performance_daily/", "advi/49financial/platinum/49financial/"]
        fx_head = _mirror(os.path.join(td, "fx_head"), root, None, _fixture(real, pfx))
        fx_base = _mirror(os.path.join(td, "fx_base"), root, base, _fixture(real, pfx))
        hs, e1 = _render(fx_head)
        rows = [s for s in (hs or {}).get(BUCKET, []) if isinstance(s, dict)]
        text = json.dumps(rows)
        ok2a = all(("arn:aws:s3:::%s/%s*" % (BUCKET, p)) in text for p in pfx) and \
            all(("%s*" % p) in text for p in pfx)
        rc_base, out_base = _plan(fx_base)
        print("  list-prefix fixture: head renders=%s; base module plan rc=%d" % (hs is not None, rc_base))
        res.append(("R2 a list-prefix row renders NotResource and StringNotLike over both prefixes, and the base module "
                    "refuses it", ok2a and rc_base != 0))

        bad = [["*"], [""], ["advi/49financial/platinum/x"], [], ["a/", "b/*"]]
        refused = 0
        for pf in bad:
            m = _mirror(os.path.join(td, "bad%d" % refused), root, None, _fixture(real, pf))
            rc, _out = _plan(m)
            if rc != 0:
                refused += 1
            else:
                print("    NOT REFUSED: prefix %r" % (pf,))
        print("  malformed prefix fixtures refused: %d of %d" % (refused, len(bad)))
        res.append(("R3 a list holding *, an empty string, a prefix not ending in /, or nothing is refused", refused == len(bad)))

        rc4, out4 = _plan(head_mod)
        print("  real registry plan rc=%d" % rc4)
        res.append(("R4 the real registry plans clean in the tree's module", rc4 == 0))
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
        print("ROUND 4 MODULE FENCE: 0 of 4 arms")
        sys.exit(1)
    try:
        res = render(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the module and registry rendered", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 MODULE FENCE: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
