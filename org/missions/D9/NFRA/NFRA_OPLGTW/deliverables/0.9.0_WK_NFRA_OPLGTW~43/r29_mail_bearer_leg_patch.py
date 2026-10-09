"""OG-rl-15 A1, Phase A DESIGN ARTEFACT (nothing is applied to the release tree): builds the proposed deploy-to-ec2.sh change for the MAIL_BEARER leg on a SCRATCH copy
and prints it as a unified diff. usage: python r29_mail_bearer_leg_patch.py <deploy-to-ec2.sh of the candidate> <scratch out file>"""
import sys

src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8", newline="").read()
BS = chr(92)          # a backslash: the script is a heredoc body, so its shell variables are written \$X
D = BS + "$"
a = "MAIL_BEARER=" + D + "(aws secretsmanager get-secret-value --secret-id gateway/mail/bearer --region ${REGION} --query SecretString --output text)" + chr(10)
assert t.count(a) == 1, "anchor"
add = a + chr(10).join([
    "# OG-rl-15 A1 (the MAIL_BEARER leg): the laptop Teams agent's OWN mail bearer, a second labelled value. Read host-side like TEAMS_BEARER above: a failed read, an",
    "# empty value or the CLI's text rendering of a null secret REFUSES (non-zero) before the code is extracted, any .env is written or the service restarts; the value",
    "# is never printed (length only). The two values are joined with a comma, positionally aligned with MAIL_BEARER_LABELS (msgpull,commassist).",
    "MAIL_BEARER_COMMASSIST=" + D + "(aws secretsmanager get-secret-value --secret-id gateway/mail/commassist-bearer --region ${REGION} --query SecretString --output text) || { echo \"ERROR: REFUSED: the commassist mail bearer could not be read; no code extracted, no .env written, no restart.\" >&2; exit 3; }",
    "if [ -z \"" + D + "MAIL_BEARER_COMMASSIST\" ] || [ \"" + D + "MAIL_BEARER_COMMASSIST\" = \"None\" ]; then",
    "    echo \"ERROR: REFUSED: the commassist mail bearer is empty; no code extracted, no .env written, no restart.\" >&2",
    "    exit 3",
    "fi",
    "echo \"OK: commassist mail bearer read host-side (non-empty, " + D + "{#MAIL_BEARER_COMMASSIST} characters)\"",
    "MAIL_BEARER=\"" + D + "MAIL_BEARER," + D + "MAIL_BEARER_COMMASSIST\"",
    ""])
t = t.replace(a, add)
old = "MAIL_BEARER_LABELS=msgpull" + BS + "n"
assert t.count(old) == 1, "labels"
t = t.replace(old, "MAIL_BEARER_LABELS=msgpull,commassist" + BS + "n")
open(out, "w", encoding="utf-8", newline="").write(t)
print("scratch copy written:", out)
