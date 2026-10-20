#!/usr/bin/env python
"""OG-ls-1 Phase B step 3: read the narrowed policy BACK from IAM and simulate against the LIVE role (iam:SimulatePrincipalPolicy; nothing written). READ ONLY.
Real samples are found by a list walk (schwab/ one level, then its first scope's silver/ one level) and an events list-rules, never typed.
Writes W/LS_LIVE.json (decisions, counts, the samples). usage: python ls1_phaseb.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import time

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
ROLE, POLICY, BUCKET, ARN_B = "opal-gateway-role", "gateway-family-depth-read-policy", "opal-data-assets", "arn:aws:s3:::opal-data-assets"
iam, s3, ev = boto3.client("iam"), boto3.client("s3"), boto3.client("events", region_name="us-east-1")
doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
sha16 = hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
acts = sorted({a for s in st for a in ([s["Action"]] if isinstance(s["Action"], str) else s["Action"])})
silver = [s for s in st if s["Sid"] == "FamilyDepthSilverPrefixListOnly"][0]["Condition"]["StringLike"]["s3:prefix"]
sources = ["schwab", "orion", "eclipse", "blackdiamond", "trueshares", "pathfinder", "msn", "smartx"]
want = sorted(p for s in sources for p in ("%s/*/silver/" % s, "%s/*/silver/*" % s))
shape = {"statements": len(st), "all_allow": all(s["Effect"] == "Allow" for s in st), "actions": acts, "silver_patterns": len(silver), "silver_patterns_equal_the_sixteen": sorted(silver) == want, "any_pattern_starts_with_star": any(p.startswith("*") for p in silver)}
shape["ok"] = shape["statements"] == 4 and shape["all_allow"] and acts == ["events:DescribeRule", "s3:GetObject", "s3:ListBucket"] and shape["silver_patterns_equal_the_sixteen"] and not shape["any_pattern_starts_with_star"]

scopes = [p["Prefix"] for p in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/", Delimiter="/", MaxKeys=5).get("CommonPrefixes", [])]
sample_silver = None
for sc in scopes:
    tabs = [p["Prefix"] for p in s3.list_objects_v2(Bucket=BUCKET, Prefix=sc + "silver/", Delimiter="/", MaxKeys=5).get("CommonPrefixes", [])]
    if tabs:
        sample_silver, sample_scope = tabs[0], sc
        break
status_key = sample_scope + "meta/backfill-status.json"
status_exists = bool(s3.list_objects_v2(Bucket=BUCKET, Prefix=status_key, MaxKeys=1).get("KeyCount"))
rules = ev.list_rules(NamePrefix="opal-assets-silver-").get("Rules", [])
rule_arn = [r["Arn"] for r in rules if r["Name"].endswith("-sweep-daily")][0]
role_arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
key_arn = "%s/%s" % (ARN_B, status_key)


def sim(action, resource, prefix=None, delimiter=None):
    ctx = []
    if prefix is not None:
        ctx.append({"ContextKeyName": "s3:prefix", "ContextKeyValues": [prefix], "ContextKeyType": "string"})
    if delimiter is not None:
        ctx.append({"ContextKeyName": "s3:delimiter", "ContextKeyValues": [delimiter], "ContextKeyType": "string"})
    kw = {"PolicySourceArn": role_arn, "ActionNames": [action], "ResourceArns": [resource]}
    if ctx:
        kw["ContextEntries"] = ctx
    return iam.simulate_principal_policy(**kw)["EvaluationResults"][0]["EvalDecision"]


cases = [("silver list under a source (real prefix)", "s3:ListBucket", ARN_B, sample_silver, None, "allowed"),
         ("silver list under bloomberg", "s3:ListBucket", ARN_B, "bloomberg/global/silver/", None, "implicitDeny"),
         ("silver list under gateway", "s3:ListBucket", ARN_B, "gateway/global/silver/", None, "implicitDeny"),
         ("silver list under yahoo", "s3:ListBucket", ARN_B, "yahoo/g/silver/", None, "implicitDeny"),
         ("silver list under commonwealth", "s3:ListBucket", ARN_B, "commonwealth/cottonwood/silver/", None, "implicitDeny"),
         ("root list WITH delimiter", "s3:ListBucket", ARN_B, "schwab/", "/", "allowed"),
         ("root list with NO delimiter", "s3:ListBucket", ARN_B, "schwab/", None, "implicitDeny"),
         ("DescribeRule on a real sweep rule", "events:DescribeRule", rule_arn, None, None, "allowed"),
         ("GetObject on a real backfill-status key", "s3:GetObject", key_arn, None, None, "allowed"),
         ("PutRule on the same rule", "events:PutRule", rule_arn, None, None, "implicitDeny"),
         ("PutObject on the same key", "s3:PutObject", key_arn, None, None, "implicitDeny")]
results = []
for name, action, res, pre, dl, expect in cases:
    d = sim(action, res, pre, dl)
    results.append({"name": name, "action": action, "decision": d, "expected": expect, "ok": d == expect or (expect == "implicitDeny" and d == "explicitDeny")})
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "policy_name": POLICY, "policy_sha256_16": sha16, "shape": shape, "inline_policies_on_role": len(iam.list_role_policies(RoleName=ROLE)["PolicyNames"]),
       "samples": {"sample_silver_prefix": sample_silver, "sample_status_key_exists": status_exists, "sample_status_key_arn": key_arn, "sample_rule_arn": rule_arn, "sample_root_prefix": "schwab/"},
       "api": "iam:SimulatePrincipalPolicy on the live role", "results": results, "all_as_expected": all(r["ok"] for r in results) and shape["ok"] and status_exists}
io.open(W + "LS_LIVE.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({"policy_sha256_16": sha16, "shape": shape, "inline": rec["inline_policies_on_role"], "sample_silver_prefix_depth": sample_silver.count("/"), "status_exists": status_exists, "all_as_expected": rec["all_as_expected"]}))
for r in results:
    print("%-48s %-13s %s" % (r["name"], r["decision"], "ok" if r["ok"] else "MISMATCH (want %s)" % r["expected"]))
