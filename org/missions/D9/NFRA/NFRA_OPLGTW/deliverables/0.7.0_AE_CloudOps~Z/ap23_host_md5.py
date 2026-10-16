#!/usr/bin/env python
"""OG-ap-23 Phase B, deploy leg: the SSM md5 walk -- the HOST'S OWN bytes against the release.

Three families of expectation, each with its own source (a walk compared to one source only would let a staged file pass
by being compared to itself):
  1. app/ and deploy/ tracked files, requirements.txt and identity_tool_allowlist.txt: the release WORKTREE's bytes
     (what the tar actually packed, so a line-ending difference cannot turn a correct deploy red); the worktree-equals-commit
     link is made separately by `git status --porcelain` over the same paths plus an ancestor read.
  2. lib/trading_calendar.py and lib/opal_naming.py: the release worktree's lib/ bytes (the calendar ships from the release
     tree; opal_naming is the release blob).
  3. app/refs/partner_roster.json and app/refs/scopes.json: NOT in the release commit. Their expected md5 is the md5 of the
     blob at trunk_sha of data/mdpf/config/partner_roster.json and infra/logic/registry/scopes.json (read with git show),
     because those are the files the deploy script stages into the bundle from the repo sources.
The dashboard bundle is EXCLUDED and said so: it is built from the mcportal checkout, so no release blob exists to compare.

usage: python ap23_host_md5.py <out.json>        (run from the repository root)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
TREE = "C:/tmp/og-rel-code"
REC = json.load(open("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap23_release.json", encoding="utf-8"))
RELEASE, TRUNK = REC["release_sha"], REC["trunk_sha"]
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
REMOTE = "/opt/opal-gateway"
OUT = sys.argv[1]
REFS = {"app/refs/partner_roster.json": "data/mdpf/config/partner_roster.json",
        "app/refs/scopes.json": "infra/logic/registry/scopes.json"}


def md5(data):
    return hashlib.md5(data).hexdigest()


PAIRS = {}
for fam in ("app", "deploy"):
    for root, dirs, files in os.walk(os.path.join(SRC, fam)):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn.endswith((".log", ".pyc")) or fn in (".env", "audit.jsonl"):
                continue
            lp = os.path.join(root, fn)
            PAIRS[os.path.relpath(lp, SRC).replace(os.sep, "/")] = lp
for fn in ("requirements.txt", "identity_tool_allowlist.txt"):
    PAIRS[fn] = os.path.join(SRC, fn)
PAIRS["lib/trading_calendar.py"] = os.path.join(TREE, "lib", "trading_calendar.py")
PAIRS["lib/opal_naming.py"] = os.path.join(TREE, "lib", "opal_naming.py")
for name in REFS:
    PAIRS.pop(name, None)           # an untracked test copy must never be the expectation

local = {k: md5(io.open(v, "rb").read()) for k, v in sorted(PAIRS.items())}
for name, repo in REFS.items():
    blob = subprocess.run(["git", "show", "%s:%s" % (TRUNK, repo)], capture_output=True).stdout
    if not blob:
        raise SystemExit("cannot read %s:%s" % (TRUNK, repo))
    local[name] = md5(blob)

pathspecs = ["infra/aws/ec2/opal-gateway/" + k for k in PAIRS if not k.startswith("lib/")] + ["lib/trading_calendar.py", "lib/opal_naming.py"]
dirty = subprocess.run(["git", "-C", TREE, "status", "--porcelain", "--"] + pathspecs,
                       capture_output=True).stdout.decode("utf-8", "replace").strip()
cont = subprocess.run(["git", "-C", TREE, "merge-base", "--is-ancestor", RELEASE, "HEAD"]).returncode
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
parent = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD^"], capture_output=True).stdout.decode().strip()

cmd = ("echo BEGIN_WALK && cd %s && find app deploy lib -type f ! -path '*__pycache__*' ! -name '*.pyc' | sort "
       "| xargs md5sum && md5sum requirements.txt identity_tool_allowlist.txt && echo END_WALK" % REMOTE)
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                       Parameters={"commands": [cmd]})["Command"]["CommandId"]
inv = None
for _ in range(60):
    time.sleep(3)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
if inv is None or inv["Status"] != "Success":
    raise SystemExit("SSM walk did not succeed: status=%s stderr=%s" % (inv and inv["Status"], (inv or {}).get("StandardErrorContent", "")[:400]))
out = inv["StandardOutputContent"]
if "BEGIN_WALK" not in out or "END_WALK" not in out:
    raise SystemExit("the walk output is not bracketed: a truncated read must not pass as complete")
host = {}
for line in out.splitlines():
    line = line.strip()
    if not line or " " not in line or line in ("BEGIN_WALK", "END_WALK"):
        continue
    h, p = line.split(None, 1)
    host[p.strip()] = h

equal, differ, missing = [], [], []
for k, h in local.items():
    if k not in host:
        missing.append(k)
    elif host[k] == h:
        equal.append(k)
    else:
        differ.append({"path": k, "expected": h, "host": host[k]})
extra = [k for k in host if k not in local]
res = {"instance": INSTANCE, "release": RELEASE, "trunk": TRUNK, "deploy_tree_head": head, "deploy_tree_parent": parent,
       "release_is_ancestor_of_head": cont == 0, "worktree_dirty_over_deployed_paths": dirty.splitlines(),
       "ssm_status": inv["Status"], "command_id": cid, "denominator_expected_files": len(local), "denominator_host_files": len(host),
       "equal": len(equal), "differ": differ, "missing_on_host": missing, "extra_on_host": extra,
       "app_refs_equal_to_trunk_blobs": {k: (host.get(k) == local[k]) for k in REFS},
       "dashboard": "excluded by grain: built from the mcportal checkout, no release blob to compare"}
fails = []
if differ:
    fails.append("%d file(s) differ" % len(differ))
if missing:
    fails.append("%d expected file(s) absent on the host: %s" % (len(missing), missing[:10]))
if extra:
    fails.append("%d host file(s) no expectation explains: %s" % (len(extra), extra[:10]))
if dirty:
    fails.append("the release worktree is dirty over the deployed paths")
if cont != 0:
    fails.append("the release commit is NOT an ancestor of the deploy tree HEAD")
res["VERDICT"] = "PASS" if not fails else "FAIL"
res["FAILS"] = fails
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1) + "\n")
print("WROTE %s" % OUT)
print("  host files %d / expected files %d -> EQUAL %d, DIFFER %d, MISSING-ON-HOST %d, EXTRA-ON-HOST %d"
      % (len(host), len(local), len(equal), len(differ), len(missing), len(extra)))
print("  app/refs equal to trunk blobs: %s" % res["app_refs_equal_to_trunk_blobs"])
print("  worktree clean over the deployed paths: %s ; release is ancestor of HEAD %s: %s ; head parent %s"
      % (not dirty, head[:10], cont == 0, parent[:10]))
print("  VERDICT: " + res["VERDICT"])
for x in fails:
    print("  FAIL: " + x)
sys.exit(0 if not fails else 1)
