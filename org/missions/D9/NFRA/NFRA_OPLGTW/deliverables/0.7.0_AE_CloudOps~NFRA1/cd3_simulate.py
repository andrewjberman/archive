#!/usr/bin/env python
"""OG-cd-3 Phase A: the plan's policy document run through iam:SimulateCustomPolicy (a pure read: nothing is created, attached or applied) with the negative controls the ask promises, so the signers see what the grant does
and does NOT allow BEFORE it is applied. The document below is the one the targeted plan prints for aws_iam_role_policy.gw_family_depth_read (family_depth_read_iam.tf at trunk HEAD), transcribed (FOUR statements after amendment A1: the list statement is split and the source-root one carries s3:delimiter = /); Phase B repeats the
same calls against the LIVE policy with simulate-principal-policy. Counts and decisions only.
usage: python cd3_simulate.py <out.json>"""
from __future__ import annotations

import json
import sys
import time

import boto3

ACCT = boto3.client("sts").get_caller_identity()["Account"]
POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {"Sid": "FamilyDepthSweepRuleDescribeOnly", "Effect": "Allow", "Action": ["events:DescribeRule"], "Resource": ["arn:aws:events:us-east-1:%s:rule/opal-assets-silver-*-sweep-daily" % ACCT]},
        {"Sid": "FamilyDepthBackfillStatusReadOnly", "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["arn:aws:s3:::opal-data-assets/*/meta/backfill-status.json"]},
        {"Sid": "FamilyDepthSilverPrefixListOnly", "Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": ["arn:aws:s3:::opal-data-assets"],
         "Condition": {"StringLike": {"s3:prefix": ["*/silver/", "*/silver/*"]}}},
        {"Sid": "FamilyDepthSourceRootListOneLevelOnly", "Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": ["arn:aws:s3:::opal-data-assets"],
         "Condition": {"StringLike": {"s3:prefix": ["schwab/", "orion/", "eclipse/", "blackdiamond/", "trueshares/", "pathfinder/", "msn/", "smartx/"]}, "StringEquals": {"s3:delimiter": "/"}}},
    ],
}
RULE = "arn:aws:events:us-east-1:%s:rule/opal-assets-silver-etf-sweep-daily" % ACCT
OTHER_RULE = "arn:aws:events:us-east-1:%s:rule/some-other-rule" % ACCT
STATUS = "arn:aws:s3:::opal-data-assets/schwab/example-scope/meta/backfill-status.json"
DATA = "arn:aws:s3:::opal-data-assets/schwab/example-scope/silver/example_table/part-0.parquet"
BUCKET = "arn:aws:s3:::opal-data-assets"


def case(name, action, resource, expect, prefix=None, delimiter=None):
    return {"name": name, "action": action, "resource": resource, "expect": expect, "prefix": prefix, "delimiter": delimiter}


CASES = [
    case("describe a silver sweep rule", "events:DescribeRule", RULE, "allowed"),
    case("NEGATIVE: put the same rule", "events:PutRule", RULE, "implicitDeny"),
    case("NEGATIVE: describe a rule outside the pattern", "events:DescribeRule", OTHER_RULE, "implicitDeny"),
    case("get a backfill-status.json", "s3:GetObject", STATUS, "allowed"),
    case("NEGATIVE: put the same key", "s3:PutObject", STATUS, "implicitDeny"),
    case("NEGATIVE: get a data object", "s3:GetObject", DATA, "implicitDeny"),
    case("list a source root WITH delimiter /", "s3:ListBucket", BUCKET, "allowed", "schwab/", "/"),
    case("NEGATIVE: list a source root with NO delimiter", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/", None),
    case("NEGATIVE: list a source root with a delimiter other than /", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/", "-"),
    case("list a silver table prefix with no delimiter (family_depth.py:261 makes this call)", "s3:ListBucket", BUCKET, "allowed", "schwab/example-scope/silver/"),
    case("list a silver table prefix WITH delimiter /", "s3:ListBucket", BUCKET, "allowed", "schwab/example-scope/silver/", "/"),
    case("NEGATIVE: list a gold prefix", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/example-scope/gold/"),
    case("NEGATIVE: list a bronze prefix", "s3:ListBucket", BUCKET, "implicitDeny", "schwab/example-scope/bronze/"),
    case("NEGATIVE: list with no prefix", "s3:ListBucket", BUCKET, "implicitDeny", None),
    case("NEGATIVE: list a source that is not one of the eight", "s3:ListBucket", BUCKET, "implicitDeny", "othersource/"),
    case("NEGATIVE: delete an object", "s3:DeleteObject", STATUS, "implicitDeny"),
    # the glob's breadth, stated honestly in the ask: a prefix with a /silver/ component under ANY first component is admitted
    case("BREADTH: list a bronze-rooted prefix that contains /silver/", "s3:ListBucket", BUCKET, "allowed", "bronze/x/silver/y/"),
]


def main():
    iam = boto3.client("iam")
    out = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "api": "iam:SimulateCustomPolicy (read-only; nothing created or attached)", "results": []}
    for c in CASES:
        kw = {"PolicyInputList": [json.dumps(POLICY)], "ActionNames": [c["action"]], "ResourceArns": [c["resource"]]}
        ctx = []
        if c["prefix"] is not None:
            ctx.append({"ContextKeyName": "s3:prefix", "ContextKeyValues": [c["prefix"]], "ContextKeyType": "string"})
        if c["delimiter"] is not None:
            ctx.append({"ContextKeyName": "s3:delimiter", "ContextKeyValues": [c["delimiter"]], "ContextKeyType": "string"})
        if ctx:
            kw["ContextEntries"] = ctx
        r = iam.simulate_custom_policy(**kw)["EvaluationResults"][0]
        out["results"].append({"name": c["name"], "action": c["action"], "decision": r["EvalDecision"], "expected": c["expect"], "ok": r["EvalDecision"] == c["expect"]})
    out["all_as_expected"] = all(x["ok"] for x in out["results"])
    out["cases"] = len(out["results"])
    with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=1) + "\n")
    for x in out["results"]:
        print("%-62s %-12s %s" % (x["name"], x["decision"], "ok" if x["ok"] else "MISMATCH (want %s)" % x["expected"]))
    print("all as expected:", out["all_as_expected"], "of", out["cases"])


if __name__ == "__main__":
    main()
