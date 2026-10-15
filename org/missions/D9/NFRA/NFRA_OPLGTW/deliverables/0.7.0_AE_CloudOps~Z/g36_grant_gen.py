#!/usr/bin/env python
"""OG-ap-19 Phase A step 2: derive the G3 grant's resource list FROM THE CODE, by AST.

The order's reason for an AST generator, in its own words, is that the grant "cannot drift from the
code (as hv2_grant_gen.py did for the harvest grant)". So nothing here is typed by hand: every prefix
comes out of app/portal_models.py and app/portal_macro.py, the bucket comes out of the naming registry,
and the SUBTRACTION comes out of the existing grant's own Resource list.

WHAT IT PRODUCES: the prefixes the thirteen G3 tools read that the internal reader's EXISTING policy
does NOT already cover. That difference is the whole grant -- a prefix the role can already reach needs
no new statement, and granting it twice would widen nothing while making the diff look bigger than the
act.

WHY AST AND NOT IMPORT: these modules import starlette, boto3 and the gateway's own package, none of
which is needed to read a tuple of string literals. Importing would also run module-level code. ast
reads the literals and nothing else.

THE THREE AGREEMENTS IT REFUSES WITHOUT (each is a Z-S107-class trap -- a grant that passes every
static check while every real read returns AccessDenied):
  1. the bucket the CODE names == the naming registry's bucket for scope `global` == the bucket the LIVE
     policy already names. A grant on the wrong bucket is invisible to a policy linter.
  2. the existing grant's Resource list in the .tf == the one live in IAM. If source and world disagree,
     the subtraction is computed against a fiction, so it stops instead.
  3. the residue is non-empty. An empty residue would mean the grant is unnecessary, and emitting an
     empty policy is not the same answer as "no grant needed" -- it would be a statement with no
     Resource, which is invalid and would be caught much later.

Usage:
  .tools/aws iam get-role-policy --role-name gateway-global-internal-reader-role \
    --policy-name gateway-global-internal-reader-policy --query PolicyDocument --output json > live.json
  python g36_grant_gen.py <gateway dir> --live-policy live.json --json <out>
"""
from __future__ import annotations

import argparse
import ast
import io
import json
import os
import sys

POLICY_NAME = "gateway-global-portal-tiered-read-policy"   # lib/opal_naming.name("gateway","global","portal-tiered-read","policy")
SCOPE = "global"
EXISTING_ROLE = "gateway-global-internal-reader-role"
EXISTING_POLICY = "gateway-global-internal-reader-policy"
EXISTING_TF = "infra/aws/terraform/opal-gateway/mcpmsp_internal_reader.tf"
REGISTRY_LOCALS = "infra/aws/terraform/modules/opal_name/generated_locals.tf"


def literals(path: str) -> dict:
    """Every module-level assignment of a str, or of a tuple/list of str, by name."""
    tree = ast.parse(io.open(path, encoding="utf-8").read(), filename=path)
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for tgt in node.targets:
            if not isinstance(tgt, ast.Name):
                continue
            v = node.value
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out[tgt.id] = v.value
            elif isinstance(v, (ast.Tuple, ast.List)) and v.elts and all(
                    isinstance(e, ast.Constant) and isinstance(e.value, str) for e in v.elts):
                out[tgt.id] = tuple(e.value for e in v.elts)
    return out


def as_prefix(value: str) -> str:
    """A key becomes its directory prefix; a prefix stays itself. Never a bare bucket root."""
    if value.endswith("/"):
        return value
    return value.rsplit("/", 1)[0] + "/" if "/" in value else ""


def covered_by(prefix: str, existing: set) -> bool:
    """True when some existing granted prefix is a prefix of this one (so it is already reachable)."""
    return any(prefix.startswith(e) for e in existing)


def tf_existing_prefixes(path: str) -> set:
    """The granted prefixes in the existing .tf, read from its Resource strings."""
    text = io.open(path, encoding="utf-8").read()
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if "arn:aws:s3:::" not in line:
            continue
        # "arn:aws:s3:::${local.int_served_bkt}/json/*",  ->  json/
        tail = line.split("arn:aws:s3:::", 1)[1].rstrip('",')
        if "/" not in tail:
            continue
        keypart = tail.split("/", 1)[1]
        out.add(keypart[:-1] if keypart.endswith("*") else keypart)
    return out


