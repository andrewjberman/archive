#!/usr/bin/env bash
# MX-c-8 AC3 (FWD-21 routing, offline): this worktree's discover answers the two harvest subjects with harvest_datasets
# matches, and the Schwab control keeps its three silver datasets with no harvest match. Instrument c10_discover.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 120 python "$(native "$H/c10_discover.py")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
