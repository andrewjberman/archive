#!/usr/bin/env bash
# OPLGTW OG-gv-1 AC2 (round 47) -- Andrew's Schwab grant moves to the master-wide scope. PHASE B: the LIVE policy partitions (strong reads) hold the master-wide grant, nothing else changed, decide() against the deployed tree at the batch17 release admits the four read tools, and a served read as the principal answers. See grantcheck.py for the exact record fields.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
res=$(timeout 110 python3 -I "$(dirname "$0")/grantcheck.py" phaseB andrew "$W" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
