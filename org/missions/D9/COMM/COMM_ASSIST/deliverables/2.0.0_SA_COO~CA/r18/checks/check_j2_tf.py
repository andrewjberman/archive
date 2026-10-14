"""CA-j-2: chat_assist.tf declares the ingress-mark secret SHELL (no value), lets the two functions read it, and sets INGRESS_MARK_MODE (default record).

Prints:  J2-TF ok=<True|False> arms=<n> of 7 failed=<names|none> reason=<text>
Reads files only (argv[1] = a tree root, default the working directory, so a scratch reference can be graded). No AWS, no init, no plan.
Arms: names (NAMES.json row), shell (the secret resource reads that row), reads (it is in secret_arns), mode (variable default "record" and the
environment key), value (no secret_string and no secret_version anywhere), keep (the existing joins and secrets are untouched), plus fmt.
"""
import re
import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
TF = ROOT / "infra" / "aws" / "terraform" / "transcripts" / "chat_assist.tf"
NAMES = ROOT / "data" / "transcripts" / "scripts" / "teams_chat" / "NAMES.json"
ARMS = ("names", "shell", "reads", "mode", "value", "keep", "fmt")
VAR = "chat_assist_ingress_mark_mode"


def main():
    got, why = {}, ""
    try:
        text = TF.read_text(encoding="utf-8")
        names = json.loads(NAMES.read_text(encoding="utf-8"))
        got["names"] = names.get("secrets", {}).get("ingress_mark") == "teams/global/ingress-mark"
        got["shell"] = bool(re.search(r'resource\s+"aws_secretsmanager_secret"\s+"ca_ingress_mark"\s*\{[^}]*name\s*=\s*local\.ca_names\.secrets\.ingress_mark\b', text, re.S))
        sa = re.search(r"secret_arns\s*=\s*concat\(\[(.*?)\]", text, re.S)
        got["reads"] = bool(sa and "aws_secretsmanager_secret.ca_ingress_mark.arn" in sa.group(1))
        v = re.search(r'variable\s+"%s"\s*\{(.*?)\n\}' % VAR, text, re.S)
        got["mode"] = bool(v and re.search(r'default\s*=\s*"record"', v.group(1)) and re.search(r"INGRESS_MARK_MODE\s*=\s*var\.%s\b" % VAR, text))
        got["value"] = not re.search(r"secret_string|aws_secretsmanager_secret_version|secret_binary", text)
        keep = [
            "MUSE_ANSWER_PUBKEY = var.chat_assist_muse_answer_pubkey",
            'var.chat_assist_mail_bearer_secret_arn == "" ? {} : { MAIL_BEARER_SECRET = var.chat_assist_mail_bearer_secret_arn }',
            "aws_secretsmanager_secret.ca_gateway_bearer.arn",
            "aws_secretsmanager_secret.ca_owner_phone.arn",
            "data.aws_secretsmanager_secret.ca_kimi.arn",
            'var.chat_assist_mail_bearer_secret_arn == "" ? [] : [var.chat_assist_mail_bearer_secret_arn]',
        ]
        got["keep"] = all(k in text for k in keep)
        r = subprocess.run(["terraform", "fmt", "-check", "-diff", str(TF)], capture_output=True, text=True, timeout=90)
        got["fmt"] = r.returncode == 0
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    failed = [a for a in ARMS if not got.get(a)]
    ok = not why and not failed
    print("J2-TF ok=%s arms=%d of %d failed=%s reason=%s" % (ok, len(ARMS) - len(failed), len(ARMS), ",".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
