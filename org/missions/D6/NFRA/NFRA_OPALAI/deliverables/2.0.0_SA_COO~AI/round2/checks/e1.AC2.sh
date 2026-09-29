#!/usr/bin/env bash
# OA-e-1 AC2 (seam probe against the REAL neighbours): the LIVE host's TENANT_ID (read over SSM, never printed) and the
# LIVE policy store's ACTIVE principal_profiles. With the code at this worktree, asker_scope.resolve_asker_class(tid)
# returns Opal-internal for EVERY active profile's tid (a real asker is never denied by a tenant mismatch) and None for
# a tenant that is not Opal's (the deny-by-default arm). Counts only; no tid, oid or email is printed.
. "$(dirname "$0")/_root.sh"
out=$(timeout 170 python "org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~AI/round2/checks/e1_seam.py" . 2>&1 | tr -d '\r')
printf '%s\n' "$out" | grep -v '^OK$\|^NOT-OK$'
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
