#!/usr/bin/env bash
# OPLGTW OG-gp-1 AC1 (round-37, FWD-22): the named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gp1.py test_oggp1_ac01 test_oggp1_ac02 test_oggp1_ac03 test_oggp1_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
