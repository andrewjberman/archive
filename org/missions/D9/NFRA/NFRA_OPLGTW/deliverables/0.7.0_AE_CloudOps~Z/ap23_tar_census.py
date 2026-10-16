#!/usr/bin/env python
"""OG-ap-23 A5: the tar census. Runs the deploy script's OWN staging block and OWN tar line against a synthetic SRC and a
synthetic workspace (bash, GNU tar), then reads the real member list of the archive it built.

SRC carries DECOY copies of app/refs/partner_roster.json and app/refs/scopes.json (the untracked test copies a release
tree can hold); the synthetic workspace carries trunk_sha's real blobs of the two repo sources. The census is what the
archive holds: each name once, with the md5 of the member's bytes, which must equal the md5 of trunk's blob.
Also reported: the existing excludes (.env, audit.jsonl, *.log, __pycache__) still drop their targets, and a SRC-only file
under app/refs/ is still shipped.

usage: python ap23_tar_census.py <deploy-to-ec2.sh> <trunk_sha> <out.json>   (run from the repository root)
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile

SCRIPT, TRUNK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
REFS = {
    "app/refs/partner_roster.json": "data/mdpf/config/partner_roster.json",
    "app/refs/scopes.json": "infra/logic/registry/scopes.json",
}


def blob(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("cannot read %s:%s" % (ref, path))
    return r.stdout


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def region(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


def posix(path):
    """A path in the form Git Bash's tar accepts (a drive letter reads as a remote host to GNU tar)."""
    path = path.replace("\\", "/")
    if len(path) > 2 and path[1] == ":":
        path = "/" + path[0].lower() + path[2:]
    return path


def md5(data):
    return hashlib.md5(data).hexdigest()


text = open(SCRIPT, encoding="utf-8").read()
stage = region(text, "for _stage_src in", 'cp "$WORKSPACE_ROOT/infra/logic/registry/scopes.json"')
stage += text[text.index('cp "$WORKSPACE_ROOT/infra/logic/registry/scopes.json"'):].split("\n", 1)[0] + "\n"
tar_block = region(text, 'tar -czf "$TMP/$ART"', 'echo "INFO: built artifact')
bundle_dir = [ln for ln in text.split("\n") if ln.startswith("DASHBOARD_BUNDLE_DIR=")]
if not bundle_dir:
    raise SystemExit("DASHBOARD_BUNDLE_DIR= not found in the script")

root = tempfile.mkdtemp(prefix="ap23_tar_census_")
ws, src, tmp = (os.path.join(root, n) for n in ("ws", "src", "tmp"))
for repo_path in REFS.values():
    write(os.path.join(ws, repo_path), blob(TRUNK, repo_path))
write(os.path.join(ws, "lib/opal_naming.py"), blob(TRUNK, "lib/opal_naming.py"))
for name in REFS:
    write(os.path.join(src, name), b"DECOY untracked test copy -- must never ship\n")
write(os.path.join(src, "app/refs/other.json"), b"SRC-only file under app/refs\n")
write(os.path.join(src, "app/x.py"), b"print('x')\n")
write(os.path.join(src, "app/.env"), b"SECRET=1\n")
write(os.path.join(src, "app/audit.jsonl"), b"{}\n")
write(os.path.join(src, "app/run.log"), b"log\n")
write(os.path.join(src, "app/__pycache__/x.pyc"), b"pyc\n")
write(os.path.join(src, "deploy/d.sh"), b"d\n")
write(os.path.join(src, "requirements.txt"), b"r\n")
write(os.path.join(src, "identity_tool_allowlist.txt"), b"i\n")
os.makedirs(os.path.join(tmp, "bundle", "lib"), exist_ok=True)
write(os.path.join(tmp, "bundle", "dashboard", "index.html"), b"<html></html>\n")

prog = "\n".join([
    "set -euo pipefail",
    bundle_dir[0],
    "WORKSPACE_ROOT=%s" % json.dumps(posix(ws)),
    "SRC=%s" % json.dumps(posix(src)),
    "TMP=%s" % json.dumps(posix(tmp)),
    "ART=art.tgz",
    stage,
    tar_block,
])
sh = os.path.join(root, "run.sh")
write(sh, prog.encode("utf-8"))
r = subprocess.run(["bash", posix(sh)], capture_output=True)
if r.returncode != 0:
    sys.stderr.write(r.stderr.decode("utf-8", "replace"))
    raise SystemExit("the script's own staging and tar block failed rc=%d" % r.returncode)

members = {}
shipped = {}
with tarfile.open(os.path.join(tmp, "art.tgz"), "r:gz") as tf:
    names = [m.name.rstrip("/") for m in tf.getmembers()]
    for m in tf.getmembers():
        if m.isfile():
            shipped[m.name] = shipped.get(m.name, 0) + 1
    for name in REFS:
        data = tf.extractfile(name).read() if name in names else b""
        members[name] = {"count": names.count(name), "md5": md5(data) if data else None}
want = {name: md5(blob(TRUNK, repo)) for name, repo in REFS.items()}
res = {
    "members": members,
    "expected_md5_from_trunk_blobs": want,
    "trunk_sha": TRUNK,
    "archive_member_count": len(names),
    "src_only_file_shipped": shipped.get("app/refs/other.json", 0) == 1,
    "existing_excludes_hold": not any(n.endswith((".env", "audit.jsonl", "run.log", "x.pyc")) for n in names),
    "dashboard_and_lib_shipped": "dashboard/index.html" in names and any(n.startswith("lib") for n in names),
    "decoy_shipped": any(m["md5"] == md5(b"DECOY untracked test copy -- must never ship\n") for m in members.values()),
}
res["VERDICT"] = "PASS" if (
    all(members[n]["count"] == 1 and members[n]["md5"] == want[n] for n in REFS)
    and res["src_only_file_shipped"] and res["existing_excludes_hold"] and res["dashboard_and_lib_shipped"]
    and not res["decoy_shipped"]) else "FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, indent=1) + "\n")
print(json.dumps({k: res[k] for k in ("members", "src_only_file_shipped", "existing_excludes_hold", "decoy_shipped", "VERDICT")}))
sys.exit(0 if res["VERDICT"] == "PASS" else 1)
