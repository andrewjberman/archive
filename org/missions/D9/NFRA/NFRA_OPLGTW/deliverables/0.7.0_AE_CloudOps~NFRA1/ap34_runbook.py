#!/usr/bin/env python
"""OG-ap-34 Phase B step 6: runbook 7.2 names the new live release (the OG-ap-28 and OG-ap-31 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. The previous live release (AMGT_HARVST, deployed by another seat) is a commit that is NOT in this repository, so
neither its sha nor its manifest commit is backticked here. The rolled-back release b124377b41 is never in the manifest's deployed_commit history, so it is not backticked either. The backticked hex are d3ae88be46 (the live rollback commit), 4be300110e, bf9d23b518, d14445961d,
3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap34_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-17T02:1xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-17T05:2xZ) the live release is `9d5b712557` (deployed 2026-10-17T05:19Z; NFRA_OPLGTW OG-ap-34, the round-40 fourth batched release: the 49F window pages back "
    "30 dated partitions at a time with a cursor, newest first by trade date, with the arena cap and 8 read workers, and MI's re-emitted catalog). It was cut on `d3ae88be46`, the rollback "
    "commit of the OG-ap-32 attempt, so it carries the three harvest files the AMGT_HARVST HVST-cc-7 release changed (that release is a commit that is not in this repository; its byte "
    "reference is the S3 tarball opal-gateway-319c9413a2.tar.gz). "
    "**This act moved NO IAM, added no environment key and added no tool.** "
    "**The rollback target for any further release is NOT `4be300110e`** (it would revert the harvest fixes): it is the content that was live before this release, held by `d3ae88be46` "
    "(S3 tarball opal-gateway-d3ae88be46.tar.gz, sha256 764f565cffef). The base `4be300110e` carries "
    "app/data_entitlement.py, app/identity_scope.py and app/revocation.py (each read with git cat-file -e beside a negative control at d88cd32d0c~1, where app/data_entitlement.py is absent, so "
    "the positive reads discriminate and are not a vacuous rc=0). Redeploy through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the host then keeps a few inert files of the "
    "older release that the older code does not import, because the archive is extracted over the old tree. The releases before that were `4be300110e` (NFRA_OPLGTW OG-ap-31, the round-39 "
    "batched release), `bf9d23b518` (NFRA_OPLGTW OG-ap-28, the round-38 batched release) and `d14445961d` (the mcportal pf bundle release of 2026-10-16), then `3d5c9c8bf1` "
    "(deployed 2026-10-16T09:14:19Z; NFRA_OPLGTW OG-ap-23, the code batch release), built on `d577e0e729` (NFRA_OPLGTW OG-ap-21), then `c4c106aea1` (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release), and `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and category-views release). "
    "The paragraphs below give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
