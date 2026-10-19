#!/usr/bin/env bash
# OPLGTW OG-en-32 AC1 (round 44; row Z-S391): the five route-test cases that fail at the base (each expects a 405 and receives a 404) pass together.
# The five node ids are fixed here, from the row: a case dropped or renamed to make the count pass is a failure of THIS check, not a pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
IDS="tests/test_transcript_route.py::test_bearer_constant_time_own_prefix_only tests/test_teams_route.py::test_methods_and_unknown_routes tests/test_teams_route.py::test_new_routes_are_get_only_and_allowlist_still_refuses_neighbours tests/test_mail_route.py::test_transcript_and_ms_bearers_refused_on_mail_prefix tests/test_mail_route.py::test_graph_get_only_fails_closed"
out=$(cd "$GW" && timeout 110 python -m pytest -q -p no:cacheprovider --color=no $IDS 2>&1 | tr -d '\r'); rc=$?
last=$(printf '%s\n' "$out" | tail -1)
p=$(printf '%s\n' "$last" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); f=$(printf '%s\n' "$last" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
restore_audit
echo "the five named route-test cases: passed ${p:-0} of 5; failed ${f:-0}; pytest rc=$rc"
[ "$rc" = 0 ] && [ "${p:-0}" = 5 ] && [ "${f:-0}" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
