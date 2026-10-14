#!/usr/bin/env bash
# OPLGTW OG-pt-2 AC1 (round-37 FWD22-W5, FWD-22 G3): the four macro/valuation/scanner/freshness tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_pt2.py test_ogpt2_ac01 test_ogpt2_ac02 test_ogpt2_ac03 test_ogpt2_ac04 test_ogpt2_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
