#!/usr/bin/env python3
"""NFRA_OPLGTW OG-ap-24 -- grant generator for the vendor read roles of the G2 client adapters.

Reads (a) the merged adapter modules app/client_adapter_*.py, finding by AST every (vendor, segment, layer, table) they
pass to ctx.prefix(...) (a name bound to a module constant is resolved; a helper that wraps ctx.prefix is inlined; a
vendor, layer or table the AST cannot resolve is printed and is a STOP, exit 2), (b) the DATA_CATALOG rows
(app/refs/DATA_CATALOG.yaml, the rows the core's Ctx reads) to turn each into the bucket and the key prefix, and (c) the
saved live policy documents of the two existing roles (GR_BEFORE inputs) to decide whether an existing role already
covers what an adapter reads.

A segment the AST cannot resolve (a runtime firm segment) is matched against the catalog by (vendor, layer, table) and
the key's firm segments. A table with NO catalog row is a GAP: listed, never invented.

Modes:  (none) print the per-role table and the gaps;  --write  write the .tf;  --check  regenerate and diff against
the committed .tf, exit 0 only when equal in both directions and nothing is unresolved.

ROLE KEY: the vendor, except blackdiamond, which is keyed by firm (CTO ruling, OG-ap-24 A3 / cell OG-ch-1):
blackdiamond49f and blackdiamondcottonwood. Names are lib/opal_naming.py name() output.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
APP = ROOT / "infra/aws/ec2/opal-gateway/app"
CATALOG = APP / "refs/DATA_CATALOG.yaml"
TF = ROOT / "infra/aws/terraform/opal-gateway/client_vendor_roles_iam.tf"
LEGACY = ROOT / "infra/logic/registry/legacy_addresses.json"
LIVE_BD = HERE / "bd_policy_before.json"
LIVE_SCHWAB = HERE / "schwab_policy_before.json"

# key -> (opal_naming scope in LONG form or None, function). The names are printed from name(), never typed.
ROLE_SHAPE = {
    "blackdiamond49f": ("49financial", "blackdiamond-read"),
    "blackdiamondcottonwood": ("cottonwood", "blackdiamond-read"),
    "orion": ("inflection", "orion-read"),
    "eclipse": ("inflection", "eclipse-read"),
    "smartx": (None, "smartx-read"),
    "commonwealth": ("cottonwood", "commonwealth-read"),
}
# keys whose role already exists and is not generated here
EXISTING = {"schwab": "gateway-schwab-read-role"}
# blackdiamond firm segments (the segment with any -live suffix removed) per firm key
BD_SEGMENTS = {"blackdiamond49f": {"49f", "49financial"}, "blackdiamondcottonwood": {"cottonwood"}}
READ_ACTIONS = ["s3:GetObject", "s3:GetObjectVersion"]


class Stop(Exception):
    pass


def head_text(rel):
    """The COMMITTED bytes of a repo path at HEAD. A grant is never derived from a working-tree copy another seat may be
    editing (the catalog is re-emitted in the shared tree while this runs)."""
    r = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + rel], capture_output=True)
    if r.returncode != 0:
        raise Stop("git show HEAD:%s failed rc=%d" % (rel, r.returncode))
    return r.stdout.decode("utf-8")


def head_adapters():
    r = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "--name-only", "HEAD", "infra/aws/ec2/opal-gateway/app/"],
                       capture_output=True)
    if r.returncode != 0:
        raise Stop("git ls-tree failed rc=%d" % r.returncode)
    names = [n for n in r.stdout.decode("utf-8").splitlines() if "/client_adapter_" in n and n.endswith(".py")]
    if not names:
        raise Stop("no client_adapter_*.py at HEAD (a zero is not an absence of adapters: the ls-tree path is wrong)")
    return sorted(names)


def _sha16(doc) -> str:
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]


# --------------------------------------------------------------------------------------------- adapters (AST)

def _consts(tree):
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            out[node.targets[0].id] = node.value.value
    return out


def _ev(node, consts, env):
    """('lit', s) | ('dyn', tag, suffix)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return ("lit", node.value)
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        if node.id in consts:
            return ("lit", consts[node.id])
        return ("dyn", node.id, "")
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _ev(node.left, consts, env), _ev(node.right, consts, env)
        if a[0] == "lit" and b[0] == "lit":
            return ("lit", a[1] + b[1])
        if a[0] == "dyn" and b[0] == "lit":
            return ("dyn", a[1], a[2] + b[1])
        return ("dyn", "expr", "")
    return ("dyn", ast.dump(node)[:40], "")


