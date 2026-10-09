#!/usr/bin/env bash
# MX-d-7 AC2 (FWD-13 DONE WHEN, read against live S3 before release): for model benchmarks, aum-metrics and
# aggregate-aua-timeseries, the as-of discover states (this worktree's code) equals the served artifact's own field,
# read independently by d7_live.py; claim measured. Read-only, Opal AWS only.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
R="$(pwd)"
out=$(cd "$GW" && timeout 110 python "$(native "$H/d7_live.py")" "$(native "$R/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -4
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
