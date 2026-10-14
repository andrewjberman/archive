#!/usr/bin/env bash
# MX-c-9 AC3 (FWD-20 depth): every (a) depth claim is valid; each MEASURED depth equals its served artifact's field as
# read by the aws CLI (second instrument); mdpf_get_aggregate_aua is measured; this worktree's discover answers the AUA
# row's own example question with that depth read at answer time. Instrument c11_depth.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
AWS="$(native "$(pwd)/.tools/aws.cmd")"; [ -f "$(pwd)/.tools/aws.cmd" ] || AWS="$(pwd)/.tools/aws"
out=$(timeout 400 python "$(native "$H/c11_depth.py")" "$(native "$(pwd)/$GW")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" "$AWS" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | grep -E '^(DEPTH|PART1|PART2)|Error|Traceback' | tail -20
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
