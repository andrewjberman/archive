#!/usr/bin/env bash
# OPLGTW OG-ab-2 AC1 (CTO~Z ruling @4e2f00c9fa): copy_site_file_to_s3 generalised -- three named tests in
# tests/test_og_ab2_pairs.py, offline:
#   (01) exactly TWO admitted (extension, destination) pairs: .xlsx -> the fee_statement root, .pptx -> the market_update
#        root, each root computed from lib/opal_naming.py address() (never typed); any other extension is REFUSED;
#   (02) a .pptx item lands under the market_update root by a conditional put and returns {s3_key, bytes, sha256}; an
#        existing key is REFUSED and nothing is written;
#   (03) deploy-to-ec2.sh writes the market_update root key from one variable computed by address(), and the deploy
#        refuses if it does not end in /bronze/market_update/.
# Plus E2's suites whole (no regression): test_advi_site_to_s3.py, test_advi_site_to_s3_registration.py, test_og_ab1_carry.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_ab2_audit_$$.jsonl"
pytest_named tests/test_og_ab2_pairs.py test_ogab2_ac01 test_ogab2_ac02 test_ogab2_ac03; r=$?
for f in tests/test_advi_site_to_s3.py tests/test_advi_site_to_s3_registration.py tests/test_og_ab1_carry.py; do
  [ -f "$GW/$f" ] || { echo "$f: absent"; r=1; continue; }
  out=$(cd "$GW" && timeout 110 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  echo "$f: pytest rc=$rc; $(printf '%s\n' "$out" | tail -1)"
  [ "$rc" = 0 ] || r=1
done
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
