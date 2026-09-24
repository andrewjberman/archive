#!/usr/bin/env bash
# OA-t-4 AC1 (built): the watch's lineage tests pass -- the three named tests, and nothing failed.
#   test_refresh_on_expiry                  an expired access token triggers ONE refresh_token grant and the new token is used
#   test_never_reads_claude_credentials     no code path opens ~/.claude/.credentials.json (the open is trapped in the test)
#   test_refresh_family_in_state_dir        the rotated refresh token is persisted under the configured state dir only
. "$(dirname "$0")/_root.sh"
F="opal_ai/opal/agent/teams_watch/test_teams_watch_lineage.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_refresh_on_expiry test_never_reads_claude_credentials test_refresh_family_in_state_dir; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 3; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
