#!/usr/bin/env bash
# OPLGTW OG-n-1 AC2 (the declaration): the gateway root declares aws_eip.gw + aws_eip_association.gw, and a plan TARGETED
# at exactly those two reports no changes (the applied world equals the declaration). Targeted because the root at HEAD
# also declares NFRA_MCPORTAL resources that are not applied yet (MP-a-1, behind G-HDR); a full plan lists them.
# The root's two required variables come from the environment, never typed here:
#   TF_VAR_mcportal_owner_key_claim, TF_VAR_mcportal_owner_key (the order's placeholders).
. "$(dirname "$0")/_root.sh"
T=infra/aws/terraform/opal-gateway
: "${TF_VAR_mcportal_owner_key_claim:?export TF_VAR_mcportal_owner_key_claim (the order placeholder)}"
: "${TF_VAR_mcportal_owner_key:?export TF_VAR_mcportal_owner_key (the order placeholder)}"
RD='^resource "aws_eip(_association)?" "gw"'
d=$(cat $T/*.tf | grep -cE "$RD")
out=$(cd $T && timeout 110 terraform plan -input=false -lock=false -no-color -detailed-exitcode -target=aws_eip.gw -target=aws_eip_association.gw 2>&1 | tr -d '\r'); rc=$?
line=$(printf '%s\n' "$out" | grep -m1 -E 'No changes|Plan:|Error')
echo "declared eip resources=$d of 2; targeted plan rc=$rc ($line)"
if [ "$d" = 2 ] && [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
