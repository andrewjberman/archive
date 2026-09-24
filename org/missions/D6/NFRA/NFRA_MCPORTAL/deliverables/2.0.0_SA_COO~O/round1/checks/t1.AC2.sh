#!/usr/bin/env bash
# MP-t-1 AC2 (bound: the existing routes do not move): tests/test_sprint_view.py passes as at the cut (8 passed), and
# tests/test_identity_scope.py fails only on what failed at the cut (test_scoped_deny_by_default) with >= 5 passed.
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
s=$(timeout 100 python -m pytest tests/test_sprint_view.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | tail -1)
sp=$(printf '%s' "$s" | grep -oE '[0-9]+ passed' | awk '{print $1}'); sf=$(printf '%s' "$s" | grep -oE '[0-9]+ (failed|error)' | awk '{print $1}')
o=$(timeout 100 python -m pytest tests/test_identity_scope.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
ip=$(printf '%s\n' "$o" | grep -cE '::[A-Za-z0-9_]+(\[.*\])? PASSED')
new=$(printf '%s\n' "$o" | grep -oE '::[A-Za-z0-9_]+(\[.*\])? (FAILED|ERROR)' | sed -E 's/^:://; s/ (FAILED|ERROR)$//' | grep -vx 'test_scoped_deny_by_default' | grep -c .)
echo "sprint: ${s}; identity_scope passed=$ip, failures not present at the cut=$new"
if [ "${sp:-0}" -ge 8 ] && [ -z "$sf" ] && [ "$ip" -ge 5 ] && [ "$new" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