def _is_ctx_prefix(call):
    return isinstance(call.func, ast.Attribute) and call.func.attr == "prefix" \
        and isinstance(call.func.value, ast.Name) and call.func.value.id == "ctx" and len(call.args) == 4


def scan_adapter(rel):
    path = Path(rel)
    tree = ast.parse(head_text(rel), filename=rel)
    consts = _consts(tree)
    helpers = {}
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef):
            rets = [n for n in ast.walk(fn) if isinstance(n, ast.Return) and isinstance(n.value, ast.Call)
                    and _is_ctx_prefix(n.value)]
            if len(rets) == 1 and len(fn.body) <= 2:
                helpers[fn.name] = ([a.arg for a in fn.args.args], rets[0].value)
    # a variadic helper: def f(ctx, *tables): {t: ctx.prefix(V, S, L, t) for t in tables} -> one read per vararg
    varargs = {}
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef) and fn.args.vararg is not None:
            targets = {c.target.id for n in ast.walk(fn) if isinstance(n, (ast.DictComp, ast.ListComp, ast.SetComp))
                       for c in n.generators if isinstance(c.target, ast.Name)
                       and isinstance(c.iter, ast.Name) and c.iter.id == fn.args.vararg.arg}
            inner = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and _is_ctx_prefix(n)
                     and isinstance(n.args[3], ast.Name) and n.args[3].id in targets]
            if len(inner) == 1:
                varargs[fn.name] = (len(fn.args.args), inner[0])
    skip = {id(h[1]) for h in helpers.values()} | {id(v[1]) for v in varargs.values()}
    found, unresolved = [], []

    def add(call, env, line):
        vendor, seg, layer, table = (_ev(a, consts, env) for a in call.args)
        for what, val in (("vendor", vendor), ("layer", layer), ("table", table)):
            if val[0] != "lit":
                unresolved.append((path.name, line, what, val[1]))
                return
        found.append({"module": path.stem, "line": line, "vendor": vendor[1], "segment": seg,
                      "layer": layer[1], "table": table[1]})

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _is_ctx_prefix(node) and id(node) not in skip:
            add(node, {}, node.lineno)
        elif isinstance(node.func, ast.Name) and node.func.id in varargs:
            nfixed, inner = varargs[node.func.id]
            tname = inner.args[3].id
            for extra in node.args[nfixed:]:
                add(inner, {tname: _ev(extra, consts, {})}, node.lineno)
        elif isinstance(node.func, ast.Name) and node.func.id in helpers:
            params, inner = helpers[node.func.id]
            env = {p: _ev(a, consts, {}) for p, a in zip(params, node.args)}
            add(inner, env, node.lineno)
    return found, unresolved


def role_key(call):
    if call["vendor"] != "blackdiamond":
        return call["vendor"]
    mod = call["module"].replace("client_adapter_", "", 1)
    return "blackdiamond" + (mod[2:] if mod.startswith("bd") else mod)


# --------------------------------------------------------------------------------------------- catalog

def catalog_rows():
    try:
        import yaml
    except ImportError:
        raise Stop("PyYAML is not importable: run with the interpreter that has it (plain python, not -I)")
    doc = yaml.safe_load(head_text("infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"))
    rows = []
    for section in doc.values():
        if isinstance(section, list):
            for row in section:
                if isinstance(row, dict) and row.get("prefix") and row.get("bucket") and row.get("table") \
                        and not row.get("retired"):
                    rows.append(row)
    return rows


