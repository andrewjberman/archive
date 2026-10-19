#!/usr/bin/env python
"""OG-rz-2 Phase B: land the EC2 manifest's standing clauses on the SHARED branch (box/sitez), the OG-ap-28 discipline.

The deploy wrapper rewrote the manifest inside the release tree, whose manifest baseline is older than trunk's; its own commit could not land there (the commit-time
naming gate needs the overlay that was restored for the clean check). So that file is a record of the deploy (its deployed_at is the wrapper's own timestamp, read
here), not the source of the trunk edit. The edit is made against THIS tree's manifest. The wrapper writes NO file_checksums, so the existing keys are recomputed from
the release tree's bytes and CROSS-CHECKED against the host's md5 read live over SSM; one disagreement refuses the whole edit. The key set is not widened.
mcportal_commit does not move (the dashboard bundle is the same pin).
usage: python ap48_manifest.py   (run from the repository root of the worktree on box/sitez; no argument)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time

import boto3

ROOT = os.getcwd()
TREE = "C:/tmp/og-rel-batch15"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "13917ef993207bee6b8df0124eec5444da4d62cd"          # the release that is live now
BASE = "6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c"             # OG-ap-50's release, live before this deploy (the rollback commit)
SEAT = "0.7.0_AE_CloudOps~NFRA1"

wrapper = json.load(io.open(os.path.join(TREE, "infra", "aws", "ec2", "EC2_MANIFEST.json"), encoding="utf-8"))["services"]["opal-gateway"]
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
if head != RELEASE or wrapper.get("deployed_commit") != RELEASE:
    raise SystemExit("REFUSED: the release tree HEAD or its wrapper-written manifest is not the release")
DEPLOYED_AT = wrapper["deployed_at"]

SERVED = json.load(io.open(os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1", "RZ2_SERVED.json"), encoding="utf-8"))["body"]
NOTE = (
    "NFRA_OPLGTW OG-rz-2 (round 46): the host was resized from t4g.small to t4g.large (in place, targeted safe-apply, main.tf blob 1cf3c199cb2c; downtime %s s) and THEN the fourteenth batched release %s was deployed at %s over %s (OG-ap-50) with DEPLOY_BASE_REF=%s "
    "under the stale-base guard, three halves signed (CTO f39cd21642, COO H1-H8, CVO 86c19380ab) on ask sha256 5dfadc6c78c3. Ten files whole from trunk 9095ce68f3: OG-rz-1 (deploy/opal-gateway.service MemoryHigh 5600M and MemoryMax 6400M, tests/test_og_un1.py, "
    "the deploy contract target_instance_type t4g.large) and OG-ms-1 (Schwab master 08403355 registered in MASTERS, the audit set, both contract copies and the staged scopes.json; the client tools keep refusing 0840). The limits were released only AFTER the resize. "
    "NO IAM moved, no env key, no tool changed, NO arming and NO SSM write; registry %s, tools/list %s, .env %s keys, health %s, host md5 %s of %s equal to the release blobs, host memory total %s MB, the marker reads the release sha; the two large replies "
    "(mdpf_get_aggregate_aua and opal_discover), one at a time, completed under MemoryHigh. Ledger nfra-oplgtw-gateway-resize-t4g-large. Rollback target: the pre-deploy content held by %s (S3 tarball opal-gateway-6d1b5dcb64b.tar.gz, 922315 bytes, sha256 e7cd9de1617a); "
    "the SAFE order is the tarball first (limits back to 1200M and 1400M), THEN t4g.small. ||| PREVIOUS: "
    % (SERVED["downtime"]["downtime_seconds"], RELEASE, DEPLOYED_AT, BASE, BASE, SERVED["registry_count"], SERVED["tools_list"], SERVED["env_key_count"], SERVED["health_after"], SERVED["host_md5"]["equal"], SERVED["host_md5"]["expected_files"],
       SERVED["memory_total_mb"], BASE))

dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--", "infra/aws/ec2/EC2_MANIFEST.json"], capture_output=True).stdout.decode().strip()
if dirty:
    raise SystemExit("REFUSED: this tree's manifest is already modified (%r)" % dirty)
man = json.load(io.open(MANIFEST, encoding="utf-8"))
svc = man["services"]["opal-gateway"]
if svc["deployed_commit"] != BASE:
    raise SystemExit("REFUSED: this branch's deployed_commit is %s, not the base %s" % (svc["deployed_commit"], BASE))

keys = sorted(svc["file_checksums"])
print("file_checksums key set (unchanged, %d keys): %s" % (len(keys), keys))


def local_md5(rel):
    p = os.path.join(TREE, rel) if rel.startswith("lib/") else os.path.join(SRC, rel)
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


release_sums = {k: local_md5(k) for k in keys}
cmd = "cd /opt/opal-gateway && md5sum " + " ".join(keys)
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
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
print("host control: %d of %d paths read, %d disagree (ssm:%s)" % (len(host), len(keys), len(bad), cid))
if bad:
    raise SystemExit("REFUSED: the release and the host disagree on %s -- the manifest is not written" % [b[0] for b in bad])
changed = {k: (svc["file_checksums"][k], release_sums[k]) for k in keys if svc["file_checksums"][k] != release_sums[k]}
print("checksums that MOVE with this release: %d of %d" % (len(changed), len(keys)))
for k, (o, n) in sorted(changed.items()):
    print("  %-34s %s -> %s" % (k, o, n))

svc["previous_deployed_commit"] = BASE
svc["deployed_commit"] = RELEASE
svc["deployed_at"] = DEPLOYED_AT
svc["deployed_by"] = SEAT
svc["file_checksums"] = {k: release_sums[k] for k in keys}
svc["release_note"] = NOTE + svc["release_note"]
man["_last_updated"] = DEPLOYED_AT
io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(json.dumps(man, indent=2) + "\n")
print("WROTE %s" % MANIFEST)
print("  deployed_commit %s -> %s ; previous %s ; deployed_at %s" % (BASE[:10], RELEASE[:10], svc["previous_deployed_commit"][:10], DEPLOYED_AT))
