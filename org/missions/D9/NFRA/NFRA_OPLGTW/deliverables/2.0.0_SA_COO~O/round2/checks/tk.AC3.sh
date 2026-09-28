#!/usr/bin/env bash
# OPLGTW OG-t-1 AC3 (regression control): the moto-free suites around tier, guard, owner gate and deny still pass.
# Base value 47 passed (measured 2026-09-28 by the drafting fork). moto modules are excluded: moto is not installed.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
out=$(cd "$GW" && timeout 100 python -m pytest tests/test_attachment_tools.py tests/test_min_tier_gate.py tests/test_ratelimit.py \
  tests/test_owner_gate.py tests/test_email_deny.py tests/test_identity_scope.py tests/test_sprint_view.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | tail -1)
rm -f "$AUDIT_PATH"; restore_audit
echo "$out"
n=$(printf '%s' "$out" | sed -nE 's/^([0-9]+) passed.*/\1/p')
if [ -n "$n" ] && [ "$n" -ge 47 ] && ! printf '%s' "$out" | grep -Eq 'failed|error'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
