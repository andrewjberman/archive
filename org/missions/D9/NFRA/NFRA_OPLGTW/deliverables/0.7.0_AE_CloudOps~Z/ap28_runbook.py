#!/usr/bin/env python
"""OG-ap-28 Phase B step 6: runbook 7.2 names the new live release.

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING (see ap23_runbook.py): rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold
Read-the-manifest line and this paragraph must stay in ONE block with no blank line between them, and inside that window every backticked
10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py AND appear in the manifest's own
deployed_commit history. So no md5 and no other sha prefix is backticked here. The backticked hex are bf9d23b518 (the live release),
d14445961d (the rollback target), 3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets), each verified against rb.AC2 after the
manifest edit.

usage: python ap28_runbook.py        (run from the repository root)
"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-16T09:2xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-16T18:0xZ) the live release is `bf9d23b518` (deployed 2026-10-16T17:57:06Z; NFRA_OPLGTW OG-ap-28, the round-38 batched "
    "release: units and currency fields on client position rows, the news coverage floor, the chatter lag in trading days, the Muse client narrowing "
    "INERT, a no-row key answering 404, a 429 audit row, the four 49F Black Diamond live tools read from opal-data-bd through their own role, and the "
    "mcportal pin). **This release moved NO IAM and added no tool, so a binary rollback undoes the whole of it.** The seventh reader key "
    "(BLACKDIAMOND49FLIVE_READER_ROLE_ARN) is written by the deploy script and disappears with a rollback; the role it names and its grant are "
    "OG-ap-29 and stay. **The rollback target is `d14445961d`**, the base this release was cut on and the state running on the host until this deploy: "
    "it carries app/data_entitlement.py, app/identity_scope.py and app/revocation.py (each read with git cat-file -e beside a negative control at "
    "d88cd32d0c~1, where app/data_entitlement.py is absent, so the positive reads discriminate and are not a vacuous rc=0). Redeploy it through "
    "safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the host then keeps a few inert files of this release that the base code does "
    "not import, because the archive is extracted over the old tree. The release before that was `3d5c9c8bf1` (deployed 2026-10-16T09:14:19Z; "
    "NFRA_OPLGTW OG-ap-23, the code batch release), built on `d577e0e729` (NFRA_OPLGTW OG-ap-21), then `c4c106aea1` (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release), and `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and "
    "category-views release). The paragraphs below give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
print("  no blank line was added between the bold Read line and this paragraph")
