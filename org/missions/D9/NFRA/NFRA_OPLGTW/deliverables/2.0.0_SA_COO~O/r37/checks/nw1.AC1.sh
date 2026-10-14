#!/usr/bin/env bash
# OPLGTW OG-nw-1 AC1 (round-37 FWD22-W6, FWD-22 G6): the five news tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_nw1.py test_ognw1_ac01 test_ognw1_ac02 test_ognw1_ac03 test_ognw1_ac04 test_ognw1_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
