#!/usr/bin/env bash
# MX-d-7 AC3 (no regression): the routing harness over the 27 real asks routes at least 24 to the expected tool (the
# round-7 floor), so reading freshness from the artifact changed no route.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 110 python tests/routing/run_routing.py 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -E '^ROUTING: ' | tail -1)
n=$(printf '%s' "$line" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\).*/\1/p'); d=$(printf '%s' "$line" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\).*/\2/p')
echo "${line:-ROUTING: no summary line (rc=$rc)}; floor 24 of 27"
if [ -n "$n" ] && [ "$d" = 27 ] && [ "$n" -ge 24 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