def resolve(calls, rows):
    """-> grants {key: {bucket: set(prefix)}}, gaps [(key, vendor, table, segdesc)], matched count per call."""
    grants, gaps = {}, []
    for c in calls:
        key = role_key(c)
        seg = c["segment"]
        hit = []
        for r in rows:
            parts = r["prefix"].split("/")
            if len(parts) < 4 or parts[0] != c["vendor"] or r.get("layer") != c["layer"] or r["table"] != c["table"]:
                continue
            rseg = parts[1]
            if seg[0] == "lit":
                if rseg != seg[1]:
                    continue
            elif seg[2] and not rseg.endswith(seg[2]):
                continue
            base = rseg[:-len(seg[2])] if seg[0] == "dyn" and seg[2] else rseg
            if key in BD_SEGMENTS and base not in BD_SEGMENTS[key]:
                continue
            hit.append(r)
        if not hit:
            sd = seg[1] if seg[0] == "lit" else "<%s>%s" % (seg[1] if seg[1].isidentifier() else "runtime", seg[2])
            gaps.append((key, c["vendor"], c["table"], sd, c["module"]))
        for r in hit:
            grants.setdefault(key, {}).setdefault(r["bucket"], set()).add(r["prefix"])
    return grants, sorted(set(gaps))


def legacy_keys():
    """(bucket, template) -> the registry row key of this order's reader (NFRA_OPLGTW, key gateway-client-*)."""
    doc = json.loads(head_text("infra/logic/registry/legacy_addresses.json"))
    out = {}
    for r in doc["legacy_addresses"]:
        if r.get("reader") == "NFRA_OPLGTW" and r["key"].startswith("gateway-client-"):
            out[(r["bucket"], r["template"])] = r["key"]
    return out


def covers(policy_path, grants_for_key):
    """Offline: does the saved live policy's Allow object statement cover every wanted object ARN?"""
    doc = json.loads(policy_path.read_text(encoding="utf-8"))
    allow = []
    for st in doc["Statement"]:
        if st.get("Effect") == "Allow" and "s3:GetObject" in (st["Action"] if isinstance(st["Action"], list) else [st["Action"]]):
            res = st["Resource"]
            allow += res if isinstance(res, list) else [res]
    miss = []
    for bucket, prefixes in sorted(grants_for_key.items()):
        for p in sorted(prefixes):
            arn = "arn:aws:s3:::%s/%s*" % (bucket, p)
            if not any(a == arn or (a.endswith("*") and arn.startswith(a[:-1])) for a in allow):
                miss.append(arn)
    return miss


# --------------------------------------------------------------------------------------------- naming + render

def names(key):
    sys.path.insert(0, str(ROOT))
    from lib import opal_naming
    scope, fn = ROLE_SHAPE[key]
    return (opal_naming.name("gateway", scope, fn, "role"), opal_naming.name("gateway", scope, fn, "policy"))


def _hcl_list(items, indent):
    pad = " " * indent
    return "[\n" + "".join('%s  "%s",\n' % (pad, i) for i in items) + pad + "]"


