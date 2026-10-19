#!/usr/bin/env bash
# OPLGTW OG-cd-3 AC2 (round 46, PHASE B): the ledger nfra-oplgtw-grants-cd3 is CLOSED with its sentinel gone, and the read grant is LIVE in IAM, RE-READ here:
# the gateway role holds the policy named in W/FD_APPLIED.json with exactly three Allow statements over exactly events:DescribeRule, s3:GetObject, s3:ListBucket; the simulator ALLOWS events:DescribeRule on the sample sweep-rule ARN
# and s3:GetObject on the sample backfill-status key ARN of the record, and does NOT allow the negative controls events:PutRule on the rule ARN or s3:PutObject on the same key ARN.
# Override (dry-run controls only): CD3_APPLIED_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${CD3_APPLIED_OVERRIDE:-$W/FD_APPLIED.json}"
slug=nfra-oplgtw-grants-cd3; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "FD_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r pol rule key <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('policy_name',''),d.get('sample_rule_arn',''),d.get('sample_status_key_arn',''))" "$(native "$REC")" | tr -d '\r')"
role=opal-gateway-role
doc=$(aws iam get-role-policy --role-name "$role" --policy-name "$pol" --query PolicyDocument --output json | tr -d '\r')
shape=$(printf '%s' "$doc" | python -I -c "
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print('unreadable'); sys.exit()
st=d.get('Statement'); st=[st] if isinstance(st,dict) else (st or [])
acts=sorted({a for s in st for a in ([s.get('Action')] if isinstance(s.get('Action'),str) else (s.get('Action') or []))})
print('ok' if len(st)==3 and acts==['events:DescribeRule','s3:GetObject','s3:ListBucket'] and all(s.get('Effect')=='Allow' for s in st) else 'wrong')
" | tr -d '\r')
arn=$(aws iam get-role --role-name "$role" --query Role.Arn --output text | tr -d '\r')
sim() { aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names "$1" --resource-arns "$2" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; }
a=$(sim events:DescribeRule "$rule"); b=$(sim s3:GetObject "$key"); c=$(sim events:PutRule "$rule"); d=$(sim s3:PutObject "$key")
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; policy $pol shape $shape; simulate DescribeRule $a, GetObject $b; negative controls PutRule $c, PutObject $d"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$shape" = ok ] && [ "$a" = allowed ] && [ "$b" = allowed ] && [ "$c" != allowed ] && [ "$d" != allowed ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
