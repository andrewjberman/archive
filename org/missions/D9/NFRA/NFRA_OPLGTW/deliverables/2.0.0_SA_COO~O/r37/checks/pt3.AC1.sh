#!/usr/bin/env bash
# OPLGTW OG-pt-3 AC1 (round-37 FWD22-W5, FWD-22 G3): the firm-scoped tool's named tests pass, including the two-firm negative arm.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_pt3.py test_ogpt3_ac01 test_ogpt3_ac02 test_ogpt3_ac03 test_ogpt3_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
