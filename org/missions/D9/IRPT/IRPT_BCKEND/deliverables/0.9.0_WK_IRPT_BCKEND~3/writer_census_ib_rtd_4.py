#!/usr/bin/env python3
"""IB-rtd-4's WRITER CENSUS: every principal that can write
s3://opal-data-assets/config/mdpf/route_bindings.yaml, read LIVE.

Adapted from IB-rtc-6's writer_census_ib_rtc_6.py (same two-plane method,
same simulator-limits handling) for this key instead of the 49 Financial
directory prefix. Two planes, each read, never assumed:
  RESOURCE plane -- the bucket policy: every statement, and which of them
                    could allow a write or deny one.
  IDENTITY plane -- EVERY IAM role and user in the account, simulated
                    (iam:SimulatePrincipalPolicy) for s3:PutObject on the
                    concrete object ARN, the bucket policy passed as the
                    resource policy so a Deny in it counts. The denominator
                    is every principal listed.

Read-only. Output: one line per writer/reader and a denominator line; --json
writes the rows. --action selects the simulated action (default
s3:PutObject; pass s3:GetObject for the readers-by-grant census).
usage: py -3.12 writer_census_ib_rtd_4.py [--action s3:PutObject|s3:GetObject] [--json out]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

BUCKET = "opal-data-assets"
KEY = "config/mdpf/route_bindings.yaml"


def _as_list(x):
    return [x] if isinstance(x, str) else list(x or [])


def _documents(iam, kind: str, name: str) -> list:
    """Every policy document that applies to the principal: inline, attached managed (default version),
    and, for a user, its groups' inline and attached."""
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


def _matching_allow_statements(iam, kind: str, name: str, key_arn: str, action: str) -> list:
    import fnmatch
    hits = []
    for d in _documents(iam, kind, name):
        for s in _as_list(d.get("Statement")) if isinstance(d.get("Statement"), list) else [d.get("Statement")]:
            if not isinstance(s, dict) or s.get("Effect") != "Allow":
                continue
            acts = [a for a in _as_list(s.get("Action")) if fnmatch.fnmatch(action.lower(), a.lower())]
            res = [r for r in _as_list(s.get("Resource")) if fnmatch.fnmatch(key_arn, r)]
            if acts and res:
                hits.append(s.get("Sid"))
    return hits


