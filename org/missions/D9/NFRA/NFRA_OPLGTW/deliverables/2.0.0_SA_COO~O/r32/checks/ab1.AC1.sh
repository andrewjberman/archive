#!/usr/bin/env bash
# OPLGTW OG-ab-1 AC1 (dell2 ADVI_BILLING packet E2, CTO~Z ruling msg 32663, row ADVI_BILLING-D2-W7-S1): the required carry.
# Three named tests in tests/test_og_ab1_carry.py, offline:
#   (01) DESTRUCTIVE_OPS["copy_site_file_to_s3"] is WRITE_REVERSIBLE, blast_dimensions ["files:1"], and
#        TOOL_WRITE_CLASS["copy_site_file_to_s3"] == "write_files" (the class upload_text_to_site carries);
#   (02) "copy_site_file_to_s3" is in data_entitlement.NATIVE_TOOLS;
#   (03) deploy-to-ec2.sh's .env printf writes ADVI_FEE_STATEMENT_S3_ROOT from one variable, and its value computed by
#        lib/opal_naming.py address() ends in /bronze/fee_statement/.
# Plus the packet's own two test files whole: tests/test_advi_site_to_s3.py, tests/test_advi_site_to_s3_registration.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_ab1_audit_$$.jsonl"
pytest_named tests/test_og_ab1_carry.py test_ogab1_ac01 test_ogab1_ac02 test_ogab1_ac03; r1=$?
for f in tests/test_advi_site_to_s3.py tests/test_advi_site_to_s3_registration.py; do
  [ -f "$GW/$f" ] || { echo "$f: absent"; r1=1; continue; }
  out=$(cd "$GW" && timeout 110 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  echo "$f: pytest rc=$rc; $(printf '%s\n' "$out" | tail -1)"
  [ "$rc" = 0 ] || r1=1
done
restore_audit; rm -f "$AUDIT_PATH"
[ "$r1" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
