#!/usr/bin/env bash
# OA-t-5 AC3 (bound: nothing existing moves): tests/test_identity_scope.py fails ONLY on what already failed at the cut
# (test_scoped_deny_by_default, red at 0070f8a7ef on site Z) and passes at least the 5 it passed there. Measured at the
# cut: 5 passed, 1 failed. A new failure, or fewer passes, is a regression this cell introduced.
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest tests/test_identity_scope.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
passed=$(printf '%s\n' "$out" | grep -cE '::[A-Za-z0-9_]+(\[.*\])? PASSED')
fails=$(printf '%s\n' "$out" | grep -oE '::[A-Za-z0-9_]+(\[.*\])? (FAILED|ERROR)' | sed -E 's/^:://; s/ (FAILED|ERROR)$//' | sort -u | tr '\n' ' ')
new=$(printf '%s\n' $fails | grep -vx 'test_scoped_deny_by_default' | grep -c .)
echo "passed=$passed; failing=[${fails% }]; failures not present at the cut=$new"
if [ "$passed" -ge 5 ] && [ "$new" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
