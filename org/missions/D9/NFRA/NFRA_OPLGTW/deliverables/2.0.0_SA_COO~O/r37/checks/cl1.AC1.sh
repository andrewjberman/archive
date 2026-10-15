#!/usr/bin/env bash
# OPLGTW OG-cl-1 AC1 (round-37, FWD-22): the named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cl1.py test_ogcl1_ac01 test_ogcl1_ac02 test_ogcl1_ac03 test_ogcl1_ac04 test_ogcl1_ac05 test_ogcl1_ac06 test_ogcl1_ac07 test_ogcl1_ac08 test_ogcl1_ac09 test_ogcl1_ac10 test_ogcl1_ac11 test_ogcl1_ac12; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
