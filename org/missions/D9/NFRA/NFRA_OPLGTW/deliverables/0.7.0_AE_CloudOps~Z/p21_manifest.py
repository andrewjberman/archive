#!/usr/bin/env python
"""OG-ap-21 Phase B step 8: land the EC2 manifest's standing clauses on the SHARED tree.

WHY THIS IS NOT A COPY OF THE WRAPPER'S COMMIT: safe-ec2-deploy committed its manifest edit inside
the release worktree, whose manifest baseline is OLDER than trunk's -- it still read
deployed_commit=daa56d81ac, because the base c4c106aea1 was itself a release whose manifest commit
also stayed on its own branch. Copying that commit onto trunk would roll the field backwards through
a value that was never live here. So the edit is made against the SHARED tree's own content, and the
wrapper's 4-line commit is treated as a record of the deploy, not as the source of the trunk edit.

AND THE WRAPPER DID NOT WRITE file_checksums AT ALL: its diff is 4 lines (_last_updated,
deployed_commit, deployed_at, deployed_by) and 0 checksum lines. The order asks for checksums from
the release blobs, so they are recomputed here from the release worktree's own bytes and then
CROSS-CHECKED against the host's md5 read live over SSM. Either source alone would be a producer
self-report; the pair is the control. A single disagreement refuses the whole edit.

The key SET is not widened: exactly the 10 keys the manifest already carries are recomputed. Adding
keys here would be a taxonomy change riding a release, which is not this act.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time

import boto3

ROOT = r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace"
TREE = r"C:\tmp\og-rel-p21"
MANIFEST = os.path.join(ROOT, "infra", "aws", "ec2", "EC2_MANIFEST.json")
SRC = os.path.join(TREE, "infra", "aws", "ec2", "opal-gateway")
INSTANCE = "i-07dccb1615503ac99"
RELEASE = "d577e0e7297b3ecba183023d8374855a93f148a7"
BASE = "c4c106aea1cc47d15f81397208226bd9b292c9dc"
DEPLOYED_AT = "2026-10-16T00:09:44Z"      # the wrapper's own timestamp, not a fresh clock
SEAT = "0.7.0_AE_CloudOps~Z"

NOTE = (
    "NFRA_OPLGTW OG-ap-21 (round 37, workstream PERSON-ROLES, FWD-22; the person-roles release): "
    "release commit %s (branch rel-nfra-oplgtw-p21, local, never merged; 20 files vs %s -- 8 gateway "
    "app modules, deploy-to-ec2.sh, both copies of NFRA_OPLGTW_CONTRACT.json, 7 test files and the two "
    "IAM .tf files) deployed %s with DEPLOY_BASE_REF=%s; the stale-base guard read the live ref EQUAL at "
    "both checkpoints (early and immediately-before-upload, from s3-metadata git-ref on "
    "opal-gateway-latest). Carries: tools 75 -> 76 (+harvest_get_published_analysis, 0 removed, read "
    "from app.tools.mcp._tool_manager.list_tools() on the host); the news DynamoDB reads and the "
    "published-layer Lambda invoke moved onto the ASSUMED internal reader role, so the served tools act "
    "through gateway-global-internal-reader-role rather than the box's default credential chain; and the "
    "person reader (access_state/data_entitlement), which can widen a scoped Opal identity to a served "
    "tool only when NFRA_MCPORTAL writes a record, and can narrow or stop anyone. Row Z-S153 ruling: "
    "this release KEEPS the base entitlement guard (W67-S1 stays open as its own cell). IAM, three acts "
    "each applied ALONE through safe-apply and each read back from live IAM, graded by diffing two full "
    "captures of BOTH roles: +gateway-global-news-read-internal-policy (dynamodb:Query+GetItem, 3 tables "
    "and the date-index) and +gateway-global-harvest-published-invoke-policy (lambda:InvokeFunction on "
    "the ONE function opal-amgt-scoped-api) on the internal reader, then -gateway-global-news-read-policy "
    "destroyed BY NAME off the instance role AFTER the served read, which narrows that role 25 -> 24 "
    "inline statements with the other 24 byte-identical by canonical sha. The new news document and the "
    "one it replaced share canonical sha256 09b69a98ccd4ba8c -- not a byte wider. The invoke grant was "
    "ABSENT on BOTH roles before the act, so it is a NEW grant and not a move (A2). Read-back: 123 of "
    "123 host files md5 == the release blobs across app, deploy and lib (SSM, not an S3 ETag); the six "
    "tools served to an Opal stand-in through an assumed identity reading "
    "gateway-global-internal-reader-role/ap21-identity-probe beside an instance identity of "
    "opal-gateway-role/%s, a non-Opal refused through BOTH seams (typed_opal_only for four, "
    "harvest_opal_only for news_for_security and the published-analysis tool) with 0 DynamoDB reads AND "
    "0 Lambda invokes, three person-reader arms green against a stub store that wrote no record, and the "
    "same read re-run WHOLE after the destroy with every value unchanged. Ledger "
    "nfra-oplgtw-gateway-release-p21. Halves: CTO @378438988e, COO @c9c5cb0e07, CVO @bee4c81023, all "
    "pinned to %s against ask sha 862a1de9a7c6. Rollback: redeploy the base %s with "
    "DEPLOY_BASE_REF=%s, destroy the two new internal-reader statements, and re-create "
    "gateway-global-news-read-policy from the replayable inner document at "
    "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/P21_ROLLBACK_gw_news_read.policy.json. "
    "Open: ap21.AC2's contract_staging_test_green clause, row NFRA_OPLGTW-Z-S156. ||| PREVIOUS: "
    % (RELEASE, BASE[:10], DEPLOYED_AT, BASE, INSTANCE, RELEASE[:10], BASE[:10], RELEASE))

# ---- refuse to edit a manifest somebody else is mid-edit on --------------------------------
dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--",
                        "infra/aws/ec2/EC2_MANIFEST.json"],
                       capture_output=True).stdout.decode().strip()
if dirty:
    raise SystemExit("REFUSED: the shared manifest is already modified (%r) -- a peer may be mid-edit" % dirty)

man = json.load(io.open(MANIFEST, encoding="utf-8"))
svc = man["services"]["opal-gateway"]
if svc["deployed_commit"] != BASE:
    raise SystemExit("REFUSED: trunk's deployed_commit is %s, not the base %s this release was cut on"
                     % (svc["deployed_commit"], BASE))

keys = sorted(svc["file_checksums"])
print("file_checksums key set (unchanged, %d keys): %s" % (len(keys), keys))


def local_md5(rel):
    p = os.path.join(TREE, rel) if rel.startswith("lib/") else os.path.join(SRC, rel)
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


release_sums = {k: local_md5(k) for k in keys}

# ---- the control: the HOST's own md5 of the same 10 paths, read live ------------------------
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
    raise SystemExit("REFUSED: the host md5 control did not run (%s): %s"
                     % (inv["Status"], inv.get("StandardErrorContent", "")[:300]))
host = {}
for line in inv["StandardOutputContent"].splitlines():
    line = line.strip()
    if " " in line:
        h, p = line.split(None, 1)
        host[p.strip()] = h

bad = [(k, release_sums[k], host.get(k)) for k in keys if host.get(k) != release_sums[k]]
print("host control: %d of %d paths read, %d disagree" % (len(host), len(keys), len(bad)))
if bad:
    for k, r, h in bad:
        print("  DISAGREE %-44s release=%s host=%s" % (k, r, h))
    raise SystemExit("REFUSED: the release blobs and the host disagree -- the manifest is not written")

changed = {k: (svc["file_checksums"][k], release_sums[k]) for k in keys
           if svc["file_checksums"][k] != release_sums[k]}
print("checksums that MOVE with this release: %d of %d" % (len(changed), len(keys)))
for k, (o, n) in sorted(changed.items()):
    print("  %-44s %s -> %s" % (k, o, n))

svc["previous_deployed_commit"] = svc["deployed_commit"]
svc["deployed_commit"] = RELEASE
svc["deployed_at"] = DEPLOYED_AT
svc["deployed_by"] = SEAT
svc["file_checksums"] = {k: release_sums[k] for k in keys}
svc["release_note"] = NOTE + svc["release_note"]
man["_last_updated"] = DEPLOYED_AT

io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(json.dumps(man, indent=2) + "\n")
print("WROTE %s" % MANIFEST)
print("  deployed_commit          %s -> %s" % (BASE[:10], RELEASE[:10]))
print("  previous_deployed_commit %s" % svc["previous_deployed_commit"][:10])
print("  release_note             %d bytes (was %d)" % (len(svc["release_note"]), len(svc["release_note"]) - len(NOTE)))
