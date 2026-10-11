#!/usr/bin/env bash
# MX-c-7 AC3 (round-8 analysis E2; FWD-18, FWD-11): FWD-18 reads 3 of 14 from the emitted catalog with C3 carried by
# E-4/E-5/E-9 and C1 no longer claimed by E-25; discover carries no need-local word fold; an unknown model name reaches
# E-13 and the match carries the five served model codes. Instrument c7_tags.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 120 python "$(native "$H/c7_tags.py")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -8
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
