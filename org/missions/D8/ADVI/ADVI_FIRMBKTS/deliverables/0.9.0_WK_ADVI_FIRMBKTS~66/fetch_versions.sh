#!/bin/bash
# FB-h-7 read-only fetch (S3 get-object only): every listed version of the 12 served
# trade-date objects for 2026-08-20..23, written OUTSIDE the checkout.
DATA=/c/dev/wk-firmbkts-66-data
cd "$DATA" || exit 1
while IFS=$'\t' read -r key vid lm loc; do
  if [ -s "$loc" ]; then continue; fi
  timeout 120 aws s3api get-object --bucket opal-data-bd --key "$key" --version-id "$vid" "$loc" </dev/null >/dev/null || echo "FAIL $key $vid"
done < ver_manifest.tsv
echo DONE
