#!/usr/bin/env bash
# OPLGTW gt0 AC1 (round-37 G1-TYPED, FWD-22): the base's five named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt0.py test_oggt0_ac01 test_oggt0_ac02 test_oggt0_ac03 test_oggt0_ac04 test_oggt0_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
