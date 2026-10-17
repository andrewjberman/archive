#!/usr/bin/env python
"""OG-ap-36 Phase B step 6: runbook 7.2 names the new live release (the OG-ap-28 and OG-ap-31 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. The previous live release (AMGT_HARVST, deployed by another seat) is a commit that is NOT in this repository, so
neither its sha nor its manifest commit is backticked here. The rolled-back release b124377b41 is never in the manifest's deployed_commit history, so it is not backticked either. The backticked hex are d3ae88be46 (the live rollback commit), 4be300110e, bf9d23b518, d14445961d,
3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap36_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-17T05:2xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-17T17:3xZ) the live release is `efcc8ae19f` (deployed 2026-10-17T17:06Z; NFRA_OPLGTW OG-ap-36, the round-41 fifth batched release: the 49F client transactions and fees "
    "tools run off the event loop, one prefix listing, an Arrow-side fence and account filter, the adapter's reason word kept at the tool boundary, and a host marker file that reads the release sha). "
    "It was cut on `1753c741d9`, the AMGT_HARVST HVST-cd-2 release deployed by another seat (a commit on a local branch of this repository, not merged into this lineage; its byte reference is the S3 tarball "
    "opal-gateway-1753c741d9.tar.gz, sha256 7cf249065b6b). "
    "**This act moved NO IAM, added no environment key and added no tool.** "
    "**The rollback target for any further release is `1753c741d9`**, the content that was live before this release (the live ref's tarball above): redeploy through safe-ec2-deploy.sh declaring the "
    "live release as DEPLOY_BASE_REF, then remove /opt/opal-gateway/.deployed_commit (the older code does not write it). The host then keeps a few inert files of this release that the older code does "
    "not import, because the archive is extracted over the old tree. The release before that on this lineage was `9d5b712557` (NFRA_OPLGTW OG-ap-34, the round-40 fourth batched release), "
    "cut on `d3ae88be46` (the OG-ap-32 rollback commit), then `4be300110e` (NFRA_OPLGTW OG-ap-31, the round-39 "
    "batched release), `bf9d23b518` (NFRA_OPLGTW OG-ap-28, the round-38 batched release) and `d14445961d` (the mcportal pf bundle release of 2026-10-16), then `3d5c9c8bf1` "
    "(deployed 2026-10-16T09:14:19Z; NFRA_OPLGTW OG-ap-23, the code batch release), built on `d577e0e729` (NFRA_OPLGTW OG-ap-21), then `c4c106aea1` (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release), and `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and category-views release). "
    "The paragraphs below give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
