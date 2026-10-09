#!/usr/bin/env bash
# MX-c-7 AC2 (FWD-19 routing): the operations lead's 8 phrasings reach E-30..E-35 on the FIRST try in discover,
# offline, against the working tree's catalog (Opal-internal principal). Instrument c7_route.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 120 python "$(native "$H/c7_route.py")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -10
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
