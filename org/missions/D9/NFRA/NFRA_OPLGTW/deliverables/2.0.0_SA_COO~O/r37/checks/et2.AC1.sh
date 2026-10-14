#!/usr/bin/env bash
# OPLGTW OG-et-2 AC1 (round-37 FWD22-W7, FWD-22 G5 wave A): the fund tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_et2.py test_oget2_ac01 test_oget2_ac02 test_oget2_ac03 test_oget2_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
