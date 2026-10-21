#!/usr/bin/env bash
# OPLGTW OG-gm-2 AC1 (round 47) -- Menachem's Schwab grant, master-wide over the three masters. PHASE A: the candidate record, the diff, the decide() pre-flight on the master-wide parser, the email_deny finding and the three-half ask. See grantcheck.py for the exact record fields.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
res=$(timeout 110 python3 -I "$(dirname "$0")/grantcheck.py" phaseA menachem2 "$W" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
