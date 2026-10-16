#!/usr/bin/env bash
# OPLGTW OG-ap-25 AC2 (round-37 CLASS-INCREMENT, PHASE B): the ledger nfra-oplgtw-grants-ap25 is CLOSED with its sentinel gone, and the grant is LIVE in IAM, RE-READ here:
# the gateway role holds the policy named in W/CLS_APPLIED.json, whose document allows exactly dynamodb:GetItem on the etf-classifications table ARN; the simulator allows GetItem on it and denies Scan (negative control).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap25; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/CLS_APPLIED.json" ] || { echo "CLS_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r pol arn <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('policy_name',''),d.get('table_arn',''))" "$(native "$W/CLS_APPLIED.json")" | tr -d '\r')"
role=opal-gateway-role
doc=$(aws iam get-role-policy --role-name "$role" --policy-name "$pol" --query PolicyDocument --output json 2>/dev/null | tr -d '\r')
shape=$(printf '%s' "$doc" | python -c "
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print('unreadable'); sys.exit()
st=d.get('Statement'); st=[st] if isinstance(st,dict) else (st or [])
acts=sorted({a for s in st for a in ([s.get('Action')] if isinstance(s.get('Action'),str) else (s.get('Action') or []))})
res=sorted({r for s in st for r in ([s.get('Resource')] if isinstance(s.get('Resource'),str) else (s.get('Resource') or []))})
print('ok' if len(st)==1 and acts==['dynamodb:GetItem'] and res==[sys.argv[1]] and all(s.get('Effect')=='Allow' for s in st) else 'wrong')
" "$arn" | tr -d '\r')
sim() { aws iam simulate-principal-policy --policy-source-arn "$(aws iam get-role --role-name $role --query Role.Arn --output text | tr -d '\r')" --action-names "$1" --resource-arns "$arn" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
g=$(sim dynamodb:GetItem); s=$(sim dynamodb:Scan)
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; policy $pol shape $shape; simulate GetItem $g, Scan (negative control) $s"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$shape" = ok ] && [ "$g" = allowed ] && [ "$s" != allowed ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
