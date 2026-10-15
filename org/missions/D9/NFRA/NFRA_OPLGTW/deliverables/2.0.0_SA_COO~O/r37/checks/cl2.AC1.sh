#!/usr/bin/env bash
# OPLGTW OG-cl-2 AC1 (round-37, FWD-22): the named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cl2.py test_ogcl2_ac01 test_ogcl2_ac02 test_ogcl2_ac03 test_ogcl2_ac04 test_ogcl2_ac05 test_ogcl2_ac06 test_ogcl2_ac07 test_ogcl2_ac08; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
