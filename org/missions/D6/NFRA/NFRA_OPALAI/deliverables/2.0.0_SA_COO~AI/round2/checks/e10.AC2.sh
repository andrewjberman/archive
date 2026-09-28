#!/usr/bin/env bash
# OA-e-10 AC2 (the built behaviour, on the census's branch): tests/test_login_retire.py passes, and the test named for the
# census's BRANCH PASSED -- test_login_removed (REMOVE: /login answers 404 and a legacy-state /callback is refused) or
# test_login_narrowed (NARROW: /login refuses an identity outside the named server identities).
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~16/E10_LOGIN_CENSUS.md"
G=infra/aws/ec2/opal-gateway
br=$(git show "HEAD:$F" 2>&1 | tr -d '\r' | grep -m1 -oE '^BRANCH: (REMOVE|NARROW)' | awk '{print $2}')
[ -n "$br" ] || { echo "no BRANCH in a committed census"; echo "RESULT: FAIL"; exit 1; }
want=test_login_removed; [ "$br" = NARROW ] && want=test_login_narrowed
[ -f "$G/tests/test_login_retire.py" ] || { echo "tests/test_login_retire.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$G" && timeout 110 python -m pytest tests/test_login_retire.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
named=$(printf '%s\n' "$out" | grep -cE "^PASSED tests/test_login_retire.py::$want( |$)")
failed=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "branch=$br named=$want passed=$named failed/errored=$failed; summary: $(printf '%s\n' "$out" | tail -1)"
if [ "$named" -ge 1 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
