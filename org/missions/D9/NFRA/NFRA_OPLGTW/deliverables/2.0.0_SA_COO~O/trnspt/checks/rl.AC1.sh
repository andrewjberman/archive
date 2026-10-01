#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-rl-1 AC1 (C7: each route's FIRST criterion is a negative arm run on demand), against the SERVED
# gateway: cross-prefix bearers refused both ways; an off-allowlist meeting refused; an off-table sender refused; an
# off-table sender in a table sender's thread refused; a non-PDF attachment returns metadata only. Bearers are read
# from Secrets Manager into memory and never printed. Message ids come from the issuer at run time
# (OG_RL_OFF_TABLE_MSG, OG_RL_THREAD_MSG, OG_RL_NONPDF_MSG, OG_RL_NONPDF_ATT); an arm with no input is NOT RUN = FAIL.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
J="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/ROUTE_NAMES.json"
[ -f "$J" ] || { echo "$J absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python "$(native "$H/_arms.py")" "$(native "$J")" 2>&1 | tr -d '\r'); printf '%s\n' "$out"
if [ "$(printf '%s\n' "$out" | tail -1)" = "ARMS 6 of 6 refused-or-metadata" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
