#!/usr/bin/env bash
# OPLGTW OG-ac-2 AC1 (round-37, the etf-classifications increment): the named offline tests of mdpf_get_security_classification pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_ac2.py test_ogac2_ac01 test_ogac2_ac02 test_ogac2_ac03 test_ogac2_ac04 test_ogac2_ac05 test_ogac2_ac06; r0=$?
restore_audit
[ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
