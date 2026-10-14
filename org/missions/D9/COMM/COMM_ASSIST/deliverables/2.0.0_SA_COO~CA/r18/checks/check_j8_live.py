"""CA-j-8 AC1: the resource policy that narrows the ingress-mark key is LIVE, read from AWS, never from a report.

PASS needs all of:
  1. the secret's resource policy (get-resource-policy) has exactly ONE statement: Effect Deny, Principal *, the one action secretsmanager:GetSecretValue, a StringNotEquals on
     aws:PrincipalArn naming the assistant's execution role (the Role both functions carry), and it covers the secret;
  2. simulated against that LIVE policy (simulate-principal-policy with the policy supplied): the execution role's GetSecretValue is allowed, and cloudops-dell1-agent-user's and
     cloudops-dell2-agent-user's are explicitDeny;
  3. management stays open: simulated against the same policy, PutSecretValue, DescribeSecret and PutResourcePolicy on the secret are NOT explicitDeny for the Dell users;
  4. the code did not move: both functions still carry PRE_CODE, INGRESS_MARK_MODE is record in both, and the secret still has a current version (its value is never read).
Prints one line per check and RESULT: PASS|FAIL. Read-only: get, describe and simulate calls.
"""
import json
import os
import subprocess
import sys
import tempfile

PRE_CODE = "nX67q2k05fh77lG2gBLsNlp6HLAZeELPq85CJpWCVhA="
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
SECRET = "teams/global/ingress-mark"
DELLS = ["cloudops-dell1-agent-user", "cloudops-dell2-agent-user"]


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return json.loads(r.stdout), None


def simulate(principal, action, resource, policy_path):
    doc, err = aws("iam", "simulate-principal-policy", "--policy-source-arn", principal, "--action-names", action, "--resource-arns", resource,
                   "--resource-policy", "file://" + policy_path)
    rows = (doc or {}).get("EvaluationResults") or []
    return (rows[0].get("EvalDecision") if rows else None), err


def main():
    ok = True
    cfgs = [aws("lambda", "get-function-configuration", "--function-name", fn)[0] or {} for fn in FUNCS]
    role = cfgs[1].get("Role")
    sec, err = aws("secretsmanager", "describe-secret", "--secret-id", SECRET)
    arn = (sec or {}).get("ARN")
    print("CHECK secret %s %s role=%s %s" % (SECRET, arn, role, err or ""))

    pol, err = aws("secretsmanager", "get-resource-policy", "--secret-id", SECRET)
    raw = (pol or {}).get("ResourcePolicy")
    doc = json.loads(raw) if raw else {}
    st = doc.get("Statement") or []
    cond = (st[0].get("Condition") or {}) if len(st) == 1 else {}
    pa = (cond.get("StringNotEquals") or {}).get("aws:PrincipalArn")
    c1 = (len(st) == 1 and st[0].get("Effect") == "Deny" and st[0].get("Principal") in ("*", {"AWS": "*"}) and st[0].get("Action") == "secretsmanager:GetSecretValue"
          and pa == role and bool(role) and st[0].get("Resource") in (arn, "*"))
    print("CHECK one Deny statement, the one action, an exception for the execution role only: %s %s" % (c1, err or ""))
    ok &= c1

    c2 = c3 = False
    if raw and arn and role:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "policy.json")
            with open(path, "w", encoding="ascii") as fh:
                fh.write(raw)
            path = path.replace("\\", "/")
            users = ["arn:aws:iam::%s:user/%s" % (arn.split(":")[4], d) for d in DELLS]
            role_read, _ = simulate(role, "secretsmanager:GetSecretValue", arn, path)
            dell_read = [simulate(u, "secretsmanager:GetSecretValue", arn, path)[0] for u in users]
            c2 = role_read == "allowed" and all(d == "explicitDeny" for d in dell_read)
            print("CHECK simulated against the live policy: execution role GetSecretValue=%s, Dell users=%s: %s" % (role_read, dell_read, c2))
            mgmt = {a: [simulate(u, a, arn, path)[0] for u in users] for a in ("secretsmanager:PutSecretValue", "secretsmanager:DescribeSecret", "secretsmanager:PutResourcePolicy")}
            c3 = all(d is not None and d != "explicitDeny" for v in mgmt.values() for d in v)
            print("CHECK management acts stay open to the Dell users (not explicitDeny): %s %s" % (c3, mgmt))
    else:
        print("CHECK simulated reads skipped: no live policy, secret or role")
    ok &= c2 and c3

    shas = [c.get("CodeSha256") for c in cfgs]
    envs = [((c.get("Environment") or {}).get("Variables") or {}) for c in cfgs]
    stages = [s for v in ((sec or {}).get("VersionIdsToStages") or {}).values() for s in v]
    c4 = all(s == PRE_CODE for s in shas) and all(e.get("INGRESS_MARK_MODE") == "record" for e in envs) and "AWSCURRENT" in stages
    print("CHECK code unchanged (%s), mode record in both, secret has a current version (value not read): %s" % (shas, c4))
    ok &= c4

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
