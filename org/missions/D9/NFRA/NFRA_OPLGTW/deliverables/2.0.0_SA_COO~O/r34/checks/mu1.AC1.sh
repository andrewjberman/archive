#!/usr/bin/env bash
# OPLGTW OG-mu-1 AC1 (round-34 E1, row W49-S3): the .pptx -> market_update pair names its object exactly as the intake
# writer does (data/transcripts/scripts/updates/intake.py: date=<placed date>/deck_<sha256[:16]>.pptx). The same bytes
# on the same date from both writers give ONE key, and the sanitized original name rides in object metadata, never in
# the key. The tests are named in tests/test_og_mu1.py, and E2's .xlsx suites still pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_mu1.py test_ogmu1_ac01 test_ogmu1_ac02 test_ogmu1_ac03; r0=$?
ok=1; [ "$r0" = 0 ] || ok=0
for s in tests/test_advi_site_to_s3.py tests/test_og_ab2_pairs.py; do
  out=$(cd "$GW" && timeout 110 python -m pytest "$s" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  echo "$s: pytest rc=$rc; $(printf '%s\n' "$out" | tail -1)"; [ "$rc" = 0 ] || ok=0
done
restore_audit
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
