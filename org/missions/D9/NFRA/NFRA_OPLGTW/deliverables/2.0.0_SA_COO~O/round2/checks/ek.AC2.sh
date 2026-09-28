#!/usr/bin/env bash
# OPLGTW OG-e-1 AC2: the moto-free regression modules stay green -- 24 passed at base (measured 2026-09-27 13:41Z),
# 24 or more after (the cell may add tests to them). AUDIT_PATH isolated as in AC1.
R="$(git rev-parse --show-toplevel)"; cd "$R/infra/aws/ec2/opal-gateway" || exit 9
export AUDIT_PATH="$(mktemp)"
out=$(timeout 300 python -m pytest tests/test_owner_gate.py tests/test_portal_grant.py tests/test_sprint_view.py tests/test_asker_scope.py -q -p no:cacheprovider --color=no 2>&1 | tail -1)
rm -f "$AUDIT_PATH"
echo "$out"
n=$(printf '%s' "$out" | sed -n 's/^\([0-9][0-9]*\) passed.*/\1/p')
if [ -n "$n" ] && [ "$n" -ge 24 ] && ! printf '%s' "$out" | grep -Eq 'failed|error'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
