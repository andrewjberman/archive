#!/usr/bin/env bash
# MP-pd-5 AC1 (U2, the script; decomposition PD.4): .tools/tests/test_claude_usage_statusline.py passes with 0 failed and each
# named test PASSES:
#   test_measured_payload_writes_snapshot_with_remaining           rate_limits five_hour/seven_day -> snapshot claim measured, remaining = 100 - used
#   test_payload_without_rate_limits_writes_absent_with_reason     no member -> claim absent with a reason, five_hour and seven_day null
#   test_absent_never_replaces_measured_snapshot                   a measured snapshot survives a later absent payload, byte for byte
#   test_never_opens_credentials_file                              the credentials file is never opened (an open of it fails the test)
#   test_bad_stdin_prints_nothing_exits_zero_and_keeps_previous_file   unparseable stdin -> no stdout, exit 0, previous file untouched
#   test_atomic_write_leaves_no_partial_file                       a failure between temp write and replace leaves no partial snapshot
#   test_account_fields_only_named_keys                            the account object holds exactly email, plan, organization and no other oauthAccount key
. "$(dirname "$0")/_root.sh"
named_pytest_in "statusline tests" "." .tools/tests/test_claude_usage_statusline.py \
  test_measured_payload_writes_snapshot_with_remaining test_payload_without_rate_limits_writes_absent_with_reason \
  test_absent_never_replaces_measured_snapshot test_never_opens_credentials_file \
  test_bad_stdin_prints_nothing_exits_zero_and_keeps_previous_file test_atomic_write_leaves_no_partial_file \
  test_account_fields_only_named_keys
