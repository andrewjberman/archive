"""CA-l-4 AC1: the package built at the pin is the NARROWER assistant that ships -- the live package minus exactly the five registry files the manifest drops.

The BUILT package (a detached worktree at M4_PIN with `bash infra/aws/lambda/teams-chat-assist/build.sh` run in it: dist/pkg) is compared with the zip the live
function serves NOW (the CA-k-4 package, CodeSha256 nQlJW0j/..., 39 files, built at 93a3f55d25). Arms:
  (a) files only in the live zip == exactly the five registry files the manifest drops (catalog_fork_keys, event_rules, key_rulings, name_rulings, root_map), and files
      only in the built package == none;
  (b) every other file is byte-equal, except the FOREIGN set (the registry files other seats changed between the two pins: legacy_addresses.json, reporting_policies.json),
      which is counted and printed;
  (c) the registry files of the built package == the manifest registry_files.txt as the pin holds it == the twelve names recorded here;
  (d) the same 17-probe battery as check_l4_equiv.py (S3 addresses for five chats and the mail parties) gives identical output from the built package and from the live zip.

Prints:  M4-EQUIV ok=<True|False> dropped=<n> foreign=<n> probes=<n> same=<n> reason=<text>
Needs: env M4_PIN, a detached worktree at M4_PIN with build.sh run in it (dist/pkg), and read access to the live function. Read-only (one get-function, one download).
Finds the repository from the current directory's git toplevel, never from this file's location.
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

PIN = os.environ.get("M4_PIN", "")
FUNC = "teams-global-chat-assist-ingress-lambda"
REG = "infra/logic/registry/"
MANIFEST = "infra/aws/lambda/teams-chat-assist/registry_files.txt"
DROPPED = sorted(REG + n for n in ["catalog_fork_keys.json", "event_rules.json", "key_rulings.json", "name_rulings.json", "root_map.json"])
FOREIGN = sorted(REG + n for n in ["legacy_addresses.json", "reporting_policies.json"])
TWELVE = sorted(["exemptions.json", "feeds.json", "firm_pages.json", "legacy_addresses.json", "mail_parties.json", "platinum_destinations.json",
                 "remediations.json", "reporting_policies.json", "resources.json", "scopes.json", "systems.json", "tiers.json"])

# The probe battery of check_l4_equiv.py, unchanged.
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


def root():
    """The checkout under test: the git toplevel of the current directory, never this file's location."""
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() or os.getcwd()


def git(*args, cwd=None):
    return subprocess.run(["git", *args], capture_output=True, cwd=cwd or ROOT).stdout


def pinned_worktree():
    """The DETACHED worktree whose HEAD is the pin (the seat's scratch checkout), never a branch checkout that happens to sit there."""
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


def probe(path):
    r = subprocess.run([sys.executable, "-c", PROBE, path], capture_output=True, text=True, cwd=path, timeout=100)
    return json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {"ERROR": (r.stderr or "")[-200:]}


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    return json.loads(r.stdout) if r.returncode == 0 else None


def built_files(pkg):
    out = {}
    for base, dirs, names in os.walk(pkg):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            if not n.endswith(".pyc"):
                p = os.path.join(base, n)
                out[os.path.relpath(p, pkg).replace(os.sep, "/")] = Path(p).read_bytes()
    return out


ROOT = root()


def main():
    dropped = probes = same = 0
    foreign = []
    why = ""
    try:
        if not PIN:
            raise RuntimeError("M4_PIN is not set")
        wt = pinned_worktree()
        if not wt:
            raise RuntimeError("no detached worktree at the pin %s" % PIN)
        pkg = Path(wt) / "infra" / "aws" / "lambda" / "teams-chat-assist" / "dist" / "pkg"
        if not pkg.is_dir():
            raise RuntimeError("no built package at %s" % pkg)
        doc = aws("lambda", "get-function", "--function-name", FUNC)
        url = ((doc or {}).get("Code") or {}).get("Location")
        if not url:
            raise RuntimeError("could not read the live function's code location")
        data = urllib.request.urlopen(url, timeout=60).read()
        zf = zipfile.ZipFile(io.BytesIO(data))
        live = {i.filename: zf.read(i.filename) for i in zf.infolist() if not i.is_dir()}
        built = built_files(pkg)
        live_only, built_only = sorted(set(live) - set(built)), sorted(set(built) - set(live))
        dropped = len(live_only)
        problems = []
        if live_only != DROPPED or built_only:
            problems.append("(a) live-only %s built-only %s, want live-only == the five dropped registry files and built-only == none" % (live_only, built_only))
        differ = sorted(n for n in set(live) & set(built) if live[n] != built[n])
        foreign = [n for n in differ if n in FOREIGN]
        other = [n for n in differ if n not in FOREIGN]
        if other:
            problems.append("(b) differ outside the foreign set: %s" % other[:6])
        if foreign:
            print("FOREIGN packaged files that differ (%d): %s" % (len(foreign), foreign))
        reg = sorted(n[len(REG):] for n in built if n.startswith(REG))
        man_text = git("show", "%s:%s" % (PIN, MANIFEST)).decode("utf-8", "replace").replace("\r", "")
        man = sorted(x.strip() for x in man_text.split("\n") if x.strip() and not x.strip().startswith("#"))
        if reg != man or man != TWELVE or len(reg) != 12:
            problems.append("(c) built registry files %s, manifest at the pin %s, want the twelve" % (reg, man))
        with tempfile.TemporaryDirectory() as tmp:
            zf.extractall(tmp)
            live_p, built_p = probe(tmp), probe(str(pkg))
        if "ERROR" in live_p or "ERROR" in built_p:
            problems.append("(d) probe failed: live=%s built=%s" % (str(live_p)[:120], str(built_p)[:120]))
        else:
            probes = len(built_p)
            same = sum(1 for k in built_p if built_p[k] == live_p.get(k))
            if probes != 17 or same != probes or set(built_p) != set(live_p):
                problems.append("(d) probes: %d keys, %d same; differ %s" % (probes, same, [k for k in built_p if built_p[k] != live_p.get(k)][:4]))
        if problems:
            why = "; ".join(problems)
    except Exception as exc:  # noqa: BLE001 -- any failure reads as ok=False with its reason
        why = "%s: %s" % (type(exc).__name__, str(exc)[:240])
    print("M4-EQUIV ok=%s dropped=%d foreign=%d probes=%d same=%d reason=%s" % (not why, dropped, len(foreign), probes, same, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
