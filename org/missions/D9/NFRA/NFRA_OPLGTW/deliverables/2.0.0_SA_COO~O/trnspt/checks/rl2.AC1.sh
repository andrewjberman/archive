#!/usr/bin/env bash
# OPLGTW OG-rl-2 AC1 (PRD v1.4 release acceptance), against the SERVED gateway: the laptop's four checks (order 103750)
# and the issuer's two page-token negative arms -- 9 conditions. Bearers are read from Secrets Manager into memory and
# never printed; the sender is read from criterion.py and never printed.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
J="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/ROUTE_NAMES.json"
[ -f "$J" ] || { echo "$J absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 200 python "$(native "$H/_lst_arms.py")" "$(native "$J")" 2>&1 | tr -d '\r'); printf '%s\n' "$out"
if [ "$(printf '%s\n' "$out" | tail -1)" = "LIST ARMS 9 of 9" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
