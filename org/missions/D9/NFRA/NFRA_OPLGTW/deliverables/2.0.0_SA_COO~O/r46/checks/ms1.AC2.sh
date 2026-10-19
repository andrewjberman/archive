#!/usr/bin/env bash
# OPLGTW OG-ms-1 AC2: the new tests and the six neighbouring files pass, except the one carried red (test_ogz1_ac08, a route-set
# pin that already fails at the live ref). Run from the gateway folder of the WORKER worktree.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "ERROR: gateway folder absent"; exit 9; }
[ -f tests/test_og_ms1.py ] || { echo "named test files: 0 passed, failed names [tests/test_og_ms1.py absent] (allowed: test_ogz1_ac08 only)"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 280 python3 -I -m pytest tests/test_og_ms1.py tests/test_grant_calendar_months.py tests/test_data_entitlement_guard.py tests/test_data_entitlement_family.py tests/test_entitlement_admin.py tests/test_og_cl1.py tests/test_schwab_query.py -q -rf --color=no -p no:cacheprovider 2>&1 | tr -d '\r')
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+')
failed=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED [^:]*::([A-Za-z0-9_]+).*/\1/' | sort -u | paste -sd, -)
ms=$(timeout 100 python3 -I -m pytest tests/test_og_ms1.py -q --color=no -p no:cacheprovider 2>&1 | tr -d '\r')
mp=$(printf '%s\n' "$ms" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+'); mf=$(printf '%s\n' "$ms" | grep -oE '[0-9]+ failed' | tail -1 | grep -oE '[0-9]+')
echo "named test files: ${passed:-0} passed, failed names [${failed}] (allowed: test_ogz1_ac08 only)"
echo "test_og_ms1: ${mp:-0} passed, ${mf:-0} failed"
if [ -n "$passed" ] && { [ -z "$failed" ] || [ "$failed" = "test_ogz1_ac08" ]; } && [ -n "$mp" ] && [ "${mf:-0}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
