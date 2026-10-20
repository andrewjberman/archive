#!/usr/bin/env python
"""OG-ls-1 Phase A step 4: the plan's AFTER policy document run through iam:SimulateCustomPolicy (a pure read: nothing is created, attached or applied; the live role is untouched).
The document is the LIVE policy (get-role-policy) with ONLY the silver list replaced by the per-source forms built from `local.family_depth_sources` parsed out of the committed .tf, so the three other statements are the live bytes.
usage: python ls1_simulate.py   (repository root)  -> W/LS_SIMULATE_PLAN.json"""
from __future__ import annotations

import io
import json
import re
import time

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
TF = "infra/aws/terraform/opal-gateway/family_depth_read_iam.tf"
ROLE, POLICY, BUCKET = "opal-gateway-role", "gateway-family-depth-read-policy", "arn:aws:s3:::opal-data-assets"
iam = boto3.client("iam")
sources = re.findall(r'"([a-z]+)"', re.search(r"family_depth_sources\s*=\s*\[(.*?)\]", io.open(TF, encoding="utf-8").read(), re.S).group(1))
doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
for st in doc["Statement"]:
    if st["Sid"] == "FamilyDepthSilverPrefixListOnly":
        st["Condition"]["StringLike"]["s3:prefix"] = [p for s in sources for p in ("%s/*/silver/" % s, "%s/*/silver/*" % s)]
acct = boto3.client("sts").get_caller_identity()["Account"]
RULE = "arn:aws:events:us-east-1:%s:rule/opal-assets-silver-etf-sweep-daily" % acct
STATUS = "arn:aws:s3:::opal-data-assets/schwab/example-scope/meta/backfill-status.json"

CASES = [
    ("ALLOWED: silver table list under a source", "s3:ListBucket", BUCKET, "allowed", "schwab/x/silver/t/", None),
    ("ALLOWED: silver table list under a source, with delimiter /", "s3:ListBucket", BUCKET, "allowed", "smartx/x/silver/t/", "/"),
    ("NEGATIVE: silver list under bloomberg", "s3:ListBucket", BUCKET, "implicitDeny", "bloomberg/global/silver/", None),
    ("NEGATIVE: silver list under gateway", "s3:ListBucket", BUCKET, "implicitDeny", "gateway/global/silver/", None),
    ("NEGATIVE: silver list under yahoo", "s3:ListBucket", BUCKET, "implicitDeny", "yahoo/g/silver/", None),
    ("NEGATIVE: silver list under commonwealth", "s3:ListBucket", BUCKET, "implicitDeny", "commonwealth/cottonwood/silver/", None),
    ("NEGATIVE: list a source root with NO delimiter", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/", None),
    ("ALLOWED: list a source root WITH delimiter /", "s3:ListBucket", BUCKET, "allowed", "schwab/", "/"),
    ("NEGATIVE: bronze-rooted prefix with a /silver/ component", "s3:ListBucket", BUCKET, "implicitDeny", "bronze/x/silver/y/", None),
    ("NEGATIVE: gold prefix under a source", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/x/gold/", None),
    ("unchanged: describe a silver sweep rule", "events:DescribeRule", RULE, "allowed", None, None),
    ("NEGATIVE: put the same rule", "events:PutRule", RULE, "implicitDeny", None, None),
    ("unchanged: get a backfill-status.json", "s3:GetObject", STATUS, "allowed", None, None),
    ("NEGATIVE: put the same key", "s3:PutObject", STATUS, "implicitDeny", None, None),
]
out = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "api": "iam:SimulateCustomPolicy (read-only; nothing created or attached)", "document": "the live policy with only the silver list replaced by the per-source forms of %d sources parsed from the committed .tf" % len(sources),
       "results": []}
for name, action, resource, expect, prefix, delimiter in CASES:
    ctx = []
    if prefix is not None:
        ctx.append({"ContextKeyName": "s3:prefix", "ContextKeyValues": [prefix], "ContextKeyType": "string"})
    if delimiter is not None:
        ctx.append({"ContextKeyName": "s3:delimiter", "ContextKeyValues": [delimiter], "ContextKeyType": "string"})
    kw = {"PolicyInputList": [json.dumps(doc)], "ActionNames": [action], "ResourceArns": [resource]}
    if ctx:
        kw["ContextEntries"] = ctx
    r = iam.simulate_custom_policy(**kw)["EvaluationResults"][0]
    out["results"].append({"name": name, "action": action, "prefix": prefix, "delimiter": delimiter, "decision": r["EvalDecision"], "expected": expect, "ok": r["EvalDecision"] == expect})
out["all_as_expected"] = all(x["ok"] for x in out["results"])
out["cases"] = len(out["results"])
io.open(W + "LS_SIMULATE_PLAN.json", "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
for x in out["results"]:
    print("%-66s %-12s %s" % (x["name"], x["decision"], "ok" if x["ok"] else "MISMATCH (want %s)" % x["expected"]))
print("all as expected:", out["all_as_expected"], "of", out["cases"], "| sources", len(sources))
