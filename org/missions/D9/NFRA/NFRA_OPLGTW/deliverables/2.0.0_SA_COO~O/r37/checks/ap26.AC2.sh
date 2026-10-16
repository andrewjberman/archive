#!/usr/bin/env bash
# OPLGTW OG-ap-26 AC2 (round-37 CLASS-INCREMENT, PHASE B): the ledger nfra-oplgtw-grants-ap26 is CLOSED with its sentinel gone, and the grant has MOVED, RE-READ from IAM:
# the internal reader role holds the policy named in W/CLS2_APPLIED.json (one statement, dynamodb:GetItem, the table ARN), the gateway instance role no longer holds it,
# the simulator allows GetItem for the internal reader role and does not allow Scan (negative control) nor GetItem for the instance role.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-grants-ap26; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/CLS2_APPLIED.json" ] || { echo "CLS2_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r pol arn <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('policy_name',''),d.get('table_arn',''))" "$(native "$W/CLS2_APPLIED.json")" | tr -d '\r')"
IR=gateway-global-internal-reader-role; GWR=opal-gateway-role
doc=$(aws iam get-role-policy --role-name "$IR" --policy-name "$pol" --query PolicyDocument --output json 2>/dev/null | tr -d '\r')
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
gone=$(aws iam list-role-policies --role-name "$GWR" --query "PolicyNames[?@=='$pol']" --output text 2>/dev/null | tr -d '\r' | grep -c .)
sim() { aws iam simulate-principal-policy --policy-source-arn "$(aws iam get-role --role-name $1 --query Role.Arn --output text | tr -d '\r')" --action-names "$2" --resource-arns "$arn" --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null | tr -d '\r'; }
g=$(sim $IR dynamodb:GetItem); s=$(sim $IR dynamodb:Scan); gi=$(sim $GWR dynamodb:GetItem)
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; internal reader holds policy $pol shape $shape; instance role still holds it $gone (want 0); simulate internal reader GetItem $g, Scan $s (negative control); instance role GetItem $gi"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$shape" = ok ] && [ "$gone" = 0 ] && [ "$g" = allowed ] && [ "$s" != allowed ] && [ "$gi" != allowed ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
