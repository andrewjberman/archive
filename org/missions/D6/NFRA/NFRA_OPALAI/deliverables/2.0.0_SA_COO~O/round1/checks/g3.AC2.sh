#!/usr/bin/env bash
# OA-g-3 AC2: gateway-access-state-table's one portal-only active grant carries operations exactly [query] (portal figures only; no list, describe or download), parsed by app/data_entitlement.py at HEAD. Counts only, no identifier printed.
. "$(dirname "$0")/_root.sh"
out=$(timeout 150 python org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~O/round1/checks/g3_scan.py AC2 . 2>&1 | tr -d '\r')
printf '%s\n' "$out" | grep -v '^OK$\|^NOT-OK$'
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
