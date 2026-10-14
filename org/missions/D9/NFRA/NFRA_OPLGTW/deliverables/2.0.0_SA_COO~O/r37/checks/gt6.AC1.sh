#!/usr/bin/env bash
# OPLGTW OG-gt-6 AC1 (round-37 G1-TYPED, FWD-22): the scope seam's four named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt6.py test_oggt6_ac01 test_oggt6_ac02 test_oggt6_ac03 test_oggt6_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
