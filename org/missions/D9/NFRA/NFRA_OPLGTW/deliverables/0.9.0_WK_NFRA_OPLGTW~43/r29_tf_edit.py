"""OG-rl-15 A7 D4 option A: the one policy line (a fifth secret ARN) in infra/aws/terraform/opal-gateway/gateway-read-secrets.tf, so the gateway host role may read
gateway/mail/commassist-bearer at deploy. Built from the BLOB at the given rev (re-runnable) and written into the given tree. Nothing is applied: the applier plans and applies it
under the ledger, after it has created the secret out-of-band.
usage: python r29_tf_edit.py <tree root> <repo for git show> <rev>"""
import subprocess
import sys

TF = "infra/aws/terraform/opal-gateway/gateway-read-secrets.tf"
root, repo, rev = sys.argv[1], sys.argv[2], sys.argv[3]
t = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, TF)], capture_output=True, check=True).stdout.decode("utf-8")
NL = chr(10)


def sub(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


t = sub(t, "# host at deploy time exactly like the mail bearer (Andrew's Teams assistant, /hx/teams)." + NL,
        "# host at deploy time exactly like the mail bearer (Andrew's Teams assistant, /hx/teams)." + NL
        + "# A FIFTH (NFRA_OPLGTW OG-rl-15 A1/A7 D4, option A): the laptop Teams agent's OWN mail bearer, gateway/mail/commassist-bearer (label commassist), read by the" + NL
        + "# host at deploy time like the others. The secret is created out-of-band by the applier before this line is applied; the existing mail bearer is never written." + NL)
t = sub(t, "on EXACTLY four secret ARNs", "on EXACTLY five secret ARNs")
t = sub(t, "gateway/principals/rosters, gateway/teams/bearer. No", "gateway/principals/rosters, gateway/teams/bearer, gateway/mail/commassist-bearer. No")
t = sub(t, "EXACTLY the four ARNs above", "EXACTLY the five ARNs above")
t = sub(t, "read allowed on the four and implicitDeny", "read allowed on the five and implicitDeny")
t = sub(t, 'data "aws_secretsmanager_secret" "gateway_teams_bearer" {' + NL + '  name = "gateway/teams/bearer"' + NL + "}" + NL,
        'data "aws_secretsmanager_secret" "gateway_teams_bearer" {' + NL + '  name = "gateway/teams/bearer"' + NL + "}" + NL + NL
        + 'data "aws_secretsmanager_secret" "gateway_mail_commassist_bearer" {' + NL + '  name = "gateway/mail/commassist-bearer"' + NL + "}" + NL)
t = sub(t, "          data.aws_secretsmanager_secret.gateway_teams_bearer.arn," + NL,
        "          data.aws_secretsmanager_secret.gateway_teams_bearer.arn," + NL + "          data.aws_secretsmanager_secret.gateway_mail_commassist_bearer.arn," + NL)
with open(root + "/" + TF, "w", encoding="utf-8", newline="") as fh:
    fh.write(t)
print("wrote", root + "/" + TF)
