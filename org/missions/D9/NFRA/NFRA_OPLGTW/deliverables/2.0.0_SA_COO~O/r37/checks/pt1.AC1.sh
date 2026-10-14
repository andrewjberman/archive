#!/usr/bin/env bash
# OPLGTW OG-pt-1 AC1 (round-37 FWD22-W5, FWD-22 G3): the four portal model/market tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_pt1.py test_ogpt1_ac01 test_ogpt1_ac02 test_ogpt1_ac03 test_ogpt1_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
