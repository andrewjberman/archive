#!/usr/bin/env bash
# OA-f-7 AC1 (the built behaviour, CTO ruling msg 26343): an asker whose active grant carries NO portal_channels (key
# absent, or an empty list) gets NO portal catalog key -- the query is refused `asker_no_portal_channels` and nothing is
# fetched -- while a grant WITH channels is still served within them. Three NAMED tests in the NEW
# tests/test_asker_nochannels.py must each PASS, and the existing asker suites (test_asker_scope.py,
# test_asker_binding.py, test_portal_grant.py) must still read 0 failed.
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
[ -f "$G/tests/test_asker_nochannels.py" ] || { echo "tests/test_asker_nochannels.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$G" && timeout 110 python -m pytest tests/test_asker_nochannels.py tests/test_asker_scope.py tests/test_asker_binding.py tests/test_portal_grant.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
need="test_grant_without_portal_channels_denied test_grant_with_empty_portal_channels_denied test_grant_with_channels_served"
n=0; p=0; miss=""
for t in $need; do n=$((n+1)); if printf '%s\n' "$out" | grep -qE "^PASSED tests[/\]test_asker_nochannels[.]py::$t( |$)"; then p=$((p+1)); else miss="$miss $t"; fi; done
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
summ=$(printf '%s\n' "$out" | tail -1)
echo "named arms passed $p of $n; failed/errored tests $failed; summary: $summ"
[ -n "$miss" ] && echo "not passed:$miss"
if [ "$p" = "$n" ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
