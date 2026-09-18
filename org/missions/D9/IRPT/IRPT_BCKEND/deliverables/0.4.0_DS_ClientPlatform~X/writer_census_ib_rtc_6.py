#!/usr/bin/env python3
"""R-44's WRITER CENSUS: every principal that can write the 49 Financial directory prefix, read LIVE.

The 49 Financial directory lands in the firm registry's destination bucket (data/firm_registry.json:
49financial -> its `bucket`, the LEGACY opal-data-bd until D14) under investor-reporting/directory/.
Two planes, each read, never assumed:
  RESOURCE plane -- the bucket policy: every statement, and which of them could allow a write or deny one.
  IDENTITY plane -- EVERY IAM role and user in the account, simulated (iam:SimulatePrincipalPolicy) for
                    s3:PutObject on a concrete key under the prefix, the bucket policy passed as the
                    resource policy so a Deny in it counts. The denominator is every principal listed.
Then the NEW principal (not yet applied) is simulated from its PLANNED policy document
(iam:SimulateCustomPolicy), and must be implicitDeny.

Read-only. Output: one line per writer and a denominator line; `--json` writes the rows.
usage: py -3.12 writer_census_ib_rtc_6.py [--planned-policy <file with the planned JSON policy>] [--json out]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

WS = pathlib.Path(__file__).resolve().parents[7]
PREFIX = "investor-reporting/directory"
PROBE_KEY_TAIL = "2099-01-01/directory.json"      # a concrete key under the prefix; nothing is written
ACTION = "s3:PutObject"


def destination_bucket(firm_id: str = "49financial") -> str:
    reg = json.loads((WS / "data" / "firm_registry.json").read_text(encoding="utf-8"))
    return next(f["bucket"] for f in reg["firms"] if f["firm_id"] == firm_id)


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


def _matching_allow_statements(iam, kind: str, name: str, key_arn: str) -> list:
    import fnmatch
    hits = []
    for d in _documents(iam, kind, name):
        for s in _as_list(d.get("Statement")) if isinstance(d.get("Statement"), list) else [d.get("Statement")]:
            if not isinstance(s, dict) or s.get("Effect") != "Allow":
                continue
            acts = [a for a in _as_list(s.get("Action")) if fnmatch.fnmatch(ACTION.lower(), a.lower())]
            res = [r for r in _as_list(s.get("Resource")) if fnmatch.fnmatch(key_arn, r)]
            if acts and res:
                hits.append(s.get("Sid"))
    return hits


def census(planned_policy: "str | None" = None):
    import boto3
    iam = boto3.client("iam")
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = destination_bucket()
    arn = "arn:aws:s3:::%s/%s/%s" % (bucket, PREFIX, PROBE_KEY_TAIL)
    lines = ["subject: %s on %s (bucket from data/firm_registry.json, prefix %s/)" % (ACTION, arn, PREFIX)]
    try:
        bp = s3.get_bucket_policy(Bucket=bucket)["Policy"]
        stmts = json.loads(bp)["Statement"]
    except Exception as exc:                           # noqa: BLE001
        return {"verdict": "NOT-EVALUATED", "lines": lines + ["bucket policy unreadable: %s" % type(exc).__name__]}
    wr = [s.get("Sid") for s in stmts if s.get("Effect") == "Allow"
          and any(a in ("s3:*", "s3:PutObject", "*") for a in
                  ([s["Action"]] if isinstance(s.get("Action"), str) else s.get("Action", [])))]
    dn = [s.get("Sid") for s in stmts if s.get("Effect") == "Deny"]
    lines.append("RESOURCE plane: bucket policy %d statement(s); allowing a write: %d %s; Deny: %d %s"
                 % (len(stmts), len(wr), wr, len(dn), dn))
    principals = []
    for page in iam.get_paginator("list_roles").paginate():
        principals += [("role", r["RoleName"], r["Arn"]) for r in page["Roles"]]
    for page in iam.get_paginator("list_users").paginate():
        principals += [("user", u["UserName"], u["Arn"]) for u in page["Users"]]
    # KNOWN SIMULATOR LIMITS, handled rather than inherited: ONE resource ARN per call (a multi-ARN call
    # poisons the verdicts); the EXACT object ARN (a wrong-grain ARN is a false deny); and a CONDITIONED
    # grant. The simulator lists as "missing" every context key ANY of the principal's statements needs,
    # whether or not that statement could grant this action. A key that cannot occur in an s3:PutObject
    # request (s3:prefix is ListBucket's; ses:, cloudwatch:, dynamodb:, ec2:, iam:, ecs:, kms: and
    # s3express: belong to other requests) cannot satisfy a condition here, so the decision stands. A
    # key that CAN occur (aws:*, s3:* other than the list keys) is re-simulated with the request's TRUE
    # value where one exists (this account, this region, the bucket's own tags); what is still missing
    # after that is UNKNOWN, never a quiet "not a writer".
    import boto3 as _b3
    account = _b3.client("sts").get_caller_identity()["Account"]
    try:
        btags = {t["Key"]: t["Value"] for t in s3.get_bucket_tagging(Bucket=bucket).get("TagSet", [])}
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
        """ONE simulation, retried at most twice on a transient error (throttling measured 2026-09-18:
        one principal of 262 raised ClientError on one run and simulated cleanly on the next). A third
        failure is recorded with its error code, never read as a verdict."""
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
        try:
            ev = simulate(PolicySourceArn=parn, ActionNames=[ACTION], ResourceArns=[arn], ResourcePolicy=bp)
            miss = [k for k in (ev.get("MissingContextValues") or []) if relevant(k)]
            if ev["EvalDecision"] != "allowed" and ev.get("MissingContextValues") and not miss:
                irrelevant_only += 1
            if ev["EvalDecision"] != "allowed" and miss:
                entries = [{"ContextKeyName": k, "ContextKeyValues": [true_value(k)], "ContextKeyType": "string"}
                           for k in miss if true_value(k) is not None]
                if entries:
                    resimulated += 1
                    ev = simulate(PolicySourceArn=parn, ActionNames=[ACTION], ResourceArns=[arn],
                                  ResourcePolicy=bp, ContextEntries=entries)
                    miss = [k for k in (ev.get("MissingContextValues") or []) if relevant(k)]
        except Exception as exc:                       # noqa: BLE001
            errors.append((kind, name, str(exc) or type(exc).__name__))
            continue
        if ev["EvalDecision"] == "allowed":
            writers.append((kind, name, parn))
        elif miss:
            unknown.append((kind, name, miss))
    # A SECOND INSTRUMENT for what the simulator left UNKNOWN: read the principal's own documents (inline,
    # attached, and its groups' for a user) and count the Allow statements whose Action AND Resource can
    # match this action on this key, conditions ignored. Zero such statements means no condition value
    # could make it a writer; one or more stays UNKNOWN and is printed.
    settled = []
    for kind, name, miss in list(unknown):
        if not _matching_allow_statements(iam, kind, name, arn):
            settled.append((kind, name))
            unknown.remove((kind, name, miss))
    lines.append("IDENTITY plane: %d principal(s) simulated (%d roles, %d users); %d could not be "
                 "simulated %s" % (len(principals), sum(1 for p in principals if p[0] == "role"),
                                   sum(1 for p in principals if p[0] == "user"), len(errors), errors[:5]))
    lines.append("  conditioned: %d with only keys that cannot occur in a PutObject request (decision "
                 "stands); %d re-simulated with the request's true context; %d settled by statement "
                 "reading (0 Allow statements match the action and key) %s; %d UNKNOWN %s"
                 % (irrelevant_only, resimulated, len(settled), settled, len(unknown),
                    [(k, n, m) for k, n, m in unknown]))
    lines.append("WRITERS: %d of %d principals may %s the 49 Financial directory prefix:"
                 % (len(writers), len(principals), ACTION))
    lines += ["  %-4s %s" % (k, n) for k, n, _ in writers]
    new_verdict = None
    if planned_policy:
        # IDENTITY plane only: SimulateCustomPolicy accepts a resource policy only with an IAM-USER
        # CallerArn, and this principal does not exist yet. Not a gap here: the RESOURCE plane above is
        # read on the same run, and a verdict it could move needs a write Allow or a Deny in it.
        doc = pathlib.Path(planned_policy).read_text(encoding="utf-8")
        r = iam.simulate_custom_policy(PolicyInputList=[doc], ActionNames=[ACTION], ResourceArns=[arn])
        new_verdict = r["EvaluationResults"][0]["EvalDecision"]
        lines.append("the NEW principal's PLANNED policy on the same key (identity plane; the bucket "
                     "policy carries %d write Allow and %d Deny): %s (a writer only if 'allowed')"
                     % (len(wr), len(dn), new_verdict))
    return {"verdict": "EVALUATED", "lines": lines, "bucket": bucket, "arn": arn,
            "principals": len(principals), "unsimulated": len(errors), "unknown": len(unknown),
            "writers": [{"kind": k, "name": n, "arn": a} for k, n, a in writers],
            "new_principal": new_verdict}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--planned-policy", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out = census(a.planned_policy)
    print("\n".join(out["lines"]))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if out["verdict"] == "EVALUATED" else 2)
