#!/usr/bin/env python
"""OG-ap-23 Phase B step 6: runbook 7.2 names the new live release.

THE GRADED WINDOW IS NARROW AND ITS SHAPE IS LOAD-BEARING (see p21_runbook.py): rb.AC2 takes `section.split("\\n\\n")[:2]`, so the bold
Read-the-manifest line and this paragraph must stay in ONE block with no blank line between them, and inside that window every backticked
10-40 hex string is read as a rollback-target commit that must carry app/data_entitlement.py AND appear in the manifest's own
deployed_commit history. So no md5 and no other sha prefix is backticked here; the only backticked hex are 3d5c9c8bf1 (the live release),
d577e0e729 (the rollback target and previous live release), c4c106aea1 and 06cfb6db64 (older targets that the paragraph below gives),
each verified against rb.AC2 after the manifest edit.

usage: python ap23_runbook.py        (run from the repository root)
"""
from __future__ import annotations

import io
import os

P = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway", "runbooks", "SCHWAB_PILOT_RUNBOOK.md")
s = io.open(P, encoding="utf-8").read()
start = s.index("As last read (2026-10-16T01:1xZ) the live release is")
end_marker = "The paragraphs below give the older targets and their provenance."
end = s.index(end_marker, start) + len(end_marker)
old = s[start:end]

new = (
    "As last read (2026-10-16T09:2xZ) the live release is `3d5c9c8bf1` (deployed 2026-10-16T09:14:19Z; NFRA_OPLGTW OG-ap-23, the code "
    "batch release: 27 added READ tools, registry 76 -> 103; the five client_* tools are the data-grant, tier-admitted class and so "
    "master_admin only; app/data_entitlement.py now carries OG-bd-3, so a profiled master_admin is admitted to the six tier-admitted tools "
    "whatever its profile's state; the six vendor reader role ARNs are written into the rebuilt .env; and the roster and registry copy "
    "are staged into app/refs at bundle time). **This release moved NO IAM, so a binary rollback undoes the whole of it.** The grants "
    "its tools read through are separate acts that stay when the binary is rolled back: the classification table read on the internal "
    "reader role (OG-ap-26) and the four etfs and mdpf prefixes (OG-ap-27); the six vendor read roles were applied earlier (OG-ap-24). "
    "**The rollback target is `d577e0e729`**, the base this release was cut on and the state running on the host from 2026-10-16T00:09:44Z "
    "until this deploy: it carries app/data_entitlement.py, app/identity_scope.py and app/revocation.py (each read with git cat-file -e "
    "beside a negative control at d88cd32d0c~1, where app/data_entitlement.py is absent, so the positive reads discriminate and are not a "
    "vacuous rc=0). Redeploy it through safe-ec2-deploy.sh declaring the live release as DEPLOY_BASE_REF; the host then keeps a few inert "
    "files of this release (the new modules, lib/opal_naming.py, app/refs) that the base code does not import, because the archive is "
    "extracted over the old tree. The release before that was `c4c106aea1` (deployed 2026-10-15T19:50:39Z; NFRA_MCPINDEX MX-r-14, the "
    "round-17 catalog release), and the one before that `06cfb6db64` (deployed 2026-10-15T10:49:37Z; NFRA_OPLGTW OG-ap-20, the G5 wave A "
    "and category-views release, with one read grant, gateway-global-etfs-read-policy, on the internal reader role). The paragraphs below "
    "give the older targets and their provenance.")

assert old != new
io.open(P, "w", encoding="utf-8", newline="\n").write(s[:start] + new + s[end:])
print("REPLACED runbook 7.2's graded paragraph: %d bytes -> %d bytes" % (len(old), len(new)))
print("  no blank line was added between the bold Read line and this paragraph")
