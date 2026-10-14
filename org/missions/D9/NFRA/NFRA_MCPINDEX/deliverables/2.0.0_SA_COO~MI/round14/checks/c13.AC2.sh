#!/usr/bin/env bash
# MX-c-13 AC2 -- discover answers what a silver TABLE row carries: its fork_keys and contract, its plain-word tags, and the
# fail-closed rule for a firm-scoped table. Three named tests in the gateway's discover test file, each on a fixture (not the live catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
if pytest_named tests/test_opal_discover.py test_silver_table_row_answer_carries_fork_keys_and_contract test_silver_table_row_nl_tags_reach_the_row test_silver_firm_scoped_table_row_is_fail_closed_for_firms; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
