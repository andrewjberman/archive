"""CA-j-5 AC1: chat_assist.tf differs from the record-mode file of the pin 3af44d523b (CA-j-7 merged) by EXACTLY ONE line: the default of chat_assist_ingress_mark_mode, record -> enforce.

Prints:  J5-TF ok=<True|False> arms=<n> of 2 failed=<names|none> reason=<text>
Reads the file and `git show 3af44d523b:...` only (argv[1] = a tree root, default the working directory, so a scratch reference can be graded). No AWS, no init, no plan.
Arms: onlydefault (the working file equals the pin's file with that one default changed to "enforce", LF-normalised, nothing else), fmt (`terraform fmt -check` passes).
"""
import re
import subprocess
import sys
from pathlib import Path

PIN = "3af44d523b"
REL = "infra/aws/terraform/transcripts/chat_assist.tf"
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
TF = ROOT / REL
ARMS = ("onlydefault", "fmt")


def main():
    got, why = {}, ""
    try:
        base = subprocess.run(["git", "show", "%s:%s" % (PIN, REL)], capture_output=True, text=True, encoding="utf-8", cwd=str(Path.cwd())).stdout
        cur = TF.read_text(encoding="utf-8").replace("\r\n", "\n")
        base = base.replace("\r\n", "\n")
        m = re.search(r'(variable\s+"chat_assist_ingress_mark_mode"\s*\{.*?default\s*=\s*)"record"', base, re.S)
        want = base[:m.start()] + m.group(1) + '"enforce"' + base[m.end():] if (base and m) else None
        got["onlydefault"] = bool(want) and cur == want
        r = subprocess.run(["terraform", "fmt", "-check", "-diff", str(TF)], capture_output=True, text=True, timeout=90)
        got["fmt"] = r.returncode == 0
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    failed = [a for a in ARMS if not got.get(a)]
    ok = not why and not failed
    print("J5-TF ok=%s arms=%d of %d failed=%s reason=%s" % (ok, len(ARMS) - len(failed), len(ARMS), ",".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