def render(grants, adapter_files):
    keys = [k for k in ROLE_SHAPE if k in grants]
    lk = legacy_keys()
    missing = [(b, p) for k in keys for b in grants[k] for p in grants[k][b] if (b, p) not in lk]
    if missing:
        for b, p in sorted(missing):
            print("STOP no legacy_addresses.json row (reader NFRA_OPLGTW, key gateway-client-*) for s3://%s/%s" % (b, p))
        raise Stop("%d prefix(es) have no registry row: commit the rows first" % len(missing))
    out = []
    w = out.append
    w("# =============================================================================")
    w("# NFRA_OPLGTW cell OG-ap-24 -- the vendor read roles of the G2 client adapters (GENERATED).")
    w("# =============================================================================")
    w("# GENERATED by org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/gr_grant_gen.py --write; the same")
    w("# program with --check must find this file equal. Do not edit by hand: change the adapters or the catalog rows and")
    w("# regenerate. Inputs: %s." % ", ".join(adapter_files))
    w("#")
    w("# ONE role per role key the adapters read through. The key is the vendor, except Black Diamond, which is keyed by firm")
    w("# (blackdiamond49f, blackdiamondcottonwood) so IAM fences the two firms apart. Each role:")
    w("#   trust    ONLY the Gateway instance role (aws_iam_role.gw), as the Schwab and Black Diamond readers; no ExternalId and")
    w("#            no secret (a same-account trust that names one role ARN; the ask states this and what the alternative costs).")
    w("#   actions  s3:GetObject and s3:GetObjectVersion on the exact catalog prefixes, s3:ListBucket only with an s3:prefix")
    w("#            under them; explicit Deny on every other object, every other bucket's listing, every other prefix's listing")
    w("#            and every non-read S3 action. No Put, no Delete, no wildcard resource.")
    w("# Names are lib/opal_naming.py name() output, read through the opal_name module (system, scope in LONG form, function, kind).")
    w("# The live gateway-blackdiamond-read-role and gateway-schwab-read-role are")
    w("# not touched. NOT APPLIED by this file's commit: the apply is Phase B, one role at a time, on the issuer's GO.")
    w("# =============================================================================")
    w("")
    w("locals {")
    w("  # The read addresses are the registry's rows (infra/logic/registry/legacy_addresses.json, reader NFRA_OPLGTW), never typed here.")
    w('  cv_registry = jsondecode(file("${path.module}/../../../logic/registry/legacy_addresses.json"))')
    w("  cv_address  = { for r in local.cv_registry.legacy_addresses : r.key => r }")
    w("")
    for k in keys:
        for b in sorted(grants[k]):
            ps = sorted(grants[k][b])
            tag = "%s_%s" % (k, b.replace("-", "_"))
            w("  cv_%s_rows = [" % tag)
            for p in ps:
                w('    local.cv_address["%s"],' % lk[(b, p)])
            w("  ]")
            w('  cv_%s_objects  = [for r in local.cv_%s_rows : "arn:aws:s3:::${r.bucket}/${r.template}*"]' % (tag, tag))
            w('  cv_%s_prefixes = [for r in local.cv_%s_rows : "${r.template}*"]' % (tag, tag))
        w("")
    w('  cv_read_actions = ["s3:GetObject", "s3:GetObjectVersion"]')
    w("}")
    for k in keys:
        role, pol = names(k)
        scope, fn = ROLE_SHAPE[k]
        buckets = sorted(grants[k])
        tags = {b: "%s_%s" % (k, b.replace("-", "_")) for b in buckets}
        all_objs = " , ".join("local.cv_%s_objects" % tags[b] for b in buckets)
        objs = "local.cv_%s_objects" % tags[buckets[0]] if len(buckets) == 1 else "concat(%s)" % all_objs.replace(" , ", ", ")
        bucket_arns = ['"arn:aws:s3:::%s"' % b for b in buckets]
        w("")
        w("# ---------------------------------------------------------------------------")
        w("# %s -- role key %s" % (role, k))
        w("# ---------------------------------------------------------------------------")
        for kind in ("role", "policy"):
            w('module "opal_name_cv_%s_%s" {' % (k, kind))
            w('  source   = "../modules/opal_name"')
            w('  system   = "gateway"')
            if scope is not None:
                w('  scope    = "%s"' % scope)
            w('  function = "%s"' % fn)
            w('  kind     = "%s"' % kind)
            w("}")
            w("")
        w('resource "aws_iam_role" "cv_%s_read" {' % k)
        w("  name = module.opal_name_cv_%s_role.name" % k)
        w("  assume_role_policy = jsonencode({")
        w('    Version = "2012-10-17"')
        w("    Statement = [{")
        w('      Sid       = "OnlyOpalGatewayRole"')
        w('      Effect    = "Allow"')
        w("      Principal = { AWS = aws_iam_role.gw.arn }")
        w('      Action    = "sts:AssumeRole"')
        w("    }]")
        w("  })")
        w('  tags = { Name = module.opal_name_cv_%s_role.name, Project = "NFRA_OPLGTW", Purpose = "client-%s-silver-read" }' % (k, k))
        w("}")
        w("")
        w('resource "aws_iam_role_policy" "cv_%s_read_policy" {' % k)
        w("  name = module.opal_name_cv_%s_policy.name" % k)
        w("  role = aws_iam_role.cv_%s_read.id" % k)
        w("")
        w("  policy = jsonencode({")
        w('    Version = "2012-10-17"')
        w("    Statement = [")
        w("      {")
        w('        Sid       = "DenyNonReadS3Actions"')
        w('        Effect    = "Deny"')
        w('        NotAction = concat(local.cv_read_actions, ["s3:ListBucket"])')
        w("        Resource = [")
        for b in buckets:
            w('          "arn:aws:s3:::%s",' % b)
            w('          "arn:aws:s3:::%s/*",' % b)
        w("        ]")
        w("      },")
        w("      {")
        w('        Sid         = "DenyReadsOutsideTheApprovedPrefixes"')
        w('        Effect      = "Deny"')
        w("        Action      = local.cv_read_actions")
        w("        NotResource = %s" % objs)
        w("      },")
        w("      {")
        w('        Sid         = "DenyListingOtherBuckets"')
        w('        Effect      = "Deny"')
        w('        Action      = "s3:ListBucket"')
        w("        NotResource = [%s]" % ", ".join(bucket_arns))
        w("      },")
        for b in buckets:
            w("      {")
            w('        Sid       = "DenyListingOutsideTheApprovedPrefixes%s"' % ("" if len(buckets) == 1 else b.replace("-", "")))
            w('        Effect    = "Deny"')
            w('        Action    = "s3:ListBucket"')
            w('        Resource  = "arn:aws:s3:::%s"' % b)
            w('        Condition = { StringNotLike = { "s3:prefix" = local.cv_%s_prefixes } }' % tags[b])
            w("      },")
        w("      {")
        w('        Sid      = "AllowApprovedObjectReads"')
        w('        Effect   = "Allow"')
        w("        Action   = local.cv_read_actions")
        w("        Resource = %s" % objs)
        w("      },")
        for b in buckets:
            w("      {")
            w('        Sid       = "AllowApprovedPrefixListing%s"' % ("" if len(buckets) == 1 else b.replace("-", "")))
            w('        Effect    = "Allow"')
            w('        Action    = "s3:ListBucket"')
            w('        Resource  = "arn:aws:s3:::%s"' % b)
            w('        Condition = { StringLike = { "s3:prefix" = local.cv_%s_prefixes } }' % tags[b])
            w("      },")
        w("    ]")
        w("  })")
        w("}")
        w("")
        w('output "opal_gateway_cv_%s_read_role_arn" {' % k)
        w("  value = aws_iam_role.cv_%s_read.arn" % k)
        w("}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------------- main

def build():
    files = [Path(x) for x in head_adapters()]
    calls, unresolved = [], []
    for f in files:
        c, u = scan_adapter(f.as_posix())
        calls += c
        unresolved += u
    if unresolved:
        for u in unresolved:
            print("STOP unresolved %s in %s:%s (%s)" % (u[2], u[0], u[1], u[3]))
        raise Stop("%d call(s) the AST cannot resolve" % len(unresolved))
    rows = catalog_rows()
    grants, gaps = resolve(calls, rows)
    return files, calls, rows, grants, gaps


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    try:
        files, calls, rows, grants, gaps = build()
    except Stop as e:
        print("STOP: %s" % e)
        return 2
    present = sorted({role_key(c) for c in calls})
    text = render(grants, [f.name for f in files])
    if mode == "--write":
        TF.write_text(text, encoding="utf-8", newline="\n")
        print("wrote %s (%d bytes)" % (TF.relative_to(ROOT).as_posix(), len(text.encode())))
    if mode == "--check":
        have = TF.read_text(encoding="utf-8").replace("\r\n", "\n") if TF.exists() else ""
        if have == text:
            print("OK: the committed .tf equals the regenerated text (%d bytes)" % len(text.encode()))
            return 0
        print("FAIL: the committed .tf differs from the regenerated text")
        for line in list(difflib.unified_diff(have.splitlines(), text.splitlines(), "committed", "regenerated", lineterm=""))[:60]:
            print(line)
        return 1
    print("adapters scanned: %d (%s)" % (len(files), ", ".join(f.name for f in files)))
    print("ctx.prefix calls resolved: %d; catalog rows read: %d" % (len(calls), len(rows)))
    print("role keys the adapters read through: %s" % ", ".join(present))
    for k in ROLE_SHAPE:
        if k not in present:
            print("NO ADAPTER YET for role key %s (%s); no role generated" % (k, names(k)[0]))
    for k in sorted(grants):
        if k not in ROLE_SHAPE:
            miss = covers(LIVE_SCHWAB, grants[k]) if k == "schwab" else ["not checked"]
            print("EXISTING ROLE %s [%s]: catalog rows %d; the saved live policy %s" % (EXISTING.get(k), k, sum(len(v) for v in grants[k].values()),
                  "covers all of them" if not miss else "does NOT cover %d of them" % len(miss)))
            continue
        role, pol = names(k)
        n = sum(len(v) for v in grants[k].values())
        print("ROLE %s [%s]: %d prefix(es) in %s" % (role, k, n, ", ".join(sorted(grants[k]))))
        for b in sorted(grants[k]):
            for p in sorted(grants[k][b]):
                print("    s3://%s/%s" % (b, p))
    if "blackdiamondcottonwood" in grants:
        miss = covers(LIVE_BD, grants["blackdiamondcottonwood"])
        print("EXISTING-ROLE REUSE for blackdiamondcottonwood (gateway-blackdiamond-read-role, saved policy sha256_16 %s): %s"
              % (_sha16(json.loads(LIVE_BD.read_text(encoding="utf-8"))),
                 "COVERS all" if not miss else "does NOT cover %d of %d wanted ARN(s)" % (len(miss), sum(len(v) for v in grants["blackdiamondcottonwood"].values()))))
    sw = json.loads(LIVE_SCHWAB.read_text(encoding="utf-8"))
    sw_allow = [r for st in sw["Statement"] if st.get("Effect") == "Allow" and st.get("Sid") == "AllowApprovedObjectReads"
                for r in (st["Resource"] if isinstance(st["Resource"], list) else [st["Resource"]])]
    sw_tables = sorted({a.rstrip("*").rstrip("/").rsplit("/", 1)[1] for a in sw_allow})
    sw_masters = sorted({a.split("/")[2] for a in sw_allow})
    sw_read = sorted({g[2] for g in gaps if g[0] == "schwab"} | {p.rstrip("/").rsplit("/", 1)[1] for bs in grants.get("schwab", {}).values() for p in bs})
    print("SCHWAB (existing gateway-schwab-read-role, saved policy sha256_16 %s): allows %d object ARN(s): tables %s for masters %s;"
          " adapter reads %s; %s" % (_sha16(sw), len(sw_allow), ",".join(sw_tables), ",".join(sw_masters), ",".join(sw_read),
                                      "all adapter tables are inside the allowed tables" if set(sw_read) <= set(sw_tables) else "NOT all inside"))
    print("    no fact_* Schwab prefix is allowed by that policy: %s" % ("true" if not any("/fact_" in a for a in sw_allow) else "false"))
    print("GAPS (tables an adapter reads with NO catalog row; never invented): %d" % len(gaps))
    for g in gaps:
        print("    key=%s vendor=%s table=%s segment=%s (%s)" % g)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
