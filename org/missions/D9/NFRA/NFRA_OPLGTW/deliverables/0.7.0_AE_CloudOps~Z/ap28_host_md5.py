#!/usr/bin/env python
"""OG-ap-28 Phase A step 1: the SSM md5 walk of the HOST against the LIVE ref, plus the .env NAMES (never values).

usage: python ap28_host_md5.py <live_ref> <out.json>   (repository root; read-only)

Expected bytes = the git blobs of the live ref over app/, deploy/, requirements.txt, identity_tool_allowlist.txt and lib/trading_calendar.py + lib/opal_naming.py. A host file whose md5
differs from the blob is ALSO tried against the blob with CRLF line endings (a Windows checkout packs what is on disk), and the classification says which. app/refs/partner_roster.json
and scopes.json are not in the live ref (the deploy script stages them from the repo): they are compared to the current trunk blobs and reported, not graded. The dashboard bundle is
EXCLUDED by grain (built from the mcportal checkout; no release blob exists to compare).
The same SSM command reads the .env KEY NAMES: how many keys, how many end in _READER_ROLE_ARN, whether MUSE_CLIENT_ID is a key, whether BLACKDIAMOND49FLIVE_READER_ROLE_ARN is. A value is never printed."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import time

import boto3

LIVE, OUT = sys.argv[1:3]
INSTANCE = "i-07dccb1615503ac99"
G = "infra/aws/ec2/opal-gateway/"
REMOTE = "/opt/opal-gateway"


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


def md5(b):
    return hashlib.md5(b).hexdigest()


paths = git("ls-tree", "-r", "--name-only", LIVE, "--", G + "app/", G + "deploy/", G + "requirements.txt", G + "identity_tool_allowlist.txt").stdout.decode().split()
exp = {}
for p in paths:
    rel = p[len(G):]
    if "__pycache__" in rel or rel.endswith((".pyc", ".log")):
        continue
    exp[rel] = git("show", "%s:%s" % (LIVE, p)).stdout
for p in ("lib/trading_calendar.py", "lib/opal_naming.py"):
    b = git("show", "%s:%s" % (LIVE, p))
    if b.returncode == 0:
        exp[p] = b.stdout
cmd = ("echo BEGIN_WALK && cd %s && find app deploy lib -type f ! -path '*__pycache__*' ! -name '*.pyc' | sort | xargs md5sum && md5sum requirements.txt identity_tool_allowlist.txt && echo END_WALK"
       " && echo BEGIN_ENV && grep -E '^[A-Za-z0-9_]+=' .env | cut -d= -f1 | sort && echo END_ENV" % REMOTE)
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
inv = None
for _ in range(80):
    time.sleep(3)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
if inv["Status"] != "Success":
    raise SystemExit("SSM walk did not succeed: %s %s" % (inv["Status"], inv.get("StandardErrorContent", "")[:300]))
out = inv["StandardOutputContent"]
for tok in ("BEGIN_WALK", "END_WALK", "BEGIN_ENV", "END_ENV"):
    if tok not in out:
        raise SystemExit("output not bracketed (%s missing): a truncated read must not pass as complete" % tok)
walk = out.split("BEGIN_WALK", 1)[1].split("END_WALK", 1)[0]
envn = [ln.strip() for ln in out.split("BEGIN_ENV", 1)[1].split("END_ENV", 1)[0].splitlines() if ln.strip()]
host = {}
for ln in walk.splitlines():
    ln = ln.strip()
    if ln and " " in ln:
        h, p = ln.split(None, 1)
        host[p.strip()] = h
equal = crlf_equal = 0
differ, missing = [], []
for k, b in sorted(exp.items()):
    if k not in host:
        missing.append(k)
    elif host[k] == md5(b):
        equal += 1
    elif host[k] == md5(b.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")):
        crlf_equal += 1
    else:
        differ.append(k)
refs = {"app/refs/partner_roster.json": "data/mdpf/config/partner_roster.json", "app/refs/scopes.json": "infra/logic/registry/scopes.json"}
extra = [k for k in host if k not in exp and k not in refs]
trunk = sys.argv[3] if len(sys.argv) > 3 else None
refs_state = {}
for k, repo in refs.items():
    if trunk:
        refs_state[k] = {"on_host": k in host, "equals_trunk_blob": (host.get(k) == md5(git("show", "%s:%s" % (trunk, repo)).stdout)) if k in host else None}
    else:
        refs_state[k] = {"on_host": k in host}
res = {"instance": INSTANCE, "live_ref": LIVE, "ssm_command_id": cid, "denominator_expected_files": len(exp), "denominator_host_files": len(host),
       "equal_lf": equal, "equal_crlf_only": crlf_equal, "differ": differ, "missing_on_host": missing, "extra_on_host_unexplained": extra, "refs": refs_state,
       "dashboard": "excluded by grain: built from the mcportal checkout, no release blob to compare",
       "env": {"key_count": len(envn), "reader_role_arn_keys": sorted(k for k in envn if k.endswith("_READER_ROLE_ARN")),
               "muse_client_id_is_a_key": "MUSE_CLIENT_ID" in envn, "bd49flive_key_present": "BLACKDIAMOND49FLIVE_READER_ROLE_ARN" in envn}}
res["VERDICT"] = "MATCH" if not (differ or missing) else "MISMATCH"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1) + "\n")
print("expected files %d / host files %d -> EQUAL (LF) %d, EQUAL (CRLF only) %d, DIFFER %d, MISSING-ON-HOST %d, EXTRA-ON-HOST %d" % (len(exp), len(host), equal, crlf_equal, len(differ), len(missing), len(extra)))
print("differ: %s ; missing: %s ; extra: %s" % (differ[:8], missing[:8], extra[:8]))
print("refs: %s" % refs_state)
print("env: %d keys, reader keys %d, MUSE_CLIENT_ID key %s, BD49FLIVE key %s" % (len(envn), len(res["env"]["reader_role_arn_keys"]), res["env"]["muse_client_id_is_a_key"], res["env"]["bd49flive_key_present"]))
print("VERDICT: " + res["VERDICT"])
