#!/usr/bin/env python
"""OG-ap-21 Phase B, deploy leg: the SSM md5 walk -- the HOST'S OWN bytes against the release blobs.

An S3 ETag is not proof here (cloud-ops rule: the S3 copy can be current while the baked copy is
stale), and neither is the deploy script's own rc=0. The only sound oracle is md5 read ON THE
INSTANCE from the path the service runs out of.

WHAT IS COMPARED, AND AGAINST WHAT: the artifact tars the release WORKTREE's files, so the host is
compared against those same working-tree bytes -- not against `git cat-file blob`, which would
differ on line endings alone and turn a correct deploy into a red walk. The worktree-equals-commit
claim is made separately, by `git status --porcelain` over the same paths, so the chain host ->
worktree -> release commit is complete and each link has its own instrument.

The three families the leg names (app, deploy, lib) plus the two loose files the tar packs. The
dashboard bundle is EXCLUDED and said so: it is built from the mcportal checkout, not from this
repo, so no release blob exists to compare it to -- an absence that is declared, never a silent skip.
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
RELEASE = "d577e0e7297b3ecba183023d8374855a93f148a7"
TREE = r"C:\tmp\og-rel-p21"
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
REMOTE = "/opt/opal-gateway"
OUT = sys.argv[1]

# host-relative path -> local file that produced it
PAIRS = {}
for fam in ("app", "deploy"):
    base = os.path.join(SRC, fam)
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn.endswith((".log", ".pyc")) or fn in (".env", "audit.jsonl"):
                continue
            lp = os.path.join(root, fn)
            rel = os.path.relpath(lp, SRC).replace(os.sep, "/")
            PAIRS[rel] = lp
for fn in ("requirements.txt", "identity_tool_allowlist.txt"):
    PAIRS[fn] = os.path.join(SRC, fn)
PAIRS["lib/trading_calendar.py"] = os.path.join(TREE, "lib", "trading_calendar.py")


def md5(p):
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


local = {k: md5(v) for k, v in sorted(PAIRS.items())}

# --- link 2: the worktree IS the release commit, over exactly these paths -------------------
pathspecs = ["infra/aws/ec2/opal-gateway/" + k for k in PAIRS if not k.startswith("lib/")]
pathspecs.append("lib/trading_calendar.py")
dirty = subprocess.run(["git", "-C", TREE, "status", "--porcelain", "--"] + pathspecs,
                       capture_output=True).stdout.decode("utf-8", "replace").strip()
# and that HEAD still CONTAINS the release commit (the wrapper added a manifest commit on top)
cont = subprocess.run(["git", "-C", TREE, "merge-base", "--is-ancestor", RELEASE, "HEAD"]).returncode
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"],
                      capture_output=True).stdout.decode().strip()

# --- link 1: the host's own md5 ------------------------------------------------------------
cmd = ("cd %s && find app deploy lib -type f ! -path '*__pycache__*' ! -name '*.pyc' | sort "
       "| xargs md5sum && md5sum requirements.txt identity_tool_allowlist.txt" % REMOTE)
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
    raise SystemExit("SSM walk did not succeed: status=%s stderr=%s"
                     % (inv and inv["Status"], (inv or {}).get("StandardErrorContent", "")[:400]))

host = {}
for line in inv["StandardOutputContent"].splitlines():
    line = line.strip()
    if not line or " " not in line:
        continue
    h, p = line.split(None, 1)
    host[p.strip()] = h

# --- grade ---------------------------------------------------------------------------------
equal, differ, missing_on_host, extra_on_host = [], [], [], []
for k, h in local.items():
    if k not in host:
        missing_on_host.append(k)
    elif host[k] == h:
        equal.append(k)
    else:
        differ.append({"path": k, "release": h, "host": host[k]})
DASH_PREFIX = ("app/static/dashboard/", "app/static/mcportal/")
for k in host:
    if k not in local:
        extra_on_host.append(k)
declared_bundle = [k for k in extra_on_host if k.startswith(DASH_PREFIX)]
other_extra = [k for k in extra_on_host if k not in declared_bundle]

res = {"instance": INSTANCE, "release": RELEASE, "deploy_tree_head": head,
       "release_is_ancestor_of_head": cont == 0,
       "worktree_dirty_over_deployed_paths": dirty.splitlines(),
       "ssm_status": inv["Status"], "command_id": cid,
       "denominator_release_files": len(local), "denominator_host_files": len(host),
       "equal": len(equal), "differ": differ,
       "missing_on_host": missing_on_host,
       "extra_on_host_declared_dashboard_bundle": len(declared_bundle),
       "extra_on_host_other": other_extra}
fails = []
if differ:
    fails.append("%d file(s) differ between the host and the release" % len(differ))
if missing_on_host:
    fails.append("%d release file(s) absent on the host: %s" % (len(missing_on_host), missing_on_host[:10]))
if dirty:
    fails.append("the release worktree is dirty over the deployed paths")
if cont != 0:
    fails.append("the release commit is NOT an ancestor of the deploy tree HEAD")
if other_extra:
    fails.append("%d host file(s) no release blob explains (and not the declared dashboard bundle): %s"
                 % (len(other_extra), other_extra[:10]))
res["VERDICT"] = "PASS" if not fails else "FAIL"
res["FAILS"] = fails
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1) + "\n")
print("WROTE %s" % OUT)
print("  host files %d / release files %d -> EQUAL %d, DIFFER %d, MISSING-ON-HOST %d"
      % (len(host), len(local), len(equal), len(differ), len(missing_on_host)))
print("  dashboard-bundle files on the host with no release blob (declared, excluded): %d" % len(declared_bundle))
print("  other unexplained host files: %d" % len(other_extra))
print("  worktree clean over the deployed paths: %s ; release is ancestor of HEAD %s: %s"
      % (not dirty, head[:10], cont == 0))
print("  VERDICT: " + res["VERDICT"])
for x in fails:
    print("  FAIL: " + x)
sys.exit(0 if not fails else 1)
