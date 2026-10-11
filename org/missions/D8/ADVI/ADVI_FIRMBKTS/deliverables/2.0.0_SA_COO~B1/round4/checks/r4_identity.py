"""ADVI_FIRMBKTS round 4: the readers' IDENTITY side of act 3b (the CTO's round-3 ADDENDUM 8, N principals x 2 rules),
issuer 2.0.0_SA_COO~B1. READ-ONLY: list-role-policies, get-role-policy, list-attached-role-policies, get-policy,
get-policy-version, get-bucket-policy. Nothing is written.

For each reader role it prints (identity Allow?, fence admits?) for ONE canonical object that role will read after the flip:
  - the ownership key for the validator's role and the eight IRPT consumers' roles;
  - a served platinum object for the two partner Lambdas' roles (acts 4b, 4c).
"Identity Allow" is a LOCAL glob evaluation of the role's inline and attached policy documents against the action and the
object ARN (an Allow statement whose Action and Resource match, no matching Deny, and a condition on an Allow is printed as
CONDITIONED, never counted as an unconditional Allow). "Fence admits" reads the live bucket policy's
DenyForeignFirmPrincipals ArnNotLike list the same way. It is not iam:SimulatePrincipalPolicy (denied to this identity for
roles); a role the evaluation cannot read prints UNREADABLE.

  python r4_identity.py [--bucket B] [--ownership KEY] [--served KEY]
Exit 0 always (it prints; the pair reads it). Plain ASCII.
"""
import argparse
import fnmatch
import json
import subprocess
import sys

ACCOUNT = "313476888478"


def aws(*a):
    r = subprocess.run(["aws"] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else "aws failed")
    return json.loads(r.stdout or "{}")


def docs_of(role):
    out = []
    for n in aws("iam", "list-role-policies", "--role-name", role).get("PolicyNames", []):
        out.append((n, aws("iam", "get-role-policy", "--role-name", role, "--policy-name", n)["PolicyDocument"]))
    for p in aws("iam", "list-attached-role-policies", "--role-name", role).get("AttachedPolicies", []):
        arn = p["PolicyArn"]
        ver = aws("iam", "get-policy", "--policy-arn", arn)["Policy"]["DefaultVersionId"]
        out.append((p["PolicyName"], aws("iam", "get-policy-version", "--policy-arn", arn, "--version-id", ver)
                    ["PolicyVersion"]["Document"]))
    return out


def _as_list(x):
    return x if isinstance(x, list) else [x]


def match(patterns, value):
    return any(fnmatch.fnmatchcase(value, p) or p == "*" for p in _as_list(patterns or []))


def identity_allow(docs, action, arn):
    allow, conditioned, deny = [], [], []
    for name, d in docs:
        for s in _as_list(d.get("Statement", [])):
            acts = s.get("Action") or []
            res = s.get("Resource") or []
            hit = match(acts, action) and match(res, arn)
            if s.get("NotAction") or s.get("NotResource"):
                continue
            if not hit:
                continue
            if s.get("Effect") == "Deny":
                deny.append(name)
            elif s.get("Condition"):
                conditioned.append(name)
            else:
                allow.append(name)
    if deny:
        return "DENIED-by:" + ",".join(sorted(set(deny)))
    if allow:
        return "ALLOW:" + ",".join(sorted(set(allow)))
    if conditioned:
        return "CONDITIONED:" + ",".join(sorted(set(conditioned)))
    return "NO-ALLOW"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", default="opal-data-49financial")
    ap.add_argument("--ownership", default="advi/49financial/platinum/49financial/ownership_map.json")
    ap.add_argument("--served", default="advi/49financial/platinum/advisors/summary/summary.json")
    a = ap.parse_args()
    pol = json.loads(aws("s3api", "get-bucket-policy", "--bucket", a.bucket)["Policy"])
    deny = [s for s in pol["Statement"] if s.get("Sid") == "DenyForeignFirmPrincipals"][0]
    patterns = deny["Condition"]["ArnNotLike"]["aws:PrincipalArn"]
    allows = [s.get("Sid") for s in pol["Statement"] if s.get("Effect") == "Allow"]
    print("bucket policy: %d statements, Allow statements=%s, fence exemption patterns=%d"
          % (len(pol["Statement"]), allows or "none", len(patterns)))
    roster = [
        ("lambda-edge-execution-role", "ownership", "validator (router and guard share it)"),
        ("irpt-49f-reporting-read-role", "ownership", "irpt-49f-reporting-read-lambda"),
        ("irpt-directory-role", "ownership", "irpt-directory-search"),
        ("irpt-export-render-role", "ownership", "irpt-export-render"),
        ("irpt-holdings-role", "ownership", "irpt-holdings"),
        ("irpt-narrative-role", "ownership", "irpt-narrative"),
        ("irpt-performance-adapter-role", "ownership", "irpt-performance-adapter"),
        ("irpt-status-role", "ownership", "irpt-status"),
        ("irpt-ycharts-generate-role", "ownership", "irpt-ycharts-generate"),
        ("exec-summary-generator-role", "served", "exec-summary-generator (act 4b)"),
        ("partners-lambda-role", "served", "opal-partners-data (act 4c)"),
    ]
    print("%-32s %-10s %-34s %-12s %s" % ("role", "object", "consumer", "fence", "identity (s3:GetObject)"))
    n_ok = 0
    for role, kind, who in roster:
        key = a.ownership if kind == "ownership" else a.served
        arn = "arn:aws:s3:::%s/%s" % (a.bucket, key)
        prin = "arn:aws:iam::%s:role/%s" % (ACCOUNT, role)
        fence = "ADMITTED" if any(fnmatch.fnmatchcase(prin, p) for p in patterns) else "NOT-ADMITTED"
        try:
            ident = identity_allow(docs_of(role), "s3:GetObject", arn)
        except Exception as e:  # noqa: BLE001
            ident = "UNREADABLE(%s)" % str(e)[:60]
        if fence == "ADMITTED" and ident.startswith("ALLOW"):
            n_ok += 1
        print("%-32s %-10s %-34s %-12s %s" % (role, kind, who, fence, ident))
    print("principals readable after the flip today (fence admits AND identity allows): %d of %d" % (n_ok, len(roster)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
