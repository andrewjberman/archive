#!/usr/bin/env bash
# MX-s-11 AC3 (what the instance fetches is what HEAD holds): the four files the asset-dim document stages from
# opal-data-bd are published byte-identical to their HEAD blobs.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
t=$(mktemp -d); n=0; ok=0
while read -r repo key; do
  n=$((n+1)); b="$t/$n"
  timeout 60 "$AWS" s3 cp "s3://opal-data-bd/$key" "$(native "$b")" >/dev/null 2>&1
  h1=$(git show "HEAD:$repo" 2>&1 | sha256sum | cut -c1-64)
  if [ -f "$b" ] && [ "$(sha256sum < "$b" | cut -c1-64)" = "$h1" ]; then ok=$((ok+1)); else echo "  MISMATCH or absent: $key"; fi
done <<'EOF'
data/black_diamond/scripts/bronze/pull_bd_asset_dim_rest.py code/bronze/pull_bd_asset_dim_rest.py
data/black_diamond/scripts/bronze/_asset_dim_rest_pin.py code/bronze/_asset_dim_rest_pin.py
lib/silver_ids.py code/lib/silver_ids.py
lib/trading_calendar.py code/lib/trading_calendar.py
EOF
echo "published byte-identical to HEAD: $ok of $n"
if [ "$ok" = 4 ] && [ "$n" = 4 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