def live_existing_prefixes(path: str) -> tuple:
    """The same list, read LIVE from IAM -- handed in as a FILE rather than spawned here.

    `.tools/aws` is a bash shim, so native Python cannot spawn it (measured: FileNotFoundError WinError 2),
    and the repo's rule for Python spawning an MSYS binary is msys_safe_run rather than a bare name. Making
    the live read an explicit INPUT is the better shape anyway: the bytes this decision rested on are a
    recorded artifact instead of a subprocess that cannot be re-read later.
    """
    if not os.path.isfile(path):
        return None, "the live policy read is ABSENT at %s -- that is an error, never an empty policy" % path
    raw = io.open(path, encoding="utf-8").read().strip()
    if not raw:
        return None, "the live policy read is EMPTY at %s -- refusing a clean-empty read" % path
    doc = json.loads(raw)
    # guard the shape: a document carrying PolicyDocument with no Statement is the envelope trap, and a
    # policy just read live with zero statements is a vacuous read, not an empty policy.
    if "PolicyDocument" in doc and "Statement" not in doc:
        return None, "the read returned the API ENVELOPE, not the inner document"
    stmts = doc.get("Statement") or []
    if not stmts:
        return None, "the live policy read back with ZERO statements -- refusing a vacuous read"
    out, buckets = set(), set()
    for s in stmts:
        res = s.get("Resource")
        for r in ([res] if isinstance(res, str) else list(res or [])):
            tail = r.split("arn:aws:s3:::", 1)[-1]
            if "/" not in tail:
                continue
            bkt, keypart = tail.split("/", 1)
            buckets.add(bkt)
            out.add(keypart[:-1] if keypart.endswith("*") else keypart)
    return out, {"prefixes": sorted(out), "buckets": sorted(buckets), "statements": len(stmts)}