def census(action: str = "s3:PutObject"):
    import boto3
    iam = boto3.client("iam")
    s3 = boto3.client("s3", region_name="us-east-1")
    arn = "arn:aws:s3:::%s/%s" % (BUCKET, KEY)
    lines = ["subject: %s on %s" % (action, arn)]
    try:
        bp = s3.get_bucket_policy(Bucket=BUCKET)["Policy"]
        stmts = json.loads(bp)["Statement"]
    except Exception as exc:                           # noqa: BLE001
        bp, stmts = None, []
        lines.append("bucket policy unreadable (%s) -- treated as NO resource-policy grant/deny "
                     "(simulate without ResourcePolicy)" % type(exc).__name__)
    wr = [s.get("Sid") for s in stmts if s.get("Effect") == "Allow"
          and any(a in ("s3:*", action, "*") for a in
                  ([s["Action"]] if isinstance(s.get("Action"), str) else s.get("Action", [])))]
    dn = [s.get("Sid") for s in stmts if s.get("Effect") == "Deny"]
    lines.append("RESOURCE plane: bucket policy %d statement(s); allowing a write: %d %s; Deny: %d %s"
                 % (len(stmts), len(wr), wr, len(dn), dn))
    principals = []
    for page in iam.get_paginator("list_roles").paginate():
        principals += [("role", r["RoleName"], r["Arn"]) for r in page["Roles"]]
    for page in iam.get_paginator("list_users").paginate():
        principals += [("user", u["UserName"], u["Arn"]) for u in page["Users"]]
    import boto3 as _b3
    account = _b3.client("sts").get_caller_identity()["Account"]
    try:
        btags = {t["Key"]: t["Value"] for t in s3.get_bucket_tagging(Bucket=BUCKET).get("TagSet", [])}
    except Exception:                                  # noqa: BLE001
        btags = {}
    list_only = {"s3:prefix", "s3:delimiter", "s3:max-keys"}

    def relevant(k):
        return (k.startswith("aws:") or k.startswith("s3:")) and k not in list_only

    def true_value(k):
        if k in ("aws:ResourceAccount", "aws:PrincipalAccount", "s3:ResourceAccount"):
            return account
        if k == "aws:RequestedRegion":
            return "us-east-1"
        if k.startswith("aws:ResourceTag/") and k.split("/", 1)[1] in btags:
            return btags[k.split("/", 1)[1]]
        return None

    def simulate(**kw):
        """ONE simulation, retried at most twice on a transient error (same throttling
        handling as IB-rtc-6's instrument)."""
        import time
        for attempt in range(3):
            try:
                return iam.simulate_principal_policy(**kw)["EvaluationResults"][0]
            except Exception as exc:                   # noqa: BLE001
                code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
                if attempt == 2 or code in ("NoSuchEntity", "InvalidInput"):
                    raise RuntimeError(code) from exc
                time.sleep(1.5 * (attempt + 1))

    writers, unknown, errors, irrelevant_only, resimulated = [], [], [], 0, 0
    for kind, name, parn in principals:
        kw = dict(PolicySourceArn=parn, ActionNames=[action], ResourceArns=[arn])
        if bp is not None:
            kw["ResourcePolicy"] = bp
        try:
            ev = simulate(**kw)
            miss = [k for k in (ev.get("MissingContextValues") or []) if relevant(k)]
            if ev["EvalDecision"] != "allowed" and ev.get("MissingContextValues") and not miss:
                irrelevant_only += 1
            if ev["EvalDecision"] != "allowed" and miss:
                entries = [{"ContextKeyName": k, "ContextKeyValues": [true_value(k)], "ContextKeyType": "string"}
                           for k in miss if true_value(k) is not None]
                if entries:
                    resimulated += 1
                    kw2 = dict(kw, ContextEntries=entries)
                    ev = simulate(**kw2)
                    miss = [k for k in (ev.get("MissingContextValues") or []) if relevant(k)]
        except Exception as exc:                       # noqa: BLE001
            errors.append((kind, name, str(exc) or type(exc).__name__))
            continue
        if ev["EvalDecision"] == "allowed":
            writers.append((kind, name, parn))
        elif miss:
            unknown.append((kind, name, miss))
    settled = []
    for kind, name, miss in list(unknown):
        if not _matching_allow_statements(iam, kind, name, arn, action):
            settled.append((kind, name))
            unknown.remove((kind, name, miss))
    lines.append("IDENTITY plane: %d principal(s) simulated (%d roles, %d users); %d could not be "
                 "simulated %s" % (len(principals), sum(1 for p in principals if p[0] == "role"),
                                   sum(1 for p in principals if p[0] == "user"), len(errors), errors[:5]))
    lines.append("  conditioned: %d with only keys that cannot occur in a %s request (decision "
                 "stands); %d re-simulated with the request's true context; %d settled by statement "
                 "reading (0 Allow statements match the action and key) %s; %d UNKNOWN %s"
                 % (irrelevant_only, action, resimulated, len(settled), settled, len(unknown),
                    [(k, n, m) for k, n, m in unknown]))
    lines.append("PRINCIPALS: %d of %d may %s %s:"
                 % (len(writers), len(principals), action, arn))
    lines += ["  %-4s %s" % (k, n) for k, n, _ in writers]
    return {"verdict": "EVALUATED", "lines": lines, "bucket": BUCKET, "arn": arn, "action": action,
            "principals": len(principals), "unsimulated": len(errors), "unknown": len(unknown),
            "writers": [{"kind": k, "name": n, "arn": a} for k, n, a in writers]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--action", default="s3:PutObject")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out = census(a.action)
    print("\n".join(out["lines"]))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if out["verdict"] == "EVALUATED" else 2)
