#!/usr/bin/env python
"""OG-ap-28 Phase B step 6: land the EC2 manifest's standing clauses on the SHARED tree.

Same discipline as OG-ap-21's p21_manifest.py: the wrapper committed its manifest edit inside the release worktree, whose manifest
baseline is OLDER than trunk's (it still reads previous_deployed_commit=2c0f84966d), so that commit is a record of the deploy, not
the source of the trunk edit. The edit is made against the SHARED tree's own content. The wrapper writes NO file_checksums, so the
10 existing keys are recomputed from the release worktree's own bytes and CROSS-CHECKED against the host's md5 read live over SSM;
a single disagreement refuses the whole edit. The key set is not widened.

One field beyond the p21 edit: services.opal-gateway.mcportal_commit moves 17dcbb28624e -> 090b9cdc85ce, because the live dashboard
bundle was built from the release's pin and a later deploy from trunk would otherwise rebuild the old bundle.

usage: python ap28_manifest.py        (run from the repository root; no argument)
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
TREE = "C:/tmp/og-rel-batch2"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "bf9d23b518527e0e5f9a26aa240fd5af72af6c11"
BASE = "d14445961dd6d04275ca8186372a4df4c4fcc5cc"
MCP_OLD, MCP_NEW = "c66ca82952c01575968d16cc736cdabe36606572", "59e802a4185a62129bf28ebb4df6eda9b70e03ff"
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
    "NFRA_OPLGTW OG-ap-28 (round 38, workstream ENRICH-R38-E, FWD-21 and FWD-22; the round-38 batched gateway release): release commit %s "
    "(branch rel-nfra-oplgtw-batch2, local, never merged; the naming-gate prelude 2dc919cf26 sits below it) deployed %s with DEPLOY_BASE_REF=%s; the "
    "stale-base guard read the live ref EQUAL at both checkpoints. Cut from trunk 858e927558. Carries: units and currency on client position rows "
    "(OG-en-4: weight_unit, currency, currency_basis; currency is null with source_absent where the source has none), coverage_floor beside an empty "
    "news answer (OG-en-5), trading_days_behind_t1 on the chatter answer (OG-en-6), the Muse client narrowing INERT (MUSE_CLIENT_ID is not set; OG-en-8), "
    "a key with no catalog row answers 404 (OG-en-9), a 429 writes one audit row event=gw_ratelimit with a hashed by_client split and the 120 per 60 s "
    "limit unchanged (OG-en-10), the four 49F Black Diamond -live tools routed to the key blackdiamond49flive and read from opal-data-bd through "
    "gateway-49f-blackdiamond-live-read-role (OG-en-12), the catalog DATA_CATALOG.yaml whole at blob b81c48aa3c (NFRA_MCPINDEX MX-c-26), the seventh "
    "reader key BLACKDIAMOND49FLIVE_READER_ROLE_ARN written into the rebuilt .env (.env 64 -> 65 key names), and mcportal_commit %s -> %s. NO IAM moved "
    "and no tool was added or removed (registry 103 before and after). Read-back: 139 of 139 host files md5 == the release across app, deploy and lib "
    "(SSM; plus the two staged app/refs files equal to trunk), served read per_tool_good 27 of 27, tools/list 103 before and after, health 200, six of "
    "seven arms true (e4 false: row Z-S305). Ledger nfra-oplgtw-gateway-release-batch2. Halves: CTO 87e4e8a540, COO ce4ce4fea9, CVO ffc2045889, pinned to "
    "%s against ask sha aa5d0a37682e. Rollback: redeploy the base %s with DEPLOY_BASE_REF=%s; the manifest pin returns with it, no IAM moves with it. "
    "||| PREVIOUS: "
    % (RELEASE, DEPLOYED_AT, BASE, MCP_OLD[:12], MCP_NEW[:12], RELEASE[:10], BASE[:10], RELEASE))

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