def registry_bucket(scope: str) -> str:
    text = io.open(REGISTRY_LOCALS, encoding="utf-8").read()
    for line in text.splitlines():
        if '"%s"' % scope in line and "=" in line and "opal-data" in line:
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("REFUSED: no bucket for scope %r in %s" % (scope, REGISTRY_LOCALS))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("gateway")
    ap.add_argument("--live-policy", required=True,
                    help="a file holding the LIVE PolicyDocument of the existing grant, written by "
                         "the aws shim from bash (see the docstring on live_existing_prefixes)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()

    pm = literals(os.path.join(a.gateway, "app", "portal_models.py"))
    mc = literals(os.path.join(a.gateway, "app", "portal_macro.py"))

    # ---- the prefixes the CODE reads ------------------------------------------------------------
    wanted = {}
    for src, lits, names in (("portal_models.SERVED_PREFIXES", pm, ("SERVED_PREFIXES",)),
                             ("portal_macro.SERVED", mc, ("SERVED",))):
        for n in names:
            v = lits.get(n)
            if v is None:
                raise SystemExit("REFUSED: %s not found as a string tuple" % src)
            for p in ([v] if isinstance(v, str) else v):
                wanted.setdefault(p, []).append(src)
    # plus every KEY_/PREFIX_/_*_KEY constant, reduced to its directory -- so a key outside any declared
    # SERVED prefix would still be caught rather than silently ungranted
    for mod, lits in (("portal_models", pm), ("portal_macro", mc)):
        for n, v in lits.items():
            if not isinstance(v, str) or "/" not in v:
                continue
            if not (n.startswith("KEY_") or n.startswith("PREFIX_") or n.endswith("_KEY") or n.endswith("_PREFIX")):
                continue
            wanted.setdefault(as_prefix(v), []).append("%s.%s" % (mod, n))

    code_bucket = pm.get("PORTAL_BUCKET")
    reg_bucket = registry_bucket(SCOPE)

    # ---- agreement 1: three buckets -------------------------------------------------------------
    live_pfx, live_raw = live_existing_prefixes(a.live_policy)
    if live_pfx is None:
        raise SystemExit("REFUSED: cannot read the existing grant live -- %s" % live_raw)
    live_buckets = live_raw["buckets"]
    if not (code_bucket == reg_bucket and live_buckets == [reg_bucket]):
        raise SystemExit("REFUSED: bucket disagreement -- code %r, registry %r, live %r"
                         % (code_bucket, reg_bucket, live_buckets))

    # ---- agreement 2: the .tf and IAM name the same existing prefixes ---------------------------
    tf_pfx = tf_existing_prefixes(EXISTING_TF)
    if tf_pfx != live_pfx:
        raise SystemExit("REFUSED: the existing grant differs between source and world -- .tf %s, live %s"
                         % (sorted(tf_pfx), sorted(live_pfx)))

    # ---- the subtraction -------------------------------------------------------------------------
    residue_all = sorted(p for p in wanted if p and not covered_by(p, live_pfx))
    already = sorted(p for p in wanted if p and covered_by(p, live_pfx))

    # COLLAPSE the residue to its minimal covering set. json-tiered/market-overview/ already covers
    # .../summary/ and .../timeseries/, so three ARNs grant exactly what one grants -- the same reach,
    # a bigger diff, and three lines for a reviewer to check instead of one. The order asks for one
    # resource; this is how that one is DERIVED rather than typed. Both counts are reported, because a
    # collapsed list that hid a non-redundant prefix would be a narrowing, not a tidy-up: the assertion
    # below proves every dropped prefix is covered by a kept one.
    residue = [p for p in residue_all if not any(p != q and p.startswith(q) for q in residue_all)]
    dropped = [p for p in residue_all if p not in residue]
    for p in dropped:
        if not any(p.startswith(q) for q in residue):
            raise SystemExit("REFUSED: collapsing dropped %r without a covering prefix -- that would narrow the grant" % p)

    # ---- agreement 3: non-empty, and no firm token ----------------------------------------------
    if not residue:
        raise SystemExit("REFUSED: the residue is EMPTY -- the existing grant already covers every prefix "
                         "the code reads, so no new policy is needed. That is an answer, not a policy.")
    firms = ("49financial", "inflection", "cottonwood", "demo", "mdpf")
    bad = [p for p in residue for f in firms if f in p]
    if bad:
        raise SystemExit("REFUSED: a firm token appears in a grant prefix: %s" % bad)

    out = {
        "policy_name": POLICY_NAME,
        "policy_name_builder": 'lib/opal_naming.py name("gateway", "global", "portal-tiered-read", "policy")',
        "bucket": reg_bucket,
        "bucket_agreement": {"code_PORTAL_BUCKET": code_bucket, "naming_registry_scope_global": reg_bucket,
                             "live_existing_policy": live_buckets, "all_three_equal": True},
        "role": "aws_iam_role.int_reader (%s)" % EXISTING_ROLE,
        "actions": ["s3:GetObject"],
        "resources": ["arn:aws:s3:::%s/%s*" % (reg_bucket, p) for p in residue],
        "residue_prefixes": residue,
        "residue_before_collapse": residue_all,
        "residue_dropped_as_redundant": dropped,
        "collapse_note": ("every dropped prefix is covered by a kept one, asserted rather than eyeballed, so the "
                          "collapse changes the DIFF and not the reach"),
        "already_covered_prefixes": already,
        "existing_grant_prefixes": sorted(live_pfx),
        "existing_grant_source_equals_world": True,
        "wanted_prefixes_with_provenance": {k: sorted(set(v)) for k, v in sorted(wanted.items()) if k},
        "denominator": {"prefixes_the_code_reads": len([p for p in wanted if p]),
                        "already_covered": len(already),
                        "newly_granted_before_collapse": len(residue_all),
                        "newly_granted": len(residue)},
        "method": ("ast over app/portal_models.py and app/portal_macro.py (module-level str and str-tuple "
                   "assignments only; no import, so no module-level code runs), minus the existing grant's own "
                   "Resource list read BOTH from mcpmsp_internal_reader.tf and LIVE from IAM and required to agree"),
    }
    if a.json:
        io.open(a.json, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
        print("  WROTE %s" % a.json)
    if a.print or not a.json:
        print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
