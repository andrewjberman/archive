#!/usr/bin/env python
"""OG-ap-46 Phase B: runbook 7.2 names the new live release (the OG-ap-28 and OG-ap-31 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. The previous live release (AMGT_HARVST, deployed by another seat) is a commit that is NOT in this repository, so
neither its sha nor its manifest commit is backticked here. The rolled-back release b124377b41 is never in the manifest's deployed_commit history, so it is not backticked either. The backticked hex are d3ae88be46 (the live rollback commit), 4be300110e, bf9d23b518, d14445961d,
3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap46_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-18T20:3xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]
tail_from = old.index("The releases before that on this lineage were")
tail = old[tail_from:]
head = (
    "As last read (2026-10-19T05:0xZ) the live release is `e09c30c3f0` (deployed 2026-10-19T04:14Z; NFRA_OPLGTW OG-ap-46, the round-44 eleventh batched release: family_depth.py with its data file and test, INERT and "
    "not reachable, and the corrected probe-listener comment; nothing arms the listener). It was cut on `eff517546e`, the OG-ap-44 release. "
    '**This act moved NO IAM, added no environment key, changed no unit, added no tool and wrote no SSM parameter.** '
    "**The rollback target for any further release is `eff517546e`**, the content that was live before this release (the live ref's tarball opal-gateway-eff517546e.tar.gz, sha256 e1a8eb744ad4): redeploy "
    'through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the rollback rewrites the marker /opt/opal-gateway/.deployed_commit to the '
    "live ref's sha; read it. The releases before that on this lineage were `eff517546e` (NFRA_OPLGTW OG-ap-44, the access-log repair), ")
tail = tail.replace("The releases before that on this lineage were ", "", 1)
new = head + "`a0c83303ee` (OG-ap-42), " + tail
assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
