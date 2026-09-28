#!/usr/bin/env bash
# OA-e-1 AC1 (the built behaviour): the three negative arms and the positive arm, as NAMED tests in
# tests/test_asker_binding.py, each PASSED; and the existing tests/test_asker_scope.py still passes (0 failed).
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
[ -f "$G/tests/test_asker_binding.py" ] || { echo "tests/test_asker_binding.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$G" && timeout 110 python -m pytest tests/test_asker_binding.py tests/test_asker_scope.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
need="test_old_message_from_wider_person_refused test_reply_to_other_chat_refused test_group_chat_unprofiled_member_refused test_same_chat_recent_message_served"
n=0; p=0; miss=""
for t in $need; do n=$((n+1)); if printf '%s\n' "$out" | grep -qE "^PASSED tests[/\]test_asker_binding[.]py::$t( |$)"; then p=$((p+1)); else miss="$miss $t"; fi; done
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
summ=$(printf '%s\n' "$out" | tail -1)
echo "named arms passed $p of $n; failed/errored tests $failed; summary: $summ"
[ -n "$miss" ] && echo "not passed:$miss"
if [ "$p" = "$n" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
