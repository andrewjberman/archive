#!/usr/bin/env bash
# OA-e-10 AC3 (the CONTROL, the OG-e-2 email-deny guard stays either way): tests/test_email_deny.py passes with 0 failed,
# and its four /sprint routes are still in the denial table it asserts.
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
sp=$(grep -oE '\("GET", "/sprint[^"]*"\)' "$G/tests/test_email_deny.py" | sort -u | grep -c .)
out=$(cd "$G" && timeout 110 python -m pytest tests/test_email_deny.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
summ=$(printf '%s\n' "$out" | tail -1)
passed=$(printf '%s\n' "$summ" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
bad=$(printf '%s\n' "$summ" | grep -cE 'failed|error')
echo "sprint routes asserted=$sp; email-deny suite: $summ"
if [ "$sp" = 4 ] && [ "$passed" -ge 1 ] && [ "$bad" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
