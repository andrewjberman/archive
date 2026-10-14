"""CA-i-9: infra/aws/terraform/transcripts/chat_assist.tf pins muse's public key into the assistant's environment, and nothing else moves.

Prints:  I4A-TF ok=<True|False> fp=<SHA256:...|none> env=<bool> fmt=<bool> mail=<bool> reason=<text>
Reads the file only. The pinned key must be the one MUSE_KEY_RECORD.md names (compared by `ssh-keygen -lf` fingerprint), the variable must carry it as
its default, the environment must join it as MUSE_ANSWER_PUBKEY, the existing mail-bearer join must be unchanged, and `terraform fmt -check` must pass.
No AWS, no init, no plan.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
TF = ROOT / "infra" / "aws" / "terraform" / "transcripts" / "chat_assist.tf"
RECORD = ROOT / "org" / "missions" / "D9" / "COMM" / "COMM_ASSIST" / "deliverables" / "2.0.0_SA_COO~CA" / "r17" / "MUSE_KEY_RECORD.md"
VAR = "chat_assist_muse_answer_pubkey"


def main():
    fp, env, fmt, mail, why = "none", False, False, False, ""
    try:
        text = TF.read_text(encoding="utf-8")
        want = re.search(r"`(SHA256:[A-Za-z0-9+/]{43})`", RECORD.read_text(encoding="utf-8")).group(1)
        m = re.search(r'variable\s+"%s"\s*\{(.*?)\n\}' % VAR, text, re.S)
        if not m:
            why = "variable %s is not declared" % VAR
        else:
            d = re.search(r'default\s*=\s*"(ssh-ed25519 [A-Za-z0-9+/=]+(?: [^"]*)?)"', m.group(1))
            if not d:
                why = "the variable has no ssh-ed25519 default"
            else:
                with tempfile.TemporaryDirectory() as tmp:
                    p = Path(tmp) / "k.pub"
                    p.write_text(d.group(1) + "\n", encoding="ascii")
                    out = subprocess.run(["ssh-keygen", "-lf", str(p)], capture_output=True, text=True, timeout=60).stdout
                got = re.search(r"(SHA256:\S+)", out)
                fp = got.group(1) if got else "none"
                if fp != want:
                    why = "the pinned key's fingerprint %s is not the record's %s" % (fp, want)
        env = bool(re.search(r"MUSE_ANSWER_PUBKEY\s*=\s*var\.%s" % VAR, text))
        mail = 'var.chat_assist_mail_bearer_secret_arn == "" ? {} : { MAIL_BEARER_SECRET = var.chat_assist_mail_bearer_secret_arn }' in text
        r = subprocess.run(["terraform", "fmt", "-check", "-diff", str(TF)], capture_output=True, text=True, timeout=90)
        fmt = r.returncode == 0
        if not why and not env:
            why = "the environment does not join MUSE_ANSWER_PUBKEY = var.%s" % VAR
        if not why and not mail:
            why = "the existing MAIL_BEARER_SECRET join was changed or removed"
        if not why and not fmt:
            why = "terraform fmt -check failed"
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I4A-TF ok=%s fp=%s env=%s fmt=%s mail=%s reason=%s" % (not why, fp, env, fmt, mail, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
