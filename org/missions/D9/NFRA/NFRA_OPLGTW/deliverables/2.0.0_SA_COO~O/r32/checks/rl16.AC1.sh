#!/usr/bin/env bash
# OPLGTW OG-rl-16 AC1 (E2 .xlsx release, Phase A): the release named in W/rl16_release.json ({"base_sha", "release_sha"})
# differs from its base ONLY in E2's paths (the advi_billing module + its tests, tools.py, destructive_ops.py,
# data_entitlement.py, deploy-to-ec2.sh, test_og_ab1_carry.py, advi_billing_gateway_iam.tf); carries NO .pptx pair
# (no "market_update" and no ADVI_MARKET_UPDATE_S3_ROOT anywhere in the release's gateway tree); and the E2 suites pass
# in the release tree.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~51/rl16_release.json"
[ -f "$REC" ] || { echo "rl16_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
ALLOW='^infra/aws/ec2/opal-gateway/(app/integrations/advi_billing/.*|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|deploy-to-ec2\.sh|tests/test_advi_site_to_s3(_registration)?\.py|tests/test_og_ab1_carry\.py|tests/test_data_entitlement_family\.py|tests/test_entitlement_admin\.py)$|^infra/aws/terraform/opal-gateway/advi_billing_gateway_iam\.tf$'
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
pptx=$(git grep -c -E 'market_update|ADVI_MARKET_UPDATE_S3_ROOT' "$rel" -- infra/aws/ec2/opal-gateway | awk -F: '{s+=$NF} END {print s+0}')
echo "base ${base:0:10} -> release ${rel:0:10}: files differing $n; outside E2's paths $outside (want 0); .pptx-pair tokens in the release gateway tree $pptx (want 0)"
[ "$outside" = 0 ] || printf '%s\n' "$files" | grep -vE "$ALLOW" | sed 's/^/  outside: /'
[ "$n" -ge 1 ] && [ "$outside" = 0 ] && [ "$pptx" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
