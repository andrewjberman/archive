#!/usr/bin/env bash
# OPLGTW OG-ap-27 AC2 (round-37, PHASE B): ledger nfra-oplgtw-grants-ap27 CLOSED with its sentinel gone; the two policies named in W/GAP_APPLIED.json are live on the
# internal reader role, RE-READ from IAM; the simulator allows GetObject on one probe key under each of the four stems, allows ListBucket with each stem as s3:prefix,
# and does NOT allow GetObject on an out-of-scope key of each bucket (negative control) nor ListBucket with an out-of-scope prefix.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap27; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/GAP_APPLIED.json" ] || { echo "GAP_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
IR=gateway-global-internal-reader-role
irarn=$(aws iam get-role --role-name "$IR" --query Role.Arn --output text | tr -d '\r')
pols=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(' '.join(d.get('policy_names',[])))" "$(native "$W/GAP_APPLIED.json")" | tr -d '\r')
held=0; for p in $pols; do aws iam get-role-policy --role-name "$IR" --policy-name "$p" --query PolicyName --output text 2>/dev/null | tr -d '\r' | grep -qx "$p" && held=$((held+1)); done
np=$(printf '%s\n' $pols | grep -c .)
simobj() { aws iam simulate-principal-policy --policy-source-arn "$irarn" --action-names s3:GetObject --resource-arns "$1" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
simlist() { aws iam simulate-principal-policy --policy-source-arn "$irarn" --action-names s3:ListBucket --resource-arns "arn:aws:s3:::$1" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$2,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
ok_o=0; ok_l=0
for k in bbg/probe snapshots/probe mdpf/etfs/gold/new_securities/probe; do [ "$(simobj arn:aws:s3:::opal-data-etfs/$k)" = allowed ] && ok_o=$((ok_o+1)); done
[ "$(simobj arn:aws:s3:::opal-data-mdpf/mdpf/feeds/model_composition/probe)" = allowed ] && ok_o=$((ok_o+1))
for k in bbg/ snapshots/ mdpf/etfs/gold/new_securities/; do [ "$(simlist opal-data-etfs "$k")" = allowed ] && ok_l=$((ok_l+1)); done
[ "$(simlist opal-data-mdpf mdpf/feeds/model_composition/)" = allowed ] && ok_l=$((ok_l+1))
neg_o=0; neg_l=0
[ "$(simobj arn:aws:s3:::opal-data-etfs/ap27-negative-control/probe)" != allowed ] && neg_o=$((neg_o+1))
[ "$(simobj arn:aws:s3:::opal-data-mdpf/ap27-negative-control/probe)" != allowed ] && neg_o=$((neg_o+1))
[ "$(simlist opal-data-etfs ap27-negative-control/)" != allowed ] && neg_l=$((neg_l+1))
[ "$(simlist opal-data-mdpf ap27-negative-control/)" != allowed ] && neg_l=$((neg_l+1))
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; policies named $np, held on the internal reader $held; simulate GetObject allowed $ok_o of 4, ListBucket allowed $ok_l of 4; negative control GetObject not allowed $neg_o of 2, ListBucket not allowed $neg_l of 2"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$np" = 2 ] && [ "$held" = 2 ] && [ "$ok_o" = 4 ] && [ "$ok_l" = 4 ] && [ "$neg_o" = 2 ] && [ "$neg_l" = 2 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
