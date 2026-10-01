#!/usr/bin/env bash
# OPLGTW OG-pr-1 AC2 (CTO ruling R3 acceptance, APPLIED): iam simulate-principal-policy on opal-gateway-role reads
# `allowed` for GetSecretValue on the three granted secrets' live ARNs and `implicitDeny` on a sibling gateway/* secret
# ARN that is not granted (the negative arm).
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
T=$(mktemp -d); arns=""
for n in gateway/transcripts/bearer gateway/mail/bearer gateway/principals/rosters; do
  a=$(aws secretsmanager describe-secret --secret-id "$n" --region us-east-1 --query ARN --output text | tr -d '\r')
  echo "describe $n -> ${a:-ABSENT}"; arns="$arns $a"
done
sib="arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/notgranted/probe-AbCdEf"
role=$(aws iam get-role --role-name opal-gateway-role --query Role.Arn --output text | tr -d '\r')
# shellcheck disable=SC2086
aws iam simulate-principal-policy --policy-source-arn "$role" --action-names secretsmanager:GetSecretValue \
  --resource-arns $arns "$sib" --output json > "$T/sim.json"; echo "simulate rc=$?"
timeout 60 python "$(native "$H/_pr.py")" simulate "$(native "$T/sim.json")" 2>&1 | tr -d '\r'; r=$?
rm -rf "$T"; exit $r
