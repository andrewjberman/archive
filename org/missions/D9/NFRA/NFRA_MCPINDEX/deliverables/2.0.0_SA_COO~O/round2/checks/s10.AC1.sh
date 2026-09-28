#!/usr/bin/env bash
# MX-s-10 AC1 (the SERVED SSM document, not the repo copy): the DEFAULT version of opal-bd-asset-dim-download runs the
# MX-s-9 REST pull module and the dim builder, and no longer runs the Playwright portal download
# (download-daily-asset-dim.ts) or reads portal credentials (BD_PASSWORD).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
c=$(timeout 60 "$AWS" ssm get-document --name opal-bd-asset-dim-download --query Content --output text 2>&1 | tr -d '\r')
[ -n "$c" ] || { echo "get-document returned nothing -- RESULT: FAIL"; exit 1; }
rest=$(printf '%s' "$c" | grep -c 'pull_bd_asset_dim_rest')
build=$(printf '%s' "$c" | grep -c 'build_bd_assets_dim')
pw=$(printf '%s' "$c" | grep -c 'download-daily-asset-dim.ts')
pwd_=$(printf '%s' "$c" | grep -c 'BD_PASSWORD')
echo "served document: rest-pull refs=$rest builder refs=$build playwright refs=$pw BD_PASSWORD refs=$pwd_"
if [ "$rest" -ge 1 ] && [ "$build" -ge 1 ] && [ "$pw" = 0 ] && [ "$pwd_" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
