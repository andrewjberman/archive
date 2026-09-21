#!/usr/bin/env python3
"""IB-rte-1 arm (d): WHO CAN CREATE OR MODIFY A TEST PRINCIPAL -- the identity plane, read LIVE.

The IDENTITY OBJECT that makes a principal a FIRM_ADVISOR of one firm is a row in DynamoDB
table `opal-users-v2` (the production authentication plane; row RT2_test_principal_human_gated.md
"where a principal lives"). This module is `writer_census_ib_rtc_6.py`'s pattern (R-44's
RESOURCE + IDENTITY plane census), ADAPTED from an S3 PutObject subject to a DynamoDB
PutItem/UpdateItem subject on that table.

TWO PLANES, EACH READ, NEVER ASSUMED:
  RESOURCE plane -- the table's own resource policy (DynamoDB tables carry none by default;
                     read via `dynamodb:GetResourcePolicy` when present, absence is reported).
  IDENTITY plane -- EVERY IAM role and user in the account, simulated for `dynamodb:PutItem`
                     AND `dynamodb:UpdateItem` on the table ARN.

THE BLIND SPOT, STATED RATHER THAN DISCOVERED LATE (the face's own words): this census is
IAM-shaped. An identity PROVIDER's own ADMIN SURFACE is not IAM -- if `opal-users-v2` rows are
created only through an application-level signup/admin Lambda (`auth-handler`) rather than by
direct table access, the set of humans/services who can REACH that Lambda's mint path is a
DIFFERENT population than the set of IAM principals this script can see, and this script cannot
enumerate it. It is named here, not measured, because measuring it needs the Lambda's own
authorization surface (a second census this cell does not run).

Read-only. No item is written. No credential value is read or printed.
usage: py -3.12 identity_writer_census_ib_rte_1.py [--json out]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

TABLE_NAME = "opal-users-v2"
ACTIONS = ("dynamodb:PutItem", "dynamodb:UpdateItem")


def _as_list(x):
    return [x] if isinstance(x, str) else list(x or [])


def _documents(iam, kind, name):
    import urllib.parse
    docs, attached = [], []
    if kind == "role":
        for n in iam.list_role_policies(RoleName=name)["PolicyNames"]:
            docs.append(iam.get_role_policy(RoleName=name, PolicyName=n)["PolicyDocument"])
        attached = iam.list_attached_role_policies(RoleName=name)["AttachedPolicies"]
    else:
        for n in iam.list_user_policies(UserName=name)["PolicyNames"]:
            docs.append(iam.get_user_policy(UserName=name, PolicyName=n)["PolicyDocument"])
        attached = list(iam.list_attached_user_policies(UserName=name)["AttachedPolicies"])
        for g in iam.list_groups_for_user(UserName=name)["Groups"]:
            for n in iam.list_group_policies(GroupName=g["GroupName"])["PolicyNames"]:
                docs.append(iam.get_group_policy(GroupName=g["GroupName"], PolicyName=n)["PolicyDocument"])
            attached += iam.list_attached_group_policies(GroupName=g["GroupName"])["AttachedPolicies"]
    for a in attached:
        v = iam.get_policy(PolicyArn=a["PolicyArn"])["Policy"]["DefaultVersionId"]
        docs.append(iam.get_policy_version(PolicyArn=a["PolicyArn"], VersionId=v)["PolicyVersion"]["Document"])
    return [json.loads(urllib.parse.unquote(d)) if isinstance(d, str) else d for d in docs]


def _matching_allow_statements(iam, kind, name, table_arn):
    import fnmatch
    hits = []
    for d in _documents(iam, kind, name):
        stmts = d.get("Statement")
        stmts = stmts if isinstance(stmts, list) else [stmts]
        for s in stmts:
            if not isinstance(s, dict) or s.get("Effect") != "Allow":
                continue
            acts = [a for act in ACTIONS for a in _as_list(s.get("Action"))
                    if fnmatch.fnmatch(act.lower(), a.lower())]
            res = [r for r in _as_list(s.get("Resource"))
                   if fnmatch.fnmatch(table_arn, r) or fnmatch.fnmatch(table_arn + "/*", r)]
            if acts and res:
                hits.append(s.get("Sid"))
    return hits


def census(json_out=None):
    import boto3
    iam = boto3.client("iam")
    ddb = boto3.client("dynamodb", region_name="us-east-1")

    desc = ddb.describe_table(TableName=TABLE_NAME)["Table"]
    table_arn = desc["TableArn"]
    lines = ["subject: %s on %s (table status=%s, item_count=%s)"
             % (" / ".join(ACTIONS), table_arn, desc["TableStatus"], desc.get("ItemCount"))]

    try:
        rp = ddb.get_resource_policy(ResourceArn=table_arn)
        lines.append("RESOURCE plane: a resource policy IS attached (RevisionId %s)" % rp.get("RevisionId"))
        rp_doc = json.loads(rp["Policy"])
    except ddb.exceptions.PolicyNotFoundException:
        lines.append("RESOURCE plane: no resource-based policy on this table (DynamoDB default; "
                     "authorization is identity-plane only unless one is attached)")
        rp_doc = None
    except Exception as exc:                                   # noqa: BLE001
        lines.append("RESOURCE plane: unreadable (%s)" % type(exc).__name__)
        rp_doc = None

    principals = []
    for page in iam.get_paginator("list_roles").paginate():
        principals += [("role", r["RoleName"], r["Arn"]) for r in page["Roles"]]
    for page in iam.get_paginator("list_users").paginate():
        principals += [("user", u["UserName"], u["Arn"]) for u in page["Users"]]

    list_only_like_keys = {"dynamodb:LeadingKeys", "dynamodb:Select", "dynamodb:Attributes"}

    def relevant(k):
        return not k.startswith("dynamodb:") or k not in list_only_like_keys

    def simulate_all(parn):
        """Every EvaluationResult for ACTIONS on this principal, retried at most twice on a
        transient error (the same pattern `writer_census_ib_rtc_6.py` uses)."""
        import time
        for attempt in range(3):
            try:
                return iam.simulate_principal_policy(
                    PolicySourceArn=parn, ActionNames=list(ACTIONS), ResourceArns=[table_arn]
                )["EvaluationResults"]
            except Exception as exc:                            # noqa: BLE001
                code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
                if attempt == 2 or code in ("NoSuchEntity", "InvalidInput"):
                    raise RuntimeError(code) from exc
                time.sleep(1.5 * (attempt + 1))

    writers, unknown, errors = [], [], []
    for kind, name, parn in principals:
        # `simulate_principal_policy` returns ONE EvaluationResult per ActionName when given a
        # list of actions; read them all rather than only the first.
        writers_this = False
        miss_this = []
        try:
            results = simulate_all(parn)
        except Exception as exc:                                # noqa: BLE001
            errors.append((kind, name, str(exc) or type(exc).__name__))
            continue
        for r in results:
            if r["EvalDecision"] == "allowed":
                writers_this = True
            miss_this += [k for k in (r.get("MissingContextValues") or []) if relevant(k)]
        if writers_this:
            writers.append((kind, name, parn))
        elif miss_this:
            unknown.append((kind, name, sorted(set(miss_this))))

    settled = []
    for kind, name, miss in list(unknown):
        if not _matching_allow_statements(iam, kind, name, table_arn):
            settled.append((kind, name))
            unknown.remove((kind, name, miss))

    lines.append("IDENTITY plane: %d principal(s) simulated (%d roles, %d users); %d could not be "
                 "simulated %s" % (len(principals), sum(1 for p in principals if p[0] == "role"),
                                   sum(1 for p in principals if p[0] == "user"), len(errors), errors[:5]))
    lines.append("  settled by statement reading (0 Allow statements match the action and resource): "
                 "%d %s; UNKNOWN (a condition key this script cannot resolve): %d %s"
                 % (len(settled), settled, len(unknown), [(k, n, m) for k, n, m in unknown]))
    lines.append("WRITERS: %d of %d principals may PutItem/UpdateItem on %s:"
                 % (len(writers), len(principals), TABLE_NAME))
    lines += ["  %-4s %s" % (k, n) for k, n, _ in writers]
    lines.append("BLIND SPOT (named, not measured): an identity provider's own admin surface "
                 "(the auth-handler Lambda's signup/admin path) is not IAM; this census cannot "
                 "see who can reach it.")

    out = {"verdict": "EVALUATED", "lines": lines, "table_arn": table_arn,
           "resource_policy_present": rp_doc is not None,
           "principals": len(principals), "unsimulated": len(errors), "unknown": len(unknown),
           "writers": [{"kind": k, "name": n, "arn": a} for k, n, a in writers]}
    if json_out:
        pathlib.Path(json_out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    result = census(a.json)
    print("\n".join(result["lines"]))
    sys.exit(0 if result["verdict"] == "EVALUATED" else 2)
