#!/usr/bin/env bash
# OPLGTW OG-rv-1 AC1 (round-37 RIVAL-FUNDS, FWD-22 G5r): the rival tools' named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_rv1.py test_ogrv1_ac01 test_ogrv1_ac02 test_ogrv1_ac03 test_ogrv1_ac04 test_ogrv1_ac05; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
