#!/usr/bin/env python
"""OG-ap-23 Phase B step 6: land the EC2 manifest's standing clauses on the SHARED tree.

Same discipline as OG-ap-21's p21_manifest.py: the wrapper committed its manifest edit inside the release worktree, whose manifest
baseline is OLDER than trunk's (it still reads previous_deployed_commit=2c0f84966d), so that commit is a record of the deploy, not
the source of the trunk edit. The edit is made against the SHARED tree's own content. The wrapper writes NO file_checksums, so the
10 existing keys are recomputed from the release worktree's own bytes and CROSS-CHECKED against the host's md5 read live over SSM;
a single disagreement refuses the whole edit. The key set is not widened.

One field beyond the p21 edit: services.opal-gateway.mcportal_commit moves 17dcbb28624e -> 090b9cdc85ce, because the live dashboard
bundle was built from the release's pin and a later deploy from trunk would otherwise rebuild the old bundle.

usage: python ap23_manifest.py        (run from the repository root; no argument)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time

import boto3

ROOT = os.getcwd()
TREE = "C:/tmp/og-rel-code"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4"
BASE = "d577e0e7297b3ecba183023d8374855a93f148a7"
MCP_OLD, MCP_NEW = "17dcbb28624eab147318052f58bcc39b8eb8029c", "090b9cdc85ce3463e73915e68b44f4c21053a71c"
SEAT = "0.7.0_AE_CloudOps~Z"

# the wrapper's own timestamp, read from the manifest commit it made on top of the release, never a fresh clock
wr = subprocess.run(["git", "-C", TREE, "show", "HEAD:infra/aws/ec2/EC2_MANIFEST.json"], capture_output=True).stdout.decode("utf-8")
wrapper = json.loads(wr)["services"]["opal-gateway"]
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
parent = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD^"], capture_output=True).stdout.decode().strip()
if parent != RELEASE or wrapper.get("deployed_commit") != RELEASE:
    raise SystemExit("REFUSED: the deploy tree's HEAD is not the wrapper's manifest commit over the release")
DEPLOYED_AT = wrapper["deployed_at"]

NOTE = (
    "NFRA_OPLGTW OG-ap-23 (round 37, workstream CODE-BATCH, FWD-22; the code batch release): release commit %s (branch "
    "rel-nfra-oplgtw-code-a5 and -a6, local, never merged; 48 files vs %s) deployed %s with DEPLOY_BASE_REF=%s; the stale-base "
    "guard read the live ref EQUAL at both checkpoints. Carries: 27 added READ tools, registry 76 -> 103 (read from "
    "app.tools.mcp._tool_manager.list_tools() on the host) -- rival funds 10, client 5, silver etfs 3, json-served 7, model composition 1, "
    "security classification 1; the five client_* tools are the data-grant, tier-admitted class (CLIENT_TOOLS), master_admin only "
    "(PRD v3.14, OG-ad-1); app/data_entitlement.py taken WHOLE, which delivers OG-bd-3 (CTO msg 33941): a profiled master_admin is admitted "
    "to the six tier-admitted tools whatever its profile's state; the six vendor reader keys (BLACKDIAMOND49F, BLACKDIAMONDCOTTONWOOD, "
    "ORION, ECLIPSE, COMMONWEALTH, SMARTX _READER_ROLE_ARN) written into the rebuilt .env, each ARN read from IAM and compared to the "
    "expected ARN in the resolved account before the upload (.env 58 -> 64 key names, none removed); and the roster and registry copy "
    "(app/refs/partner_roster.json, app/refs/scopes.json) staged at bundle time from data/mdpf/config/partner_roster.json and "
    "infra/logic/registry/scopes.json and shipped from the bundle group of the tar line, never committed (W/ap23_tar_census.json: each "
    "once, md5 equal to trunk 23587956e9's blobs). mcportal_commit %s -> %s. NO IAM moved in this release: the four internal-reader grants "
    "its etfs_silver tools and mdpf_get_model_composition need are OG-ap-27's, and the classification grant is OG-ap-26's. FIRST ATTEMPT "
    "ROLLED BACK: deployed 2026-10-16T08:13:44Z, 23 of 27 tools served and 4 answered AccessDenied before OG-ap-27, redeployed the base "
    "08:28:16Z under COO condition C5 (row Z-S164); this is the second attempt. Read-back: 141 of 141 host files md5 == the release across "
    "app, deploy and lib (SSM), served read per_tool_good 27 of 27 through the installed code (non-Opal refused with 0 reads), "
    "client_admission true (an unprofiled non-admin refused on all five client tools with 0 data reads, a master_admin stand-in served), "
    "mdpf_get_security_classification run as assumed-role gateway-global-internal-reader-role beside an instance identity of "
    "opal-gateway-role/%s, CVO C1 a real sts:AssumeRole of gateway-smartx-read-role, C2 the SmartX two-firm arm (firm A 12 rows, the "
    "other firm 0). Ledger nfra-oplgtw-gateway-release-code. Halves: CTO @2665f19c6a, COO @f94bcaf1e5, CVO @49ebdc867a, pinned to %s "
    "against ask sha ba5b9325bca5. Rollback: redeploy the base %s with DEPLOY_BASE_REF=%s; no IAM moves with it, and OG-ap-26 and "
    "OG-ap-27 stay (they are grants, not part of this binary). ||| PREVIOUS: "
    % (RELEASE, BASE[:10], DEPLOYED_AT, BASE, MCP_OLD[:12], MCP_NEW[:12], INSTANCE, RELEASE[:10], BASE[:10], RELEASE))

dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--", "infra/aws/ec2/EC2_MANIFEST.json"],
                       capture_output=True).stdout.decode().strip()
if dirty:
    raise SystemExit("REFUSED: the shared manifest is already modified (%r) -- a peer may be mid-edit" % dirty)
man = json.load(io.open(MANIFEST, encoding="utf-8"))
svc = man["services"]["opal-gateway"]
if svc["deployed_commit"] != BASE:
    raise SystemExit("REFUSED: trunk's deployed_commit is %s, not the base %s" % (svc["deployed_commit"], BASE))
if svc.get("mcportal_commit") != MCP_OLD:
    raise SystemExit("REFUSED: trunk's mcportal_commit is %s, not %s" % (svc.get("mcportal_commit"), MCP_OLD))

keys = sorted(svc["file_checksums"])
print("file_checksums key set (unchanged, %d keys): %s" % (len(keys), keys))


def local_md5(rel):
    p = os.path.join(TREE, rel) if rel.startswith("lib/") else os.path.join(SRC, rel)
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


release_sums = {k: local_md5(k) for k in keys}
cmd = "cd /opt/opal-gateway && md5sum " + " ".join(keys)
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                       Parameters={"commands": [cmd]})["Command"]["CommandId"]
inv = None
for _ in range(40):
    time.sleep(3)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
if inv["Status"] != "Success":
    raise SystemExit("REFUSED: the host md5 control did not run (%s)" % inv["Status"])
host = {}
for line in inv["StandardOutputContent"].splitlines():
    line = line.strip()
    if " " in line:
        h, p = line.split(None, 1)
        host[p.strip()] = h
bad = [(k, release_sums[k], host.get(k)) for k in keys if host.get(k) != release_sums[k]]
print("host control: %d of %d paths read, %d disagree" % (len(host), len(keys), len(bad)))
if bad:
    raise SystemExit("REFUSED: the release and the host disagree on %s -- the manifest is not written" % [b[0] for b in bad])
changed = {k: (svc["file_checksums"][k], release_sums[k]) for k in keys if svc["file_checksums"][k] != release_sums[k]}
print("checksums that MOVE with this release: %d of %d" % (len(changed), len(keys)))
for k, (o, n) in sorted(changed.items()):
    print("  %-34s %s -> %s" % (k, o, n))

svc["previous_deployed_commit"] = svc["deployed_commit"]
svc["deployed_commit"] = RELEASE
svc["deployed_at"] = DEPLOYED_AT
svc["deployed_by"] = SEAT
svc["mcportal_commit"] = MCP_NEW
svc["file_checksums"] = {k: release_sums[k] for k in keys}
svc["release_note"] = NOTE + svc["release_note"]
man["_last_updated"] = DEPLOYED_AT
io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(json.dumps(man, indent=2) + "\n")
print("WROTE %s" % MANIFEST)
print("  deployed_commit %s -> %s ; previous %s ; mcportal %s -> %s ; deployed_at %s"
      % (BASE[:10], RELEASE[:10], svc["previous_deployed_commit"][:10], MCP_OLD[:10], MCP_NEW[:10], DEPLOYED_AT))
