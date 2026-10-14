#!/usr/bin/env bash
# OPLGTW gt3 AC1 (round-37 G1-TYPED, FWD-22): the figures tools' five named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt3.py test_oggt3_ac01 test_oggt3_ac02 test_oggt3_ac03 test_oggt3_ac04 test_oggt3_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
