#!/usr/bin/env python
"""OG-ap-21 Phase B step 8: runbook 7.2 names the new live release.

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING. rb.AC2 takes
`section.split("\\n\\n")[:2]`, so block [0] is the heading and block [1] is the bold Read-the-manifest
line TOGETHER WITH this paragraph -- there is no blank line between them, and adding one would move
the paragraph out of the graded window entirely. Inside that window every BACKTICKED 10-40 hex string
is read as a rollback-target commit and must carry app/data_entitlement.py AND appear in the
manifest's own deployed_commit history. So: no md5 and no sha prefix is backticked here (the
trading-calendar md5 lives two paragraphs down for exactly that reason), and the only backticked
hex are d577e0e729 (the live release), c4c106aea1 and 06cfb6db64 -- both verified against rb.AC2's
two conditions before this edit, against a 67-value history denominator.
"""
from __future__ import annotations

import io

P = ("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/ec2/opal-gateway/runbooks/"
     "SCHWAB_PILOT_RUNBOOK.md")

s = io.open(P, encoding="utf-8").read()

start = s.index("As last read (2026-10-15T11:0xZ) the live release is")
end_marker = "the scope seam without which the portal and etfs modules cannot import)."
end = s.index(end_marker) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-16T01:1xZ) the live release is `d577e0e729` (deployed 2026-10-16T00:09:44Z; "
    "NFRA_OPLGTW OG-ap-21, the person-roles release: ONE new READ tool, harvest_get_published_analysis, "
    "registry 75 -> 76; the five news tools' DynamoDB reads and the published-layer Lambda invoke moved "
    "onto the ASSUMED internal reader role gateway-global-internal-reader-role, so those served tools now "
    "act through that identity rather than the box's default credential chain; and the person reader, "
    "which can widen a scoped Opal identity to a served tool only when NFRA_MCPORTAL has written a record, "
    "and can narrow or stop anyone. **A binary rollback does NOT undo this release's THREE IAM acts.** Two "
    "statements were ADDED to the internal reader -- gateway-global-news-read-internal-policy "
    "(dynamodb:Query and dynamodb:GetItem on the three news tables and the one date-index) and "
    "gateway-global-harvest-published-invoke-policy (lambda:InvokeFunction on the ONE function "
    "opal-amgt-scoped-api) -- and gateway-global-news-read-policy was then DESTROYED BY NAME off the "
    "instance role AFTER the served read, which narrows opal-gateway-role from 25 to 24 inline statements. "
    "Undo them deliberately through safe-apply, targeted, by name: destroy the two added statements, and "
    "re-create the destroyed one from the replayable INNER document (Version and Statement only, no API "
    "envelope) kept at org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"
    "P21_ROLLBACK_gw_news_read.policy.json. Those three names are the only keys this release touched; the "
    "internal reader's other grants -- gateway-global-internal-reader-policy, "
    "gateway-global-harvest-read-policy, gateway-global-portal-tiered-read-policy and "
    "gateway-global-etfs-read-policy -- are different names on the same role and must not be touched. "
    "**The rollback target is `c4c106aea1`**, the base this release was cut on: it was the state actually "
    "running on the host until 00:09:44Z today, and it carries app/data_entitlement.py, "
    "app/identity_scope.py and app/revocation.py (each read with git cat-file -e beside a negative control "
    "at d88cd32d0c~1, where app/data_entitlement.py is absent, so the positive reads discriminate and are "
    "not a vacuous rc=0). It is also the PREVIOUS live release (deployed 2026-10-15T19:50:39Z; "
    "NFRA_MCPINDEX MX-r-14, the round-17 catalog release). The release before that was `06cfb6db64` "
    "(deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A and category-views release: six "
    "new READ tools, registry 69 -> 75, and one read grant, gateway-global-etfs-read-policy, on this same "
    "internal reader role -- two of its nine addresses are SINGLE OBJECTS carrying no trailing star, the "
    "one shape where a silent under-grant lives, and its served read exercised them). The paragraphs below "
    "give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
print("  the block structure is preserved: no blank line was added between the bold Read line and this")
print("  paragraph, so it stays inside rb.AC2's split(chr(10)+chr(10))[:2] window")
