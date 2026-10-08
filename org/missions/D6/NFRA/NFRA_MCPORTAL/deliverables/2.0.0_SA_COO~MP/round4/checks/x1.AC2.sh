#!/usr/bin/env bash
# MP-x-1 AC2 (no regression on the owner-gated admin surface): the six admin/owner suites run with 0 failed and >=1 passed.
. "$(dirname "$0")/_root.sh"
S="tests/test_owner_gate.py tests/test_admin_grants.py tests/test_admin_refusals.py tests/test_admin_round2.py tests/test_admin_tenants.py tests/test_admin_fabric.py"
for s in $S; do [ -f "$GW/$s" ] || { echo "$GW/$s absent"; echo "RESULT: FAIL"; exit 1; }; done
out=$(cd "$GW" && timeout 200 python -m pytest $S -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "admin suites: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
