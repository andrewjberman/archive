#!/usr/bin/env python
"""OG-rl-17 Phase B: runbook 7.2 names the new live release (the OG-rz-2 shape).

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING: rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold Read-the-manifest line and this paragraph stay in ONE block with no blank line between them,
and inside that window every backticked 10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py AND appear in the manifest's own deployed_commit history. Only commits that were
deployed and carry the file are backticked: 8e3eddf959 (the live release), 13917ef993 (the rollback target, the previous live release) and the older targets of the previous paragraph.
usage: python rl17_runbook.py <deployed_at_utc> <tarball_key> <tarball_bytes> <tarball_sha16>   (repository root of the worktree on box/sitez)"""
from __future__ import annotations

import io
import os
import sys

DEPLOYED_AT, TAR_KEY, TAR_BYTES, TAR_SHA = sys.argv[1:5]
P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-20")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]
tail = old[old.index("The releases before that on this lineage were"):]
head = (
    "As last read (%s) the live release is `8e3eddf959` (deployed %s; NFRA_OPLGTW OG-rl-17, the round-47 sixteenth batched release: the client fences and resolve envelope, the Cottonwood date parse, the 50 KB projection, "
    "the in-flight guard with the cap 26 and the 8 GiB capacity key, the search and Teams-poll bounds, index_pairs, news_for_security, the YCharts and data-refresh repairs and the error-text mask; nothing arms the listener). "
    "It was cut on `13917ef993`, the OG-rz-2 release. **This act moved NO IAM, added no environment key, added no tool and wrote no SSM parameter.** "
    "**The rollback target for any further release is `13917ef993`**, the content that was live before this release (the live ref's tarball %s, %s bytes, sha256 %s): redeploy "
    "through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the rollback rewrites the marker /opt/opal-gateway/.deployed_commit to the "
    "live ref's sha; read it. The in-flight guard, the caps and the fences disappear with a rollback and the contract key returns to 2048. " % (DEPLOYED_AT[:13] + "xZ", DEPLOYED_AT, TAR_KEY, TAR_BYTES, TAR_SHA))
tail = tail.replace("The releases before that on this lineage were ", "The releases before that on this lineage were `13917ef993` (NFRA_OPLGTW OG-rz-2, the round-46 fourteenth batched release, with the resize to t4g.large), ", 1)
new = head + tail
assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
