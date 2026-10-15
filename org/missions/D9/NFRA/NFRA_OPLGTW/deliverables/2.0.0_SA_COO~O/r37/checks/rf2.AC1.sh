#!/usr/bin/env bash
# OPLGTW OG-rf-2 AC1 (round-37 RIVAL-FUNDS, FWD-22 G5r): the rival tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_rf2.py test_ogrf2_ac01 test_ogrf2_ac02 test_ogrf2_ac03 test_ogrf2_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
