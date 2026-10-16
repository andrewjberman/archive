#!/usr/bin/env bash
# OPLGTW OG-sv-2 AC1 (round-37, FWD-22, CTO ruling @131991960e): the named offline tests of portal_get_cma_assumptions pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_sv2.py test_ogsv2_ac01 test_ogsv2_ac02 test_ogsv2_ac03 test_ogsv2_ac04; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
