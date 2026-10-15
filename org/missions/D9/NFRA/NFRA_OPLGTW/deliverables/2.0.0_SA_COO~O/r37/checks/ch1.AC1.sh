#!/usr/bin/env bash
# OPLGTW OG-ch-1 AC1 (round-37 G2-HOOKUP): the named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_ch1.py test_ogch1_ac01 test_ogch1_ac02 test_ogch1_ac03 test_ogch1_ac04 test_ogch1_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
