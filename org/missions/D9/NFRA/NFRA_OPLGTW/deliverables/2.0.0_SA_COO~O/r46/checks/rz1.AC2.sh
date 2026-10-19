#!/usr/bin/env bash
# OPLGTW OG-rz-1 AC2: tests/test_og_un1.py passes against the new unit (run from the gateway folder of the worktree).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "ERROR: gateway folder absent"; exit 9; }
out=$(python3 -I -m pytest tests/test_og_un1.py -q -p no:cacheprovider 2>&1 | tr -d '\r'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+'); failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | tail -1 | grep -oE '[0-9]+')
mm=$(grep -E "^MemoryMax=" deploy/opal-gateway.service | tr -d '')
echo "unit ${mm:-MemoryMax absent}; test_og_un1: ${passed:-0} passed, ${failed:-0} failed"
[ "$mm" = "MemoryMax=6400M" ] && [ "$rc" = 0 ] && [ -n "$passed" ] && [ "${failed:-0}" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
