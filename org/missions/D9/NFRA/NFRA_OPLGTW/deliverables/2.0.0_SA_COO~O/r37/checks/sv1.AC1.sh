#!/usr/bin/env bash
# OPLGTW OG-sv-1 AC1 (round-37, FWD-22, PRD v3.13): the named offline tests of the json-served tool family pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_sv1.py test_ogsv1_ac01 test_ogsv1_ac02 test_ogsv1_ac03 test_ogsv1_ac04 test_ogsv1_ac05 test_ogsv1_ac06; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
