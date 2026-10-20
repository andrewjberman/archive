#!/usr/bin/env python
"""OG-ls-1 Phase A step 1: read the live gateway-family-depth-read-policy and, with iam:SimulatePrincipalPolicy on the live role, record the BEFORE decisions. READ ONLY. Counts, patterns and decisions only.
Writes W/LS_BEFORE.json. usage: python ls1_before.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import time

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
ROLE, POLICY, BUCKET = "opal-gateway-role", "gateway-family-depth-read-policy", "arn:aws:s3:::opal-data-assets"
iam = boto3.client("iam")
doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
sha16 = hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
silver = [s for s in st if s.get("Sid") == "FamilyDepthSilverPrefixListOnly"]
patterns = silver[0]["Condition"]["StringLike"]["s3:prefix"] if silver else None
inline = iam.list_role_policies(RoleName=ROLE)["PolicyNames"]
arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]


def sim(prefix, delimiter=None):
    ctx = [{"ContextKeyName": "s3:prefix", "ContextKeyValues": [prefix], "ContextKeyType": "string"}]
    if delimiter:
        ctx.append({"ContextKeyName": "s3:delimiter", "ContextKeyValues": [delimiter], "ContextKeyType": "string"})
    return iam.simulate_principal_policy(PolicySourceArn=arn, ActionNames=["s3:ListBucket"], ResourceArns=[BUCKET], ContextEntries=ctx)["EvaluationResults"][0]["EvalDecision"]


before_sim = {p: sim(p) for p in ("bloomberg/global/silver/", "gateway/global/silver/", "yahoo/g/silver/", "schwab/x/silver/t/")}
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "policy_sha256_16": sha16, "statements": len(st), "silver_prefix_patterns": patterns,
       "denominator": {"role_inline_policies": len(inline), "policy_present": POLICY in inline, "statement_sids": [s.get("Sid") for s in st]},
       "simulator_before": {"api": "iam:SimulatePrincipalPolicy on the live role, s3:ListBucket on the bucket with s3:prefix = the key, no delimiter", "decisions": before_sim,
                            "expected": {"bloomberg/global/silver/": "allowed", "gateway/global/silver/": "allowed", "yahoo/g/silver/": "allowed", "schwab/x/silver/t/": "allowed"}}}
io.open(W + "LS_BEFORE.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps(rec))
