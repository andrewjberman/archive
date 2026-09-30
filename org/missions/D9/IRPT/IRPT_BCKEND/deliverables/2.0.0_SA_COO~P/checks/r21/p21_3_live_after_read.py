"""Round 21 AC1 (IB-pr-213, row S132) -- the Lambda@Edge role reads ONLY the public verification keys.

Usage: python p21_3_ac1_edge_secret_narrowed.py
Read-only: iam.get_role_policy(lambda-edge-execution-role, lambda-edge-secrets-logs). Pass: every
secretsmanager:GetSecretValue Resource names a secret under opal/auth/ whose name ends in 'public-key' (optionally
followed by the '-??????' version suffix wildcard), none is a bare wildcard, and none names a private key.
"""
import json
import re
import sys
import urllib.parse

import boto3

doc = boto3.client("iam").get_role_policy(RoleName="lambda-edge-execution-role", PolicyName="lambda-edge-secrets-logs")["PolicyDocument"]
if isinstance(doc, str):
    doc = json.loads(urllib.parse.unquote(doc))
res = []
for s in doc["Statement"]:
    acts = s["Action"] if isinstance(s["Action"], list) else [s["Action"]]
    if any(a.lower() == "secretsmanager:getsecretvalue" for a in acts):
        res += s["Resource"] if isinstance(s["Resource"], list) else [s["Resource"]]
pat = re.compile(r":secret:opal/auth/[A-Za-z0-9_-]*public-key(-\?{6}|-\*)?$")
bad = [r for r in res if not pat.search(r) or "private" in r]
print("GetSecretValue resources %d: %s | not public-key only: %s" % (len(res), res, bad))
ok = bool(res) and not bad
print("P21-3-AC1 PASS" if ok else "P21-3-AC1 FAIL")
sys.exit(0 if ok else 1)
