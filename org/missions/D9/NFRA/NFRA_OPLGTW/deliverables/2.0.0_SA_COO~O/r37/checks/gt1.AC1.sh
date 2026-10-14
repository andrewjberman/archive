#!/usr/bin/env bash
# OPLGTW gt1 AC1 (round-37 G1-TYPED, FWD-22): the identity tools' four named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt1.py test_oggt1_ac01 test_oggt1_ac02 test_oggt1_ac03 test_oggt1_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
