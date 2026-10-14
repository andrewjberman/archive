"""CA-j-5 AC1: the flip to enforce is ENVIRONMENT-ONLY. The package built at the pin is byte-for-byte the package now live, and the pin differs from the live pin by exactly the one Terraform line.

Prints:  J5-EQUIV ok=<True|False> built=<base64 sha256|none> live=<CodeSha256 of both functions|none> files=<paths in the diff> tf=<bool> reason=<text>
Needs: env J5_PIN (the commit the deploy is built from), a DETACHED worktree at J5_PIN with `bash infra/aws/lambda/teams-chat-assist/build.sh` run in it (dist/teams-chat-assist.zip), and read access to the
live functions. The build is reproducible (fixed timestamps, LF endings), so equal inputs give an equal hash: a built hash equal to the live CodeSha256 PROVES the code does not move, and the plan
can show only an environment change. The packaged-path diff from the live pin (DEPLOYED) to J5_PIN must be exactly chat_assist.tf, and `check_j5_tf.py` run against that worktree must read ok=True.
Read-only.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

PIN = os.environ.get("J5_PIN", "")
DEPLOYED = "afa8752f44"
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
PACKAGED = ["infra/aws/lambda/teams-chat-assist", "infra/aws/terraform/modules/ldo", "data/transcripts/scripts/teams_chat", "daily_reports/eod", "lib/opal_naming.py",
            "org/standards/NAMING_SCHEMA.json", "infra/logic/registry", "infra/aws/terraform/transcripts"]
TF = "infra/aws/terraform/transcripts/chat_assist.tf"
J5TF = Path(__file__).with_name("check_j5_tf.py")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True).stdout


def pinned_worktree():
    block = []
    for line in git("worktree", "list", "--porcelain").decode("utf-8", "replace").splitlines() + [""]:
        if line:
            block.append(line)
            continue
        head = next((b[5:] for b in block if b.startswith("HEAD ")), "")
        if "detached" in block and PIN and head.startswith(PIN):
            return next(b[9:] for b in block if b.startswith("worktree "))
        block = []
    return None


def live_hash(fn):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, "lambda", "get-function-configuration", "--function-name", fn, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    return json.loads(r.stdout).get("CodeSha256") if r.returncode == 0 else None


def main():
    built, live, files, tf, why = "none", "none", [], False, ""
    try:
        if not PIN:
            raise RuntimeError("J5_PIN is not set")
        wt = pinned_worktree()
        if not wt:
            raise RuntimeError("no detached worktree at the pin %s" % PIN)
        zp = Path(wt) / "infra" / "aws" / "lambda" / "teams-chat-assist" / "dist" / "teams-chat-assist.zip"
        if not zp.is_file():
            raise RuntimeError("no built package at %s" % zp)
        built = base64.b64encode(hashlib.sha256(zp.read_bytes()).digest()).decode()
        hashes = [live_hash(f) for f in FUNCS]
        live = hashes[0] if len(set(hashes)) == 1 and hashes[0] else "none:%s" % hashes
        files = [x for x in git("diff", "--name-only", DEPLOYED, PIN, "--", *PACKAGED).decode("utf-8", "replace").split() if x]
        out = subprocess.run([sys.executable, str(J5TF), wt], capture_output=True, text=True, timeout=120).stdout
        tf = "J5-TF ok=True arms=2 of 2" in out
        if built != live:
            why = "the built package %s is not the live package %s: the plan would carry a code change" % (built, live)
        elif files != [TF]:
            why = "the packaged-path diff %s..%s is %s, not exactly %s" % (DEPLOYED, PIN, files[:6], TF)
        elif not tf:
            why = "check_j5_tf does not read ok=True against the pinned worktree"
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("J5-EQUIV ok=%s built=%s live=%s files=%s tf=%s reason=%s" % (not why, built, live, files, tf, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
