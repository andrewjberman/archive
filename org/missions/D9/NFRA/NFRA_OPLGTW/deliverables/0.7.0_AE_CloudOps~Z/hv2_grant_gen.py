#!/usr/bin/env python
"""OG-hv-2 Phase A step 3: GENERATE infra/aws/terraform/opal-gateway/harvest_read_iam.tf.

The 24 prefixes are READ from `app/harvest_read.py`'s own `SERVED_PREFIXES` tuple by AST, never typed
here and never typed in the .tf. Run this after any SERVED_PREFIXES change; a hand edit to the .tf is
a defect, because the grant's whole claim is that its reach EQUALS what the code serves.

A5 (order amendment, CTO relay msg 34054): `harvest_read.py` reads through `internal_role.s3_client()`
-- the ASSUMED `gateway-global-internal-reader-role` (`INTERNAL_READER_ROLE_ARN`, no fallback) -- so the
one policy attaches to `aws_iam_role.int_reader`, never to the gateway instance role. Cut the other way,
Phase B would deploy green while every served read returned AccessDenied.

Names come from the builder (CLAUDE.md Rule 30), asserted at run time against lib/opal_naming.py rather
than trusted from this docstring:

    name("gateway", "global", "harvest-read", "policy")  -> gateway-global-harvest-read-policy
    the bucket is the same builder output app/harvest_read.py carries (modules/opal_name
    generated_locals.tf, "harvest" = opal-data-harvest)

They are written as LITERALS, not interpolation: the commit-time naming limb grades a new resource
name's own bytes and RAISEs on an unresolved token, so an interpolated name is refused only later, at
apply, after the ledger is open.

Usage: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/hv2_grant_gen.py
       (from the repo root; prints the denominator and the SHA of what it wrote)
"""
from __future__ import annotations

import ast
import hashlib
import io
import os
import sys

SRC = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "harvest_read.py")
OUT = os.path.join("infra", "aws", "terraform", "opal-gateway", "harvest_read_iam.tf")
POLICY_FN = "harvest-read"


def served_prefixes(path: str) -> tuple[str, ...]:
    """SERVED_PREFIXES by AST, so a comment or a docstring mentioning a prefix cannot contribute one."""
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "SERVED_PREFIXES" for t in node.targets):
            vals = tuple(ast.literal_eval(node.value))
            if len(set(vals)) != len(vals):
                raise SystemExit("REFUSED: SERVED_PREFIXES carries a duplicate")
            return vals
    raise SystemExit("REFUSED: no module-level SERVED_PREFIXES assignment in %s" % path)


def bucket(path: str) -> str:
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "BUCKET" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("REFUSED: no module-level BUCKET assignment in %s" % path)


def main() -> int:
    sys.path.insert(0, "lib")
    import opal_naming  # noqa: E402

    prefixes = served_prefixes(SRC)
    bkt = bucket(SRC)
    pol = opal_naming.name("gateway", "global", POLICY_FN, "policy")
    print("  SERVED_PREFIXES read from %s: %d (unique %d)" % (SRC, len(prefixes), len(set(prefixes))))
    print("  bucket from the same file's BUCKET: %s" % bkt)
    print("  builder policy name: %s" % pol)

    obj_lines = "\n".join('          "arn:aws:s3:::%s/%s*",' % (bkt, p) for p in prefixes)
    # Each prefix twice: bare (so a list AT the prefix is admitted) and with the star (so a list BELOW it is).
    # 14 spaces, not 12: `terraform fmt -check -diff` (read-only; -diff ALONE writes) wants the
    # condition values one level deeper than the surrounding `"s3:prefix" = [`.
    cond_lines = "\n".join('              "%s",\n              "%s*",' % (p, p) for p in prefixes)

    body = '''# NFRA_OPLGTW OG-hv-2 (R4, FWD-21): the IAM read grant that app/harvest_read.py's two tools need.
#
# GENERATED -- do not hand edit. Generator:
#   org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/hv2_grant_gen.py
# The %(n)d prefixes below are read by AST from infra/aws/ec2/opal-gateway/app/harvest_read.py's own
# SERVED_PREFIXES, so the grant's reach cannot drift from what the code serves. Re-run the generator
# after a SERVED_PREFIXES change.
#
# WHOSE ROLE (order amendment A5): harvest_read.py reads through internal_role.s3_client(), the ASSUMED
# %(role)s (INTERNAL_READER_ROLE_ARN on the host, no fallback), so the policy
# attaches to aws_iam_role.int_reader in mcpmsp_internal_reader.tf -- never the gateway instance role,
# which is not the identity that makes the S3 call.
#
# NAMES FROM THE BUILDER (CLAUDE.md Rule 30), written as LITERALS because the commit-time naming limb
# grades the resource name's own bytes:
#   lib/opal_naming.py name("gateway", "global", "%(fn)s", "policy") = %(pol)s
#   the bucket is the builder's "harvest" home, the same value app/harvest_read.py BUCKET carries.
#
# WIDTH: read only. s3:GetObject under the %(n)d served prefixes, s3:ListBucket on the bucket itself
# confined by an s3:prefix condition to those same prefixes, and nothing else -- no Put, no Delete, no
# bucket-wide object ARN. Andrew 2026-10-13 ~20:0xZ (call 8): all %(n)d prefixes serve to Opal
# principals, raw included; a non-Opal principal is refused on every prefix by the TOOL, which is the
# gate IAM cannot express.

resource "aws_iam_role_policy" "int_reader_harvest_read" {
  name = "%(pol)s"
  role = aws_iam_role.int_reader.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "HarvestReadServedObjects",
        Effect = "Allow",
        Action = ["s3:GetObject"],
        Resource = [
%(objs)s
        ]
      },
      {
        Sid      = "HarvestListServedPrefixes",
        Effect   = "Allow",
        Action   = ["s3:ListBucket"],
        Resource = ["arn:aws:s3:::%(bkt)s"],
        Condition = {
          StringLike = {
            "s3:prefix" = [
%(conds)s
            ]
          }
        }
      }
    ]
  })
}
''' % {"n": len(prefixes), "role": "gateway-global-internal-reader-role", "fn": POLICY_FN,
       "pol": pol, "bkt": bkt, "objs": obj_lines, "conds": cond_lines}

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(body)
    raw = io.open(OUT, "rb").read()
    non_ascii = sum(1 for ch in body if ord(ch) > 127)
    print("  wrote %s: %d bytes, sha256 %s, non-ASCII characters %d"
          % (OUT, len(raw), hashlib.sha256(raw).hexdigest()[:16], non_ascii))
    print("  object ARNs %d; condition values %d (each prefix bare and starred)"
          % (len(prefixes), 2 * len(prefixes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
