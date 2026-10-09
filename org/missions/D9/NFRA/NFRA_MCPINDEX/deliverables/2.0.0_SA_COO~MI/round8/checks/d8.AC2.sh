#!/usr/bin/env bash
# MX-d-8 AC2 (FWD-17, PRD v0.7 contract 1): discover answers a GAP need with its owner and no tool, and a write-class
# need with its class and whether the CALLER's grant allows it (both arms). Named tests, offline; no other test in the
# discover file fails.
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_opal_discover.py \
  test_gap_need_answers_with_its_owner_and_no_tool \
  test_write_need_states_the_caller_grant_refused \
  test_write_need_states_the_caller_grant_allowed
rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
