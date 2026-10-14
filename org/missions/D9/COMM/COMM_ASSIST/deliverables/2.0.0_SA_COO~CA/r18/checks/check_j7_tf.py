"""CA-j-7: chat_assist.tf declares a resource policy on the ingress-mark secret that DENIES secretsmanager:GetSecretValue to every principal except the assistant's execution role.

Prints:  J7-TF ok=<True|False> arms=<n> of 6 failed=<names|none> reason=<text>
Reads files only (argv[1] = a tree root, default the working directory, so a scratch reference can be graded). No AWS, no init, no plan.
Arms: policy (the resource exists and is attached to the mark secret), deny (one statement, Effect Deny, Principal *, the ONE action GetSecretValue), scope (the exception is
a StringNotEquals on aws:PrincipalArn built from module.ldo_001.execution_role_name and the caller identity, never a typed ARN), narrow (no Allow, no wildcard action, no
second statement), keep (the round-18 CA-j-2 check still reads 7 of 7: the secret shell, its read grant, the mode), plus fmt.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
TF = ROOT / "infra" / "aws" / "terraform" / "transcripts" / "chat_assist.tf"
J2 = Path(__file__).with_name("check_j2_tf.py")
ARMS = ("policy", "deny", "scope", "narrow", "keep", "fmt")


def block(text, header):
    """The body of the first resource block whose header line matches, by brace counting."""
    m = re.search(header, text)
    if not m:
        return None
    i = text.index("{", m.end() - 1)
    depth = 0
    for j in range(i, len(text)):
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        if depth == 0:
            return text[i:j + 1]
    return None


def main():
    got, why = {}, ""
    try:
        text = TF.read_text(encoding="utf-8")
        res = block(text, r'resource\s+"aws_secretsmanager_secret_policy"\s+"ca_ingress_mark"\s*\{')
        got["policy"] = bool(res and re.search(r"secret_arn\s*=\s*aws_secretsmanager_secret\.ca_ingress_mark\.arn\b", res))
        flat = re.sub(r"\s+", " ", res or "")
        got["deny"] = bool(res and len(re.findall(r"Effect\s*=\s*\"", flat)) == 1 and re.search(r'Effect\s*=\s*"Deny"', flat)
                           and re.search(r'Principal\s*=\s*"\*"', flat) and re.search(r'Action\s*=\s*"secretsmanager:GetSecretValue"', flat))
        got["scope"] = bool(res and re.search(r"StringNotEquals\s*=\s*\{\s*\"aws:PrincipalArn\"\s*=", flat)
                            and "module.ldo_001.execution_role_name" in flat and "data.aws_caller_identity.current.account_id" in flat
                            and not re.search(r"arn:aws:iam::\d{12}", flat))
        got["narrow"] = bool(res and not re.search(r'Effect\s*=\s*"Allow"', flat) and not re.search(r'Action\s*=\s*"secretsmanager:\*"', flat)
                             and flat.count("Sid") == 1 and "NotAction" not in flat and "NotPrincipal" not in flat)
        j2 = subprocess.run([sys.executable, str(J2), str(ROOT)], capture_output=True, text=True, timeout=120).stdout
        got["keep"] = "J2-TF ok=True arms=7 of 7" in j2
        r = subprocess.run(["terraform", "fmt", "-check", "-diff", str(TF)], capture_output=True, text=True, timeout=90)
        got["fmt"] = r.returncode == 0
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    failed = [a for a in ARMS if not got.get(a)]
    ok = not why and not failed
    print("J7-TF ok=%s arms=%d of %d failed=%s reason=%s" % (ok, len(ARMS) - len(failed), len(ARMS), ",".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
