#!/usr/bin/env bash
# MX-s-1 AC1 (the conversion reaches silver, live): for each of DIVZ and IDVZ, the number of DISTINCT dates under
# opal-data-assets trueshares/<fund>/silver/fact_holdings/ is at least the number of distinct dates under
# trueshares/<fund>/bronze/holdings/ (every delivered date converted), and both are > 0. Read-only listing.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; B=opal-data-assets; ok=0; line=""
for f in DIVZ IDVZ; do
  br=$(timeout 90 "$AWS" s3api list-objects-v2 --bucket $B --prefix "trueshares/$f/bronze/holdings/" --query 'Contents[].Key' --output text 2>/dev/null | tr -d '\r' | tr '\t' '\n' | grep -oE '/[0-9]{8}/' | sort -u | grep -c .)
  sv=$(timeout 90 "$AWS" s3api list-objects-v2 --bucket $B --prefix "trueshares/$f/silver/fact_holdings/" --query 'Contents[].Key' --output text 2>/dev/null | tr -d '\r' | tr '\t' '\n' | grep -oE '[0-9]{4}-?[0-9]{2}-?[0-9]{2}' | tr -d '-' | sort -u | grep -c .)
  line="$line $f: bronze dates=$br silver fact_holdings dates=$sv;"
  [ "$br" -gt 0 ] && [ "$sv" -ge "$br" ] && ok=$((ok+1))
done
echo "live:$line funds converted $ok of 2"
if [ "$ok" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
