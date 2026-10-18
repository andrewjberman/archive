#!/usr/bin/env python
"""OG-ap-38 Phase B step 7: land the EC2 manifest's standing clauses on the SHARED branch (box/sitez), the OG-ap-28 discipline.

The deploy wrapper rewrote the manifest inside the release tree, whose manifest baseline is older than trunk's; its own commit could not land there (the commit-time
naming gate needs the overlay that was restored for the clean check). So that file is a record of the deploy (its deployed_at is the wrapper's own timestamp, read
here), not the source of the trunk edit. The edit is made against THIS tree's manifest. The wrapper writes NO file_checksums, so the existing keys are recomputed from
the release tree's bytes and CROSS-CHECKED against the host's md5 read live over SSM; one disagreement refuses the whole edit. The key set is not widened.
mcportal_commit does not move (the dashboard bundle is the same pin).
usage: python ap36_manifest.py   (run from the repository root of the worktree on box/sitez; no argument)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time

import boto3

ROOT = os.getcwd()
TREE = "C:/tmp/og-rel-batch7"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "d077cef04333500595a7a531ebddc2f43e5f8789"          # the release that is live now
BASE = "efcc8ae19f7eebb04e2f45f45c0def28af037c24"             # the OG-ap-36 release, live before this deploy (the rollback commit)
SEAT = "0.7.0_AE_CloudOps~NFRA1"

wrapper = json.load(io.open(os.path.join(TREE, "infra", "aws", "ec2", "EC2_MANIFEST.json"), encoding="utf-8"))["services"]["opal-gateway"]
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
if head != RELEASE or wrapper.get("deployed_commit") != RELEASE:
    raise SystemExit("REFUSED: the release tree HEAD or its wrapper-written manifest is not the release")
DEPLOYED_AT = wrapper["deployed_at"]

FACTS = json.load(io.open(os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1", "ap38_facts.json"), encoding="utf-8"))
NOTE = (
    "NFRA_OPLGTW OG-ap-38 (round 41): the sixth batched release %s, the repair of the ARMED hazard Z-S375, was deployed at %s over %s (the OG-ap-36 release) with DEPLOY_BASE_REF=%s "
    "under the stale-base guard (equal at both checkpoints), three halves signed (CTO f6807b0bba, CVO f1ac7e004e, COO 371e908238) on ask sha256 33686c0a63cb. It is code and unit only: "
    "app/typed_scope.py (OG-en-25 and OG-en-26: read_parquet refuses an unfiltered read over 64 MB of Arrow from the file footer and streams a filtered read by batch, only the matched rows kept; "
    "distinct_values), app/etfs_rivals_flow.py (the peer tables read with the filters pushed in, input_manifest measured and never loaded), deploy/opal-gateway.service (OG-un-1: MemoryHigh=1200M, "
    "MemoryMax=1400M, OOMScoreAdjust=300, live: systemctl and the cgroup memory.max read 1468006400) and two tests. NO IAM moved, no env key and no tool changed (registry 103, tools/list 103, "
    ".env 65 keys, health 200, host md5 139 of 139 equal to the release blobs, the marker /opt/opal-gateway/.deployed_commit reads the release sha). %s "
    "Ledger nfra-oplgtw-gateway-release-batch7. Rollback target: the pre-deploy content held by %s (S3 tarball opal-gateway-efcc8ae19f.tar.gz, 900200 bytes, sha256 b07656f114f9); "
    "the rollback reinstalls the old unit WITHOUT the limits and rewrites the marker. ||| PREVIOUS: " % (RELEASE, DEPLOYED_AT, BASE, BASE, FACTS["served_sentence"], BASE))

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
