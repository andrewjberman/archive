#!/usr/bin/env bash
# OPLGTW OG-lk-1 AC1 (round-27 ruling R43, row Z-W28-S26): no audit-lake object gets a key with an empty time part.
# Three named tests in tests/test_audit_lake_key_stamp.py, offline: (01) a record that reaches the lake writer with a
# missing or empty time field is written under a key whose time part is non-empty and well-formed; (02) a record with
# a time field gets the same key shape as before this cell (`audit/dt=<day>/<ts>-<id>.jsonl`, the day taken from the
# same time); (03) NEGATIVE CONTROL: the key builder as it stood before this cell, given the record of test 01, yields
# a key with an empty time part (so the test can see the defect it claims is fixed).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r28_lk1_audit_$$.jsonl"
pytest_named tests/test_audit_lake_key_stamp.py test_oglk1_ac01 test_oglk1_ac02 test_oglk1_ac03; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
