#!/usr/bin/env python
"""OG-ap-32 Phase B step 6: land the EC2 manifest's standing clauses on the SHARED branch (box/sitez), the OG-ap-28 discipline.

The deploy wrapper rewrote the manifest inside the release tree, whose manifest baseline is older than trunk's; its own commit could not land there (the commit-time
naming gate needs the overlay that was restored for the clean check). So that file is a record of the deploy (its deployed_at is the wrapper's own timestamp, read
here), not the source of the trunk edit. The edit is made against THIS tree's manifest. The wrapper writes NO file_checksums, so the existing keys are recomputed from
the release tree's bytes and CROSS-CHECKED against the host's md5 read live over SSM; one disagreement refuses the whole edit. The key set is not widened.
mcportal_commit does not move (the dashboard bundle is the same pin).
usage: python ap31_manifest.py   (run from the repository root of the worktree on box/sitez; no argument)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time

import boto3

ROOT = os.getcwd()
TREE = "C:/tmp/og-rel-batch4"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "d3ae88be463d88c6f4ea22fb297659bf44f43758"          # the ROLLBACK commit that is live (the release b124377b41 was rolled back at once)
TRIED = "b124377b41caf5665b999378fd0ca08ad8a1fb7d"
BASE = "319c9413a20895a63517c5ca1b9ced0f78a5573a"
SEAT = "0.7.0_AE_CloudOps~NFRA1"

wrapper = json.load(io.open(os.path.join(TREE, "infra", "aws", "ec2", "EC2_MANIFEST.json"), encoding="utf-8"))["services"]["opal-gateway"]
head = subprocess.run(["git", "-C", TREE, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
if head != RELEASE or wrapper.get("deployed_commit") != RELEASE:
    raise SystemExit("REFUSED: the release tree's HEAD or its wrapper-written manifest is not the release")
DEPLOYED_AT = wrapper["deployed_at"]

NOTE = (
    "NFRA_OPLGTW OG-ap-32 (round 40): the round-40 release %s was deployed at 2026-10-17T01:53Z over the AMGT_HARVST HVST-cc-7 release 319c9413a2 and ROLLED BACK AT ONCE at 02:02Z "
    "when the host memory trigger fired (87.1 percent during the paging read-back, limit 85; row Z-S338). LIVE NOW: rollback commit %s (branch rel-nfra-oplgtw-batch4-rollback, local, "
    "never merged), deployed %s with DEPLOY_BASE_REF=%s under the stale-base guard (equal at both checkpoints); its content is the release with app/client_adapter_bd49f.py and "
    "app/refs/DATA_CATALOG.yaml at their 4be300110e blobs, so the host runs the pre-deploy content again (host md5 against the 4be300110e blobs: 136 equal, 3 differ = the three "
    "harvest files AMGT_HARVST changed, as before the release). The three harvest files are byte-equal to trunk d2b95c10cf. NO IAM moved, no env key and no tool changed (registry 103, "
    "tools/list 103, .env 65 keys, health 200). The release b124377b41 is NOT live and its paging code did not stay: memory was not returned between pages (52, 58, 65, 73 percent after "
    "pages 1 to 4, peak 87.1). Ledger nfra-oplgtw-gateway-release-batch4. The byte reference of the AMGT_HARVST state is the S3 tarball opal-gateway-319c9413a2.tar.gz "
    "(sha256 6202213c503f). ||| PREVIOUS: " % (TRIED, RELEASE, DEPLOYED_AT, TRIED))

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

svc["previous_deployed_commit"] = TRIED
svc["deployed_commit"] = RELEASE
svc["deployed_at"] = DEPLOYED_AT
svc["deployed_by"] = SEAT
svc["file_checksums"] = {k: release_sums[k] for k in keys}
svc["release_note"] = NOTE + svc["release_note"]
man["_last_updated"] = DEPLOYED_AT
io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(json.dumps(man, indent=2) + "\n")
print("WROTE %s" % MANIFEST)
print("  deployed_commit %s -> %s ; previous %s ; deployed_at %s" % (BASE[:10], RELEASE[:10], svc["previous_deployed_commit"][:10], DEPLOYED_AT))
