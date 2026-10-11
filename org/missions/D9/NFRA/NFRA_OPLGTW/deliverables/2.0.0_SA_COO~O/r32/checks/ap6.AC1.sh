#!/usr/bin/env bash
# OPLGTW OG-ap-6 AC1 (the E2 re-cut, Phase B1): the release named in W/ap6_release.json ({"base_sha", "release_sha"})
# sits on the live gateway ref 2a5966dfbd (MP-r-2's close, COO~MP msg 33064) and carries EXACTLY the hunks of the signed
# release a88661b145 over its base 1e32562729 -- the COO half's re-cut condition:
#   (1) git patch-id --stable of the whole diff, with the one .env printf line set aside, equals the signed release's;
#   (2) the printf line differs from the base's only by E2's one key (ADVI_FEE_STATEMENT_S3_ROOT=%s\n) and its one argument;
#   (3) no path outside E2's set and no .pptx-pair token (rl16.AC1's rule, read on this release).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap6_release.json"
LIVE=2a5966dfbd89be9fe6cc0ef3566831e502b81d42; SBASE=1e32562729495695c6addaed05f047e46090776f; SREL=a88661b1454938aefa93f53b1302515bd35b1692
[ -f "$REC" ] || { echo "ap6_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
base_ok=no; [ "$base" = "$LIVE" ] && base_ok=yes
pid() { git diff "$1" "$2" | grep -vE "^[-+]printf 'MOCK_GRAPH=0" | git patch-id --stable | awk '{print $1}'; }
p_signed=$(pid "$SBASE" "$SREL"); p_recut=$(pid "$base" "$rel")
pf=$(python - "$base" "$rel" <<'EOF'
import subprocess,sys
def pl(ref):
    t=subprocess.run(['git','show',ref+':infra/aws/ec2/opal-gateway/deploy-to-ec2.sh'],capture_output=True).stdout.decode('utf-8')
    return [l for l in t.split('\n') if l.startswith("printf 'MOCK_GRAPH=0")]
b,r=pl(sys.argv[1]),pl(sys.argv[2])
K="ADVI_FEE_STATEMENT_S3_ROOT=%s\\n"; A='"${ADVI_FEE_STATEMENT_S3_ROOT}" '
ok=len(b)==1 and len(r)==1 and r[0].count(K)==1 and r[0].count(A)==1 and r[0].replace(K,'',1).replace(A,'',1)==b[0]
print('yes' if ok else 'no')
EOF
)
pf=$(printf '%s' "$pf" | tr -d '\r')
ALLOW='^infra/aws/ec2/opal-gateway/(app/integrations/advi_billing/.*|app/tools\.py|app/destructive_ops\.py|app/data_entitlement\.py|deploy-to-ec2\.sh|tests/test_advi_site_to_s3(_registration)?\.py|tests/test_og_ab1_carry\.py|tests/test_data_entitlement_family\.py|tests/test_entitlement_admin\.py)$|^infra/aws/terraform/opal-gateway/advi_billing_gateway_iam\.tf$'
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
pptx=$(git grep -c -E 'market_update|ADVI_MARKET_UPDATE_S3_ROOT' "$rel" -- infra/aws/ec2/opal-gateway | awk -F: '{s+=$NF} END {print s+0}')
echo "base ${base:0:10} is the live ref 2a5966dfbd: $base_ok; release ${rel:0:10}"
echo "patch-id (printf set aside) signed=${p_signed:0:12} recut=${p_recut:0:12} equal=$([ -n "$p_signed" ] && [ "$p_signed" = "$p_recut" ] && echo yes || echo no)"
echo "printf differs only by E2's key and argument: $pf"
echo "files differing $n; outside E2's paths $outside (want 0); .pptx-pair tokens in the release gateway tree $pptx (want 0)"
[ "$outside" = 0 ] || printf '%s\n' "$files" | grep -vE "$ALLOW" | sed 's/^/  outside: /'
[ "$base_ok" = yes ] && [ -n "$p_signed" ] && [ "$p_signed" = "$p_recut" ] && [ "$pf" = yes ] && [ "$n" -ge 1 ] && [ "$outside" = 0 ] && [ "$pptx" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
