#!/usr/bin/env bash
# OA-g-3 AC1: gateway-access-state-table holds exactly 1 ACTIVE principal_profile whose grant carries zero Schwab masters and a non-empty portal_channels scope (Alyssa Keith's; counts only, no identifier printed), parsed by app/data_entitlement.py at HEAD.
. "$(dirname "$0")/_root.sh"
out=$(timeout 150 python org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~O/round1/checks/g3_scan.py AC1 . 2>&1 | tr -d '\r')
printf '%s\n' "$out" | grep -v '^OK$\|^NOT-OK$'
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
