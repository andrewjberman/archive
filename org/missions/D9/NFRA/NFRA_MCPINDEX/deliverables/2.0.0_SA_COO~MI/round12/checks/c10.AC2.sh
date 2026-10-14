#!/usr/bin/env bash
# MX-c-10 AC2 (per-table routing): every research table is reached FIRST by each of its own example questions, plus
# two issuer anchors. Instrument c12_route.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 300 python "$(native "$H/c12_route.py")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | grep -E '^(ROUTE|ANCHOR|ROUTING)|Error|Traceback' | cut -c1-200 | tail -20
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
