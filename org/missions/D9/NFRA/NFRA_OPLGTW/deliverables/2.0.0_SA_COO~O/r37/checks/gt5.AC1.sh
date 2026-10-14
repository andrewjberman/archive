#!/usr/bin/env bash
# OPLGTW gt5 AC1 (round-37 G1-TYPED, FWD-22): the published-analysis tool's four named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt5.py test_oggt5_ac01 test_oggt5_ac02 test_oggt5_ac03 test_oggt5_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
