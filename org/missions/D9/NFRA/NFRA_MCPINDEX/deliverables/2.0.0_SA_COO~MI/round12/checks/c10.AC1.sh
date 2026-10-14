#!/usr/bin/env bash
# MX-c-10 AC1 (FWD-20 depth, EVERY (a) tool): each tool's depth claim is valid under v0.10's cases, the measured ones
# AGREE with the aws CLI's read of the served object, and no `absent` sits on an artifact that carries a date.
# Denominator printed (N of N). Instrument c12_depth.py catalog.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(native "$(pwd)/.tools/aws.cmd")"
out=$(timeout 900 python "$(native "$H/c12_depth.py")" catalog "$(native "$(pwd)/$GW")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" "$AWS" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | grep -E '^(TOOL|DEPTH)|Error|Traceback' | cut -c1-230 | tail -16
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
