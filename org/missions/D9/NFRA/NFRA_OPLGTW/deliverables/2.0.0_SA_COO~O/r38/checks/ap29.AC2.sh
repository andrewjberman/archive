#!/usr/bin/env bash
# OPLGTW OG-ap-29 AC2 (round 38, PHASE B): ledger nfra-oplgtw-grants-ap29 CLOSED with its sentinel gone; the role named in W/BDLIVE_APPLIED.json exists, RE-READ from IAM:
#  - its trust names ONLY the Gateway instance role (one principal, equal to opal-gateway-role's ARN);
#  - the simulator allows s3:GetObject on a probe key under each of the four silver tables of opal-data-bd and s3:ListBucket with each table prefix as the s3:prefix value;
#  - it does NOT allow s3:GetObject on an out-of-scope key of opal-data-bd, nor on a key of opal-data-assets, nor s3:PutObject on an allowed prefix, nor s3:ListBucket with an out-of-scope prefix (negative controls).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap29; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/BDLIVE_APPLIED.json" ] || { echo "BDLIVE_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
role=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('role_name',''))" "$(native "$W/BDLIVE_APPLIED.json")" | tr -d '\r')
[ -n "$role" ] || { echo "role_name absent"; echo "RESULT: FAIL"; exit 1; }
rarn=$(aws iam get-role --role-name "$role" --query Role.Arn --output text 2>/dev/null | tr -d '\r')
gwarn=$(aws iam get-role --role-name opal-gateway-role --query Role.Arn --output text 2>/dev/null | tr -d '\r')
trust=$(aws iam get-role --role-name "$role" --query Role.AssumeRolePolicyDocument --output json 2>/dev/null | python -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: print('unreadable'); sys.exit()
st=d.get('Statement'); st=[st] if isinstance(st,dict) else (st or [])
pr=set()
for s in st:
    p=(s.get('Principal') or {}).get('AWS')
    for x in ([p] if isinstance(p,str) else (p or [])): pr.add(x)
print(','.join(sorted(pr)))" | tr -d '\r')
trust_ok=0; [ -n "$gwarn" ] && [ "$trust" = "$gwarn" ] && trust_ok=1
simobj() { aws iam simulate-principal-policy --policy-source-arn "$rarn" --action-names "$2" --resource-arns "$1" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
simlist() { aws iam simulate-principal-policy --policy-source-arn "$rarn" --action-names s3:ListBucket --resource-arns "arn:aws:s3:::$1" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$2,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
ok_o=0; ok_l=0; neg=0
for t in unrealized transactions allocations fees; do
  [ "$(simobj arn:aws:s3:::opal-data-bd/silver/$t/probe s3:GetObject)" = allowed ] && ok_o=$((ok_o+1))
  [ "$(simlist opal-data-bd "silver/$t/")" = allowed ] && ok_l=$((ok_l+1))
done
[ "$(simobj arn:aws:s3:::opal-data-bd/silver/ap29-negative-control/probe s3:GetObject)" != allowed ] && neg=$((neg+1))
[ "$(simobj arn:aws:s3:::opal-data-assets/blackdiamond/49f/silver/dim_account_xref/probe s3:GetObject)" != allowed ] && neg=$((neg+1))
[ "$(simobj arn:aws:s3:::opal-data-bd/silver/fees/probe s3:PutObject)" != allowed ] && neg=$((neg+1))
[ "$(simlist opal-data-bd ap29-negative-control/)" != allowed ] && neg=$((neg+1))
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; role exists $([ -n "$rarn" ] && echo yes || echo no); trust is only the instance role $trust_ok (1 = yes); simulate GetObject allowed $ok_o of 4, ListBucket allowed $ok_l of 4; negative controls not allowed $neg of 4"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ -n "$rarn" ] && [ "$trust_ok" = 1 ] && [ "$ok_o" = 4 ] && [ "$ok_l" = 4 ] && [ "$neg" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
