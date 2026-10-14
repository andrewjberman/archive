"""check_ar1_grant.py -- acceptance for AMGT-ar-1 (the adapter role's read grant for the AI-fill prefix), read from the LIVE role policy.

  PYTHONPATH=<repo root> python check_ar1_grant.py [--pre-sha 77c69f8359764942]
Reads `opal-amgt-scoped-api-role`'s inline policy `opal-amgt-scoped-api-grants` (iam:GetRolePolicy, read-only) and prints
`AIFILL AR-1 GRANT: YES|NO (...)`. The prefix is `_harvest_prefixes.AI_FILL_GOLD_PREFIX` (the generated constant), never typed here.
The control: with the ONE new entry removed from each limb, the canonical sha16 of the policy equals the pre-act sha (so nothing else moved).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys

ROLE = "opal-amgt-scoped-api-role"
POLICY = "opal-amgt-scoped-api-grants"
BUCKET_ARN = "arn:aws:s3:::opal-data-harvest"


def canon_sha16(doc):
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre-sha", default="77c69f8359764942")
    ap.add_argument("--pre-statements", type=int, default=7)
    ap.add_argument("--pre-pool-resources", type=int, default=34)
    args = ap.parse_args()
    import boto3

    from lib.research.api import _harvest_prefixes as hp

    prefix = hp.AI_FILL_GOLD_PREFIX
    arn = "%s/%s*" % (BUCKET_ARN, prefix)
    cond = prefix + "*"
    doc = boto3.client("iam").get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    rows = []

    def arm(name, ok, detail=""):
        rows.append(ok)
        print("ARM %-70s %s %s" % (name, "PASS" if ok else "FAIL", str(detail)[:140]))

    statements = doc["Statement"]
    arm("the policy still has the pre-act statement count", len(statements) == args.pre_statements, len(statements))
    get_stmt = [s for s in statements if s.get("Sid") == "ReadThePoolPrefixesTheAdapterReads"]
    list_stmt = [s for s in statements if s.get("Sid") == "ListOnlyThePoolPrefixesTheAdapterReads"]
    arm("the two named statements exist once each", len(get_stmt) == 1 and len(list_stmt) == 1, (len(get_stmt), len(list_stmt)))
    if len(get_stmt) != 1 or len(list_stmt) != 1:
        print("AIFILL AR-1 GRANT: NO (%d of %d)" % (sum(rows), len(rows)))
        return 1
    resources = get_stmt[0]["Resource"] if isinstance(get_stmt[0]["Resource"], list) else [get_stmt[0]["Resource"]]
    prefixes = list_stmt[0]["Condition"]["StringLike"]["s3:prefix"]
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    arm("GetObject limb: the AI-fill prefix is granted exactly once", resources.count(arn) == 1, arn)
    arm("GetObject limb: one resource more than before", len(resources) == args.pre_pool_resources + 1, len(resources))
    arm("ListBucket limb: the AI-fill prefix condition is present exactly once", prefixes.count(cond) == 1, cond)
    arm("the new entry is object-scoped: it ends with the prefix and a star, never a bare bucket", arn.endswith(prefix + "*") and not arn.endswith("opal-data-harvest/*"), arn)
    stripped = json.loads(json.dumps(doc))
    for s in stripped["Statement"]:
        if s.get("Sid") == "ReadThePoolPrefixesTheAdapterReads":
            s["Resource"] = [r for r in s["Resource"] if r != arn]
        if s.get("Sid") == "ListOnlyThePoolPrefixesTheAdapterReads":
            s["Condition"]["StringLike"]["s3:prefix"] = [p for p in s["Condition"]["StringLike"]["s3:prefix"] if p != cond]
    sha = canon_sha16(stripped)
    arm("with the one entry removed from each limb the policy is byte-equal to the pre-act policy", sha == args.pre_sha, "%s vs %s" % (sha, args.pre_sha))
    ok = all(rows)
    print("AIFILL AR-1 GRANT: %s (%d of %d)" % ("YES" if ok else "NO", sum(rows), len(rows)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
