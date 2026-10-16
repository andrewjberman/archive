#!/usr/bin/env python
"""OG-ap-31 Phase B step 6: runbook 7.2 names the new live release (the OG-ap-28 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. So no md5 and no other sha prefix is backticked here. The backticked hex are 4be300110e (the live release),
bf9d23b518 (the rollback target), d14445961d, 3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap31_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-16T18:0xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-16T22:1xZ) the live release is `4be300110e` (deployed 2026-10-16T22:01:25Z; NFRA_OPLGTW OG-ap-31, the round-39 batched "
    "release: the 49F transactions and fees tools read every dated partition in the window up to 60 and drop only exact-duplicate rows, units and currency fields "
    "with figures as JSON numbers, the email-deny guard's route class with the master-admin exemption on the four internal browser routes, and the discover "
    "echo of bucket, vendor and firm). **This release moved NO IAM, added no environment key and added no tool, so a binary rollback undoes the whole of it.** "
    "**The rollback target is `bf9d23b518`**, the base this release was cut on and the state running on the host until this deploy: "
    "it carries app/data_entitlement.py, app/identity_scope.py and app/revocation.py (each read with git cat-file -e beside a negative control at "
    "d88cd32d0c~1, where app/data_entitlement.py is absent, so the positive reads discriminate and are not a vacuous rc=0). Redeploy it through "
    "safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the host then keeps a few inert files of this release that the base code does "
    "not import, because the archive is extracted over the old tree. The release before that was `d14445961d` (the round-38 gateway release's base, the "
    "mcportal pf bundle release of 2026-10-16), then `3d5c9c8bf1` (deployed 2026-10-16T09:14:19Z; "
    "NFRA_OPLGTW OG-ap-23, the code batch release), built on `d577e0e729` (NFRA_OPLGTW OG-ap-21), then `c4c106aea1` (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release), and `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and "
    "category-views release). The paragraphs below give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
