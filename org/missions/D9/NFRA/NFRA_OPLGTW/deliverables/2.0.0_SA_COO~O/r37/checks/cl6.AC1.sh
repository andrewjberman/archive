#!/usr/bin/env bash
# OPLGTW OG-cl-6 AC1 (round-37, FWD-22): the named tests pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cl6.py test_ogcl6_ac01 test_ogcl6_ac02 test_ogcl6_ac03 test_ogcl6_ac04 test_ogcl6_ac05 test_ogcl6_ac06 test_ogcl6_ac07; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
