#!/bin/bash
# BP-a-3 read-only fetch (S3 list-object-versions and get-object only). Writes OUTSIDE the checkout.
# 1. version listings of silver/prices/, silver/transactions/ and the canonical object
#    (skipped when GAP_NOLIST=1, so a later pass reads the same listing as the first)
# 2. manifest of the versions the measurement reads (gap_manifest.py)
# 3. get-object --version-id for every manifest row not already present
export OPAL_AGENT_SERIAL=0.9.0_WK_ADVI_BDPRCE~3
REPO=/c/dev/wk-bdprce-r1-3
DATA=/c/dev/wk-bdprce-r1-3-data
DEL=$REPO/org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~3
AWS=$REPO/.tools/aws
mkdir -p "$DATA/v"
cd "$DATA" || exit 1
if [ -z "$GAP_NOLIST" ]; then
  timeout 120 "$AWS" s3api list-object-versions --bucket opal-data-bd --prefix silver/prices/ --query 'Versions[].[Key,VersionId,LastModified,IsLatest,Size]' --output text </dev/null > versions_silver_prices_.txt || echo "FAIL list prices"
  timeout 120 "$AWS" s3api list-object-versions --bucket opal-data-bd --prefix silver/transactions/ --query 'Versions[].[Key,VersionId,LastModified,IsLatest,Size]' --output text </dev/null > versions_silver_transactions_.txt || echo "FAIL list transactions"
  timeout 120 "$AWS" s3api list-object-versions --bucket opal-data-bd --prefix silver/prices/canonical_prices.parquet --query 'Versions[].[Key,VersionId,LastModified,IsLatest,Size]' --output text </dev/null > versions_canonical.txt || echo "FAIL list canonical"
fi
python -I "$DEL/gap_manifest.py" || { echo "FAIL manifest"; exit 1; }
while IFS=$'\t' read -r kind key vid lm latest loc; do
  if [ -s "v/$loc" ]; then continue; fi
  timeout 300 "$AWS" s3api get-object --bucket opal-data-bd --key "$key" --version-id "$vid" "v/$loc" </dev/null >/dev/null || echo "FAIL $key $vid"
done < manifest.tsv
echo DONE
