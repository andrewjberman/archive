#!/usr/bin/env bash
# MX-x-6 AC2 (rows Z-S88 / Z-W28-S8, round-8 analysis E3): the gateway suite's failing-ID baseline is recorded per tree
# shape, and the drain grades a suite run by ID delta, never by count. `suite_delta.py --self-test` replays the
# recorded baseline (0 new) and a planted extra failing ID (1 new, named), and prints the baseline sizes.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
S="$GW/tests/suite_delta.py"
[ -f "$S" ] || { echo "$S absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 60 python "$S" --self-test 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ] && printf '%s\n' "$out" | grep -q '^SELF-TEST PASS'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
