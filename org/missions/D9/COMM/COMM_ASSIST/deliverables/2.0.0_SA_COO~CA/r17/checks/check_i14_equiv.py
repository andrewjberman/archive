"""CA-i-14 AC1: the package built at the pin is the assistant that ships -- and it forms the SAME S3 addresses, and considers the SAME mail parties, as the package now live.

The packaged-path diff from the live build (2fd32e12c2) to the pin carries other projects' changes (lib/opal_naming.py, infra/logic/registry/*.json). A plan cannot see
them, because source_code_hash moves identically either way (row COMM_ASSIST-Z-S3). This check reads them where they act: it imports the assistant from the BUILT
package and from the zip the live function serves, and compares every key it forms for a fixed battery of chats and the mail parties (firm -> email domains) each package reads from its own registry.

Prints:  I14-EQUIV ok=<True|False> files=<n> probes=<n> same=<n> reason=<text>
Needs: a detached worktree at PIN with `bash infra/aws/lambda/teams-chat-assist/build.sh` run in it (dist/pkg), and read access to the live function. Read-only.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PIN = "abc5ad424a"
DEPLOYED = "8a480805e5"
FUNC = "teams-global-chat-assist-ingress-lambda"
ROUND17_FILES = ["data/transcripts/scripts/teams_chat/tenant.py"]
PACKAGED = ["infra/aws/lambda/teams-chat-assist/handlers.py", "infra/aws/terraform/modules/ldo/runtime/ldo.py", "data/transcripts/scripts/teams_chat",
            "daily_reports/eod", "lib/opal_naming.py", "org/standards/NAMING_SCHEMA.json", "infra/logic/registry",
            "infra/aws/terraform/transcripts", "infra/aws/terraform/modules/ldo"]

PROBE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, mail_requests as mr
out = {"BUCKET": a.BUCKET}
try:
    out["firms"] = json.dumps({k: sorted(v) if isinstance(v, (list, set, tuple)) else v for k, v in mr.firm_domains().items()}, sort_keys=True, default=str)
except Exception as exc:
    out["firms"] = "ERR %s" % type(exc).__name__
for i, cid in enumerate(["19:abc@unq.gbl.spaces", "19:meeting_XYZ@thread.v2", "eod:2026-10-13", "job:J290", "mail:owner"]):
    out["state_%d" % i] = a.state_key("x_%d.json" % i)
    out["silver_%d" % i] = a.silver_key(cid, "context.md")
    out["bronze_%d" % i] = a.bronze_key(cid, {"created": "2026-10-13T20:13:51Z", "id": "m%d" % i})
print(json.dumps(out, sort_keys=True))
'''


def git(*args, cwd=None):
    return subprocess.run(["git", *args], capture_output=True, cwd=cwd).stdout


def pinned_worktree():
    """The DETACHED worktree whose HEAD is the pin (the seat's scratch checkout), never a branch checkout that happens to sit there."""
    block = []
    for line in git("worktree", "list", "--porcelain").decode("utf-8", "replace").splitlines() + [""]:
        if line:
            block.append(line)
            continue
        head = next((b[5:] for b in block if b.startswith("HEAD ")), "")
        if "detached" in block and head.startswith(PIN):
            return next(b[9:] for b in block if b.startswith("worktree "))
        block = []
    return None


def probe(root):
    r = subprocess.run([sys.executable, "-c", PROBE, root], capture_output=True, text=True, cwd=root, timeout=100)
    return json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {"ERROR": (r.stderr or "")[-200:]}


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    return json.loads(r.stdout) if r.returncode == 0 else None


def main():
    files = probes = same = 0
    why = ""
    try:
        changed = [x for x in git("diff", "--name-only", DEPLOYED, PIN, "--", *PACKAGED).decode("utf-8", "replace").split() if x]
        if changed != ROUND17_FILES:
            raise RuntimeError("the packaged-path diff %s..%s is not exactly the one file: %s" % (DEPLOYED, PIN, changed[:6]))
        wt = pinned_worktree()
        if not wt:
            raise RuntimeError("no detached worktree at the pin %s (or the pin is unset)" % PIN)
        pkg = Path(wt) / "infra" / "aws" / "lambda" / "teams-chat-assist" / "dist" / "pkg"
        if not pkg.is_dir():
            raise RuntimeError("no built package at %s" % pkg)
        for rel in ROUND17_FILES:
            built = (pkg / rel).read_bytes() if (pkg / rel).is_file() else b""
            pin_bytes = git("show", "%s:%s" % (PIN, rel)).replace(b"\r\n", b"\n")
            files += 1
            if not built or built != pin_bytes:
                raise RuntimeError("built %s is not the pin's bytes" % rel)
        doc = aws("lambda", "get-function", "--function-name", FUNC)
        url = ((doc or {}).get("Code") or {}).get("Location")
        if not url:
            raise RuntimeError("could not read the live function's code location")
        data = urllib.request.urlopen(url, timeout=60).read()
        with tempfile.TemporaryDirectory() as tmp:
            zipfile.ZipFile(io.BytesIO(data)).extractall(tmp)
            live, built = probe(tmp), probe(str(pkg))
        if "ERROR" in live or "ERROR" in built:
            raise RuntimeError("probe failed: live=%s built=%s" % (str(live)[:120], str(built)[:120]))
        probes = len(built)
        same = sum(1 for k in built if built[k] == live.get(k))
        if same != probes:
            why = "keys differ: %s" % [k for k in built if built[k] != live.get(k)][:4]
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I14-EQUIV ok=%s files=%d probes=%d same=%d reason=%s" % (not why, files, probes, same, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
