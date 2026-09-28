#!/usr/bin/env bash
# OPLGTW OG-u-1 AC2 (regression control): the rate limiter's and the tier/attachment suites still pass. Base 14 passed.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
out=$(cd "$GW" && timeout 100 python -m pytest tests/test_ratelimit.py tests/test_min_tier_gate.py tests/test_attachment_tools.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | tail -1)
rm -f "$AUDIT_PATH"; restore_audit
echo "$out"; n=$(printf '%s' "$out" | sed -nE 's/^([0-9]+) passed.*/\1/p')
if [ -n "$n" ] && [ "$n" -ge 14 ] && ! printf '%s' "$out" | grep -Eq 'failed|error'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
