#!/usr/bin/env python
"""OG-ap-39 Phase B: runbook 7.2 names the new live release (the OG-ap-28 and OG-ap-31 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. The previous live release (AMGT_HARVST, deployed by another seat) is a commit that is NOT in this repository, so
neither its sha nor its manifest commit is backticked here. The rolled-back release b124377b41 is never in the manifest's deployed_commit history, so it is not backticked either. The backticked hex are d3ae88be46 (the live rollback commit), 4be300110e, bf9d23b518, d14445961d,
3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap39_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-17T23:5xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-18T07:3xZ) the live release is `aa2efa2cf3` (deployed 2026-10-18T06:22Z; NFRA_OPLGTW OG-ap-39, the round-42 seventh batched release: the absent_reason notes the client tools serve "
    "in their descriptions, and the client_get_fees note reworded so it no longer claims an unmeasured zero). It was cut on `4257a2aa42`, dell1's AMGT_HARVST HVST-cg-3 release. "
    "**This act moved NO IAM, added no environment key, changed no unit and added no tool.** "
    "**The rollback target for any further release is `4257a2aa42`**, the content that was live before this release (the live ref's tarball opal-gateway-4257a2aa42.tar.gz, sha256 f59e4b4009cf): redeploy "
    "through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the rollback rewrites the marker /opt/opal-gateway/.deployed_commit to the "
    "live ref's sha; read it. The releases before that on this lineage were `d077cef043` (NFRA_OPLGTW OG-ap-38, the round-41 sixth batched release, which put the memory ceiling on the gateway unit), "
    "`efcc8ae19f` (OG-ap-36), `1753c741d9` (dell1's AMGT_HARVST HVST-cd-2 release, landed on this lineage by OG-ap-37) and `9d5b712557` (NFRA_OPLGTW OG-ap-34, the "
    "round-40 fourth batched release), cut on `d3ae88be46` (the OG-ap-32 rollback commit), then `4be300110e` (NFRA_OPLGTW OG-ap-31, the round-39 "
    "batched release), `bf9d23b518` (NFRA_OPLGTW OG-ap-28, the round-38 batched release) and `d14445961d` (the mcportal pf bundle release of 2026-10-16), then `3d5c9c8bf1` "
    "(deployed 2026-10-16T09:14:19Z; NFRA_OPLGTW OG-ap-23, the code batch release), built on `d577e0e729` (NFRA_OPLGTW OG-ap-21), then `c4c106aea1` (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release), and `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and category-views release). "
    "The paragraphs below give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
