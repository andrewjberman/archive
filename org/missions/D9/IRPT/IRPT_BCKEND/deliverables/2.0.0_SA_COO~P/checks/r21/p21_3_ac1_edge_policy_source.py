"""Round 21 AC1 (IB-pr-213, row S132) -- in Terraform, the Lambda@Edge role's GetSecretValue grant names EXACTLY the
secrets the edge validator reads, all public keys (least privilege; PRD item 1).

Usage: python p21_3_ac1_edge_policy_source.py <worktree root>
Reads, in the worktree: (a) the secret ids the edge code reads -- every 'opal/auth/<name>' literal in
infra/aws/lambda-edge/auth-validator-edge/*.mjs and the JWT_PUBLIC_KEY_SECRET_ID the edge imports from
infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs; (b) the Resource strings of the GetSecretValue statement in
aws_iam_role_policy.lambda_edge_secrets_logs (infra/aws/terraform/portal-auth/iam.tf).
Pass: every Resource ends ':secret:opal/auth/<name>-*' (or '-??????') for a <name> in (a), each name in (a) is covered,
none is a bare 'opal/auth/*', and no name contains 'private'. The live grant is read after apply by
p21_3_live_after_read.py (the issuer's served act, never this cell's).
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
reads = set()
for f in (root / "infra/aws/lambda-edge/auth-validator-edge").glob("*.mjs"):
    reads |= set(re.findall(r"opal/auth/([A-Za-z0-9_-]+)", f.read_text(encoding="utf-8")))
lib = (root / "infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs").read_text(encoding="utf-8")
reads |= set(re.findall(r"JWT_PUBLIC_KEY_SECRET_ID\s*=\s*'opal/auth/([A-Za-z0-9_-]+)'", lib))
tf = (root / "infra/aws/terraform/portal-auth/iam.tf").read_text(encoding="utf-8")
start = tf.index('resource "aws_iam_role_policy" "lambda_edge_secrets_logs"')
block = tf[start:tf.index("\n}\n", start)]
stmt = block[block.index("secretsmanager:GetSecretValue"):]
stmt = "\n".join(stmt.splitlines()[:12])
stmt = stmt[:stmt.index("Effect")] if "Effect" in stmt else stmt
res = re.findall(r'"(arn:aws:secretsmanager:[^"]+)"', stmt)
names = []
bad = []
for r in res:
    m = re.search(r":secret:opal/auth/([A-Za-z0-9_-]+?)(-\*|-\?{6})$", r)
    if not m:
        bad.append(r)
    else:
        names.append(m.group(1))
print("edge reads %s | GetSecretValue resources %d %s" % (sorted(reads), len(res), res))
ok = (bool(res) and not bad and set(names) == reads and not any("private" in n for n in names)
      and all(n.endswith("public-key") for n in names))
print("P21-3-AC1 PASS" if ok else "P21-3-AC1 FAIL")
sys.exit(0 if ok else 1)
