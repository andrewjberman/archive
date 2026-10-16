#!/usr/bin/env python
"""OG-ap-21 Phase B: the LIVE IAM capture of both gateway roles, run BEFORE and AFTER each act.

One script, one shape, three uses:
  --label preact      the pre-act capture, with the four presence probes the two applies assume
  --label post-news   after the news policy apply
  --label post-invoke after the invoke policy apply
  --label pre-destroy / post-destroy   the two halves of the destroy leg

WHY EVERY DOCUMENT IS CAPTURED, NOT JUST THE ONES I TOUCH: the destroy leg owes a proof that the
instance role's OTHER statements did not move, and that proof is only available if a BEFORE capture
of all of them exists. 25 extra reads now is the whole cost of being able to say it later.

GUARDS this script will not run without (cloud-ops apply-side trap 2, measured 2026-10-12):
  - a captured document that carries a top-level `PolicyDocument` key is the API ENVELOPE, not the
    document a put-role-policy will replay. REFUSED.
  - a document with zero statements, just read live, is a vacuous read that once made a script print
    "the document would be empty -> delete-role-policy". REFUSED.

An error is a VALUE here: a missing policy returns the string ABSENT_NoSuchEntity, never an empty
dict that reads the same as a present-but-empty one.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json

import boto3
from botocore.exceptions import ClientError

ROLE_GW = "opal-gateway-role"                                  # aws_iam_role.gw, the EC2 instance role
ROLE_IR = "gateway-global-internal-reader-role"                # aws_iam_role.int_reader, the assumed reader
NEW_NEWS = "gateway-global-news-read-internal-policy"          # leg news-policy adds this to ROLE_IR
NEW_INVOKE = "gateway-global-harvest-published-invoke-policy"  # leg invoke-policy adds this to ROLE_IR
OLD_NEWS = "gateway-global-news-read-policy"                   # leg destroy-old removes this from ROLE_GW
PUBLISHED_FN = "opal-amgt-scoped-api"
NEWS_TABLES = ["opal-news-articles", "opal-news-trending-daily", "opal-keyword-intelligence"]
NEWS_INDEX = ("opal-keyword-intelligence", "date-index")

iam = boto3.client("iam")


def canon(doc) -> str:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def guard(doc, where: str) -> None:
    if isinstance(doc, dict) and "PolicyDocument" in doc and "Statement" not in doc:
        raise SystemExit("REFUSED: %s captured the API ENVELOPE, not the document (trap 2)" % where)
    stmts = doc.get("Statement") if isinstance(doc, dict) else None
    if not stmts:
        raise SystemExit("REFUSED: %s read ZERO statements live -- a vacuous read, not an empty policy" % where)


def inline_names(role: str):
    names, pages = [], 0
    for page in iam.get_paginator("list_role_policies").paginate(RoleName=role):
        pages += 1
        names.extend(page.get("PolicyNames", []))
    return sorted(names), pages


def attached(role: str):
    arns, pages = [], 0
    for page in iam.get_paginator("list_attached_role_policies").paginate(RoleName=role):
        pages += 1
        arns.extend(p["PolicyArn"] for p in page.get("AttachedPolicies", []))
    return sorted(arns), pages


def probe(role: str, policy: str):
    try:
        r = iam.get_role_policy(RoleName=role, PolicyName=policy)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "?")
        return {"state": "ABSENT_NoSuchEntity" if code == "NoSuchEntity" else "ERROR:" + code,
                "document": None, "canon_sha256": None}
    doc = r["PolicyDocument"]
    guard(doc, "%s/%s" % (role, policy))
    c = canon(doc)
    return {"state": "PRESENT", "document": doc, "canon_sha256": hashlib.sha256(c.encode()).hexdigest()[:16],
            "statement_count": len(doc["Statement"]),
            "actions": sorted({a for s in doc["Statement"] for a in ([s["Action"]] if isinstance(s.get("Action"), str) else s.get("Action", []))}),
            "resources": sorted({a for s in doc["Statement"] for a in ([s["Resource"]] if isinstance(s.get("Resource"), str) else s.get("Resource", []))})}


def role_capture(role: str):
    names, npages = inline_names(role)
    arns, apages = attached(role)
    docs = {}
    for n in names:
        docs[n] = probe(role, n)
    return {"role": role, "inline_count": len(names), "inline_pages": npages, "inline_names": names,
            "attached_count": len(arns), "attached_pages": apages, "attached_arns": arns,
            "documents": docs,
            "canon_sha256_by_name": {k: v["canon_sha256"] for k, v in docs.items()}}


ap = argparse.ArgumentParser()
ap.add_argument("--label", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--probes", action="store_true", help="run the four presence probes and the existence reads")
a = ap.parse_args()

out = {"label": a.label, "identity": boto3.client("sts").get_caller_identity()["Arn"],
       "roles": {ROLE_GW: role_capture(ROLE_GW), ROLE_IR: role_capture(ROLE_IR)}}

if a.probes:
    out["probes"] = {
        "IR/%s" % NEW_NEWS: probe(ROLE_IR, NEW_NEWS)["state"],
        "IR/%s" % NEW_INVOKE: probe(ROLE_IR, NEW_INVOKE)["state"],
        "GW/%s" % NEW_INVOKE: probe(ROLE_GW, NEW_INVOKE)["state"],
        "GW/%s" % OLD_NEWS: probe(ROLE_GW, OLD_NEWS)["state"],
    }
    # EXISTENCE, not simulation: an iam simulate returns `allowed` for a resource nothing created
    # (cloud-ops false-allow mode, measured 2026-10-07). These are the reads that bound that.
    ex = {}
    try:
        cfg = boto3.client("lambda").get_function_configuration(FunctionName=PUBLISHED_FN)
        ex["lambda/" + PUBLISHED_FN] = {"exists": True, "arn": cfg["FunctionArn"]}
    except ClientError as exc:
        ex["lambda/" + PUBLISHED_FN] = {"exists": False, "code": exc.response.get("Error", {}).get("Code")}
    ddb = boto3.client("dynamodb")
    for t in NEWS_TABLES:
        try:
            d = ddb.describe_table(TableName=t)["Table"]
            ex["ddb/" + t] = {"exists": True, "arn": d["TableArn"],
                              "gsi": sorted(g["IndexName"] for g in d.get("GlobalSecondaryIndexes", []))}
        except ClientError as exc:
            ex["ddb/" + t] = {"exists": False, "code": exc.response.get("Error", {}).get("Code")}
    tgt = ex.get("ddb/" + NEWS_INDEX[0], {})
    ex["ddb_index/%s/%s" % NEWS_INDEX] = {"exists": NEWS_INDEX[1] in tgt.get("gsi", []),
                                          "gsi_denominator": len(tgt.get("gsi", []))}
    out["existence"] = ex

io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1, default=str) + "\n")
print("WROTE %s  (%s)" % (a.out, a.label))
print("  %s: %d inline, %d attached" % (ROLE_GW, out["roles"][ROLE_GW]["inline_count"], out["roles"][ROLE_GW]["attached_count"]))
print("  %s: %d inline, %d attached" % (ROLE_IR, out["roles"][ROLE_IR]["inline_count"], out["roles"][ROLE_IR]["attached_count"]))
if a.probes:
    for k, v in out["probes"].items():
        print("  PROBE %-70s %s" % (k, v))
    for k, v in out["existence"].items():
        print("  EXIST %-70s %s" % (k, json.dumps(v, default=str)))
