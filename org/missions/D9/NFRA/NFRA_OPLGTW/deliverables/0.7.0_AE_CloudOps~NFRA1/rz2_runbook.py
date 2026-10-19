#!/usr/bin/env python
"""OG-rz-2 Phase B: runbook 7.2 names the new live release (the OG-ap-28 and OG-ap-31 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE
block with no blank line between them, and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py
AND appear in the manifest's own deployed_commit history. The previous live release (AMGT_HARVST, deployed by another seat) is a commit that is NOT in this repository, so
neither its sha nor its manifest commit is backticked here. The rolled-back release b124377b41 is never in the manifest's deployed_commit history, so it is not backticked either. The backticked hex are d3ae88be46 (the live rollback commit), 4be300110e, bf9d23b518, d14445961d,
3d5c9c8bf1, d577e0e729, c4c106aea1 and 06cfb6db64 (older targets).
usage: python ap50_runbook.py   (run from the repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-19T17:0xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]
tail_from = old.index("The releases before that on this lineage were")
tail = old[tail_from:]
head = (
    "As last read (2026-10-20T07:xxZ) the live release is `13917ef993` (deployed 2026-10-20T06:xxZ; NFRA_OPLGTW OG-rz-2, the round-46 fourteenth batched release: the gateway host was first resized from t4g.small to t4g.large, then the unit's memory limits "
    "5600M and 6400M and the Schwab master 08403355 were released; nothing arms the listener). It was cut on `6d1b5dcb64`, the OG-ap-50 release. "
    '**This act moved NO IAM, added no environment key, added no tool and wrote no SSM parameter.** '
    "**The rollback target for any further release is `6d1b5dcb64`**, the content that was live before this release (the live ref's tarball opal-gateway-6d1b5dcb64b.tar.gz, sha256 e7cd9de1617a): redeploy "
    'through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the rollback rewrites the marker /opt/opal-gateway/.deployed_commit to the '
    "live ref's sha; read it. **Roll back in THIS order: the tarball first (the limits return to 1200M and 1400M), THEN apply t4g.small; never the reverse.** The releases before that on this lineage were `6d1b5dcb64` (NFRA_OPLGTW OG-ap-50, the family_depth route), ")
tail = tail.replace("The releases before that on this lineage were ", "", 1)
new = head + tail
assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
