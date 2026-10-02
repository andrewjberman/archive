#!/usr/bin/env bash
# OPLGTW OG-au-1 AC1 (row Z-W15-S23, analysis round 12 s.3a): the three named tests in
# infra/aws/ec2/opal-gateway/tests/test_audit_bytes_principal.py pass on this tree.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r13_au_audit_$$.jsonl"
pytest_named tests/test_audit_bytes_principal.py test_ogau1_ac01 test_ogau1_ac02 test_ogau1_ac03; rc=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
