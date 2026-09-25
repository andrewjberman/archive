#!/usr/bin/env bash
# MX-v-6 AC2 (E4, the harness scores, and its control fires): `python infra/aws/ec2/opal-gateway/tests/routing/run_routing.py`
# runs offline over the question set and ends with `ROUTING: <k> of <n> routed to the expected tool`; the same run with
# `--plant-mislabel` (one question's expected tool swapped) reports exactly one fewer hit over the same n. Both exit 0.
. "$(dirname "$0")/_root.sh"
H="$GW/tests/routing/run_routing.py"
[ -f "$H" ] || { echo "$H absent"; echo "RESULT: FAIL"; exit 1; }
a=$(timeout 110 python "$H" 2>&1 | tr -d '\r'); ra=$?
b=$(timeout 110 python "$H" --plant-mislabel 2>&1 | tr -d '\r'); rb=$?
ka=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\) .*/\1/p' | tail -1); na=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: [0-9]* of \([0-9]*\) .*/\1/p' | tail -1)
kb=$(printf '%s\n' "$b" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\) .*/\1/p' | tail -1); nb=$(printf '%s\n' "$b" | sed -n 's/^ROUTING: [0-9]* of \([0-9]*\) .*/\1/p' | tail -1)
echo "plain run rc=$ra ROUTING ${ka:-?} of ${na:-?}; planted-mislabel run rc=$rb ROUTING ${kb:-?} of ${nb:-?}"
if [ "$ra" = 0 ] && [ "$rb" = 0 ] && [ -n "$ka" ] && [ -n "$kb" ] && [ "$na" = "$nb" ] && [ "$na" -ge 20 ] && [ "$kb" = $((ka - 1)) ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
