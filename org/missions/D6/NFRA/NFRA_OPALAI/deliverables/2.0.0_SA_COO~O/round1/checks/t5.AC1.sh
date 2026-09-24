#!/usr/bin/env bash
# OA-t-5 AC1 (built): the asker-scope tests pass -- the four named tests, and nothing failed.
#   test_asker_resolved_from_message_sender   tid+oid come from the Teams message the gateway read itself
#   test_unprofiled_asker_refused             no profile -> refusal carrying the how-to-get-access line, no data read
#   test_scope_is_intersection                grant AND identity allowlist: the served scope is narrower than either
#   test_agent_supplied_identity_ignored      an asker field the agent passes changes nothing (same verdict with and without it)
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_asker_scope.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_asker_resolved_from_message_sender test_unprofiled_asker_refused test_scope_is_intersection test_agent_supplied_identity_ignored; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 4; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
