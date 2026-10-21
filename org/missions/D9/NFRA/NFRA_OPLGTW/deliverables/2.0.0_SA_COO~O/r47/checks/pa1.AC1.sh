#!/usr/bin/env bash
# OPLGTW OG-pa-1 AC1 (round 47) -- Menachem's person_access tool narrowing, written by the grant writer on Andrew's owner confirm. PHASE A: the candidate narrowing taken from the deployed registry, and the decide() pre-flight with it applied. See pacheck.py for the exact record fields.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
res=$(timeout 110 python3 -I "$(dirname "$0")/pacheck.py" phaseA "$W" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
