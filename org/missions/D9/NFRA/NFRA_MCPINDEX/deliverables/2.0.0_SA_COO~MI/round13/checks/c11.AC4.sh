#!/usr/bin/env bash
# MX-c-11 AC4 -- discover surfaces what the table rows now carry: the retired flag and reason, no tool target for a retired row,
# and the row's nl_tags reach it. Three named tests in the gateway's discover test file, each on a fixture row (not the live catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
if pytest_named tests/test_opal_discover.py test_harvest_retired_flag_in_answer test_harvest_retired_row_is_not_a_tool_target test_harvest_nl_tags_reach_the_row; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
