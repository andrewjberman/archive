"""COMM_ASSIST CA-d-2 AC1 (round 12): the mail deploy is live, read from AWS, never from a report.

PASS needs all of:
  1. the secret gateway/mail/commassist-bearer exists (describe-secret), giving its ARN;
  2. chat_assist.tf at HEAD sets var.chat_assist_mail_bearer_secret_arn's default to exactly that ARN (committed, so a
     later apply of the root cannot silently unwire it);
  3. both functions (handler, ingress) carry CodeSha256 equal to the built package
     infra/aws/lambda/teams-chat-assist/dist/teams-chat-assist.zip and different from the round-7 package xWURpe...;
  4. both functions' environment carries MAIL_BEARER_SECRET equal to that ARN;
  5. the execution policy's default version grants secretsmanager:GetSecretValue on that ARN.
Prints one line per check and RESULT: PASS|FAIL. Read-only: describe/get calls only.
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys

R7 = "xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q="
SECRET = "gateway/mail/commassist-bearer"
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
POLICY = "arn:aws:iam::313476888478:policy/teams-global-chat-assist-policy"
ZIP = "infra/aws/lambda/teams-chat-assist/dist/teams-chat-assist.zip"
TF = "infra/aws/terraform/transcripts/chat_assist.tf"


def root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
    return out.stdout.strip()


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None, (r.stderr or "").strip().splitlines()[-1:] or ["rc=%d" % r.returncode]
    return json.loads(r.stdout), None


def main():
    os.chdir(root())
    ok = True
    sec, err = aws("secretsmanager", "describe-secret", "--secret-id", SECRET)
    arn = sec.get("ARN") if sec else None
    print("CHECK secret %s exists: %s" % (SECRET, "yes" if arn else "no (%s)" % err))
    ok &= bool(arn)

    head = subprocess.run(["git", "show", "HEAD:" + TF], capture_output=True, text=True, encoding="utf-8").stdout
    m = re.search(r'variable "chat_assist_mail_bearer_secret_arn"\s*\{.*?default\s*=\s*"([^"]*)"', head, re.S)
    committed = m.group(1) if m else None
    print("CHECK chat_assist.tf default at HEAD equals the secret ARN: %s" % (bool(arn) and committed == arn))
    ok &= bool(arn) and committed == arn

    built = None
    if os.path.isfile(ZIP):
        built = base64.b64encode(hashlib.sha256(open(ZIP, "rb").read()).digest()).decode()
    print("CHECK built package present: %s" % (built or "no"))
    ok &= bool(built)

    for fn in FUNCS:
        cfg, err = aws("lambda", "get-function-configuration", "--function-name", fn)
        sha = cfg.get("CodeSha256") if cfg else None
        env = ((cfg or {}).get("Environment") or {}).get("Variables") or {}
        c1 = bool(sha) and sha == built and sha != R7
        c2 = bool(arn) and env.get("MAIL_BEARER_SECRET") == arn
        print("CHECK %s CodeSha256 == built and != r7: %s (live %s)" % (fn, c1, sha))
        print("CHECK %s MAIL_BEARER_SECRET == secret ARN: %s" % (fn, c2))
        ok &= c1 and c2

    pol, err = aws("iam", "get-policy", "--policy-arn", POLICY)
    granted = False
    if pol:
        ver = pol["Policy"]["DefaultVersionId"]
        doc, err = aws("iam", "get-policy-version", "--policy-arn", POLICY, "--version-id", ver)
        stmts = (doc or {}).get("PolicyVersion", {}).get("Document", {}).get("Statement", [])
        for s in stmts if isinstance(stmts, list) else [stmts]:
            acts = s.get("Action", [])
            acts = acts if isinstance(acts, list) else [acts]
            res = s.get("Resource", [])
            res = res if isinstance(res, list) else [res]
            if s.get("Effect") == "Allow" and "secretsmanager:GetSecretValue" in acts and arn in res:
                granted = True
    print("CHECK execution policy grants GetSecretValue on the secret ARN: %s" % granted)
    ok &= granted

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
