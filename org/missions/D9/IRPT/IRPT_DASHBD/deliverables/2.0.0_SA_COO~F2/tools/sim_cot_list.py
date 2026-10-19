"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY what-if of the Cottonwood pair's Addendum 1 statement (ListTheAccountTransactionGoldPrefixOnly), with the live bucket policy as the resource policy.

  python <this file>        run from the repository root; IAM simulate-principal-policy and get-bucket-policy only; decisions and matched ids printed

The role is the landing function's execution role. The planned statement is supplied as an extra policy document; each call is made WITHOUT and WITH the live opal-data-cottonwood bucket policy as the resource policy
(without it a bucket-level fence is invisible). Calls: s3:ListBucket with s3:prefix = the transaction prefix (expected allowed with the planned statement), the same call WITHOUT the planned statement (expected
not allowed: the live gap IB2 hit), the returns prefix (the live statement: allowed, the control), and a broader prefix (the gold root) and a sibling table prefix with the planned statement (expected not allowed:
the statement is one prefix). Decisions only.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
AWS = str(ROOT / ".tools" / "aws.cmd")
ROLE_ARN = "arn:aws:iam::313476888478:role/irpt-cot-account-return-daily-execution-role"
BUCKET = "opal-data-cottonwood"
TX = "irpt/cottonwood/gold/account_transaction/"
RETURNS = "irpt/cottonwood/gold/account_return_daily/"
PLANNED = json.dumps({"Version": "2012-10-17", "Statement": [{
    "Sid": "ListTheAccountTransactionGoldPrefixOnly", "Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": ["arn:aws:s3:::" + BUCKET],
    "Condition": {"StringLike": {"s3:prefix": [TX + "*"]}}}]})


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("aws failed: " + (r.stderr or r.stdout)[-300:])
    return json.loads(r.stdout)


def sim(prefix, planned, resource_policy):
    cmd = ["iam", "simulate-principal-policy", "--policy-source-arn", ROLE_ARN, "--action-names", "s3:ListBucket", "--resource-arns", "arn:aws:s3:::" + BUCKET,
           "--context-entries", "ContextKeyName=s3:prefix,ContextKeyValues=%s,ContextKeyType=string" % prefix]
    if planned:
        cmd += ["--policy-input-list", PLANNED]
    if resource_policy:
        cmd += ["--resource-policy", resource_policy]
    e = aws(*cmd)["EvaluationResults"][0]
    return e["EvalDecision"], [m["SourcePolicyId"] for m in e.get("MatchedStatements", [])][:3]


def main():
    bp = aws("s3api", "get-bucket-policy", "--bucket", BUCKET)["Policy"]
    calls = [("transaction prefix, planned statement ADDED", TX, True, "allowed"), ("transaction prefix, as live (no planned statement)", TX, False, "not allowed"),
             ("returns prefix, as live (control)", RETURNS, False, "allowed"), ("gold root, planned statement added", "irpt/cottonwood/gold/", True, "not allowed"),
             ("a sibling table prefix, planned statement added", "irpt/cottonwood/gold/account_dim/", True, "not allowed")]
    bad = 0
    for label, prefix, planned, want in calls:
        for with_rp in (False, True):
            dec, matched = sim(prefix, planned, bp if with_rp else None)
            ok = (dec == "allowed") == (want == "allowed")
            bad += 0 if ok else 1
            print("%-52s resource policy %-12s -> %-14s %s matched %s" % (label, "INCLUDED" if with_rp else "not included", dec, "OK" if ok else "UNEXPECTED (want %s)" % want, matched))
    print("VERDICT: %s" % ("EXPECTED in all %d calls" % (2 * len(calls)) if not bad else "%d UNEXPECTED reading(s)" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
