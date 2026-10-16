#!/usr/bin/env bash
# OPLGTW OG-ch-1 AC2 (round-37 G2-HOOKUP): the worker's probe, RE-RUN here, registers every adapter on the head in one process and asserts the Black Diamond split,
# the distinct firm role keys and the roster name map. The probe prints booleans only.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~111"
P="$W/probe_ch1.py"
[ -f "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 115 python "$P" 2>&1 | tr -d '\r'); rc=$?
echo "$out" | grep -E "^probe ch1:" | tail -n 3
leak=$(printf '%s\n' "$out" | grep -cE '[0-9]{8,}')
echo "probe rc $rc; digit runs of 8 or more in the output $leak (want 0)"
printf '%s\n' "$out" | grep -qE "^probe ch1: adapters_registered_equals_files True; bd_split True; role_keys_distinct True; roster_names_mapped True" && [ "$rc" = 0 ] && [ "$leak" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
