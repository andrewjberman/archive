#!/usr/bin/env bash
# OPLGTW OG-cd-3 AC2 (round 46, PHASE B): the ledger nfra-oplgtw-grants-cd3 is CLOSED with its sentinel gone, and the read grant is LIVE in IAM, RE-READ here:
# the gateway role holds the policy named in W/FD_APPLIED.json with exactly FOUR Allow statements (the source-root list split from the silver list, CVO refusal @adba2df9a0) over exactly events:DescribeRule, s3:GetObject, s3:ListBucket; the simulator ALLOWS events:DescribeRule on the sample sweep-rule ARN
# and s3:GetObject on the sample backfill-status key ARN of the record, and does NOT allow the negative controls events:PutRule on the rule ARN or s3:PutObject on the same key ARN.
# AMENDMENT A1: the simulator, with s3:prefix = the record's sample_root_prefix (a source root such as schwab/) ALLOWS s3:ListBucket when s3:delimiter is "/" and does NOT allow it when s3:delimiter is absent (the recursive root list).
# Override (dry-run controls only): CD3_APPLIED_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${CD3_APPLIED_OVERRIDE:-$W/FD_APPLIED.json}"
slug=nfra-oplgtw-grants-cd3; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$REC" ] || { echo "FD_APPLIED.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r pol rule key rootp <<<"$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('policy_name',''),d.get('sample_rule_arn',''),d.get('sample_status_key_arn',''),d.get('sample_root_prefix',''))" "$(native "$REC")" | tr -d '\r')"
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
print('ok' if len(st)==4 and acts==['events:DescribeRule','s3:GetObject','s3:ListBucket'] and all(s.get('Effect')=='Allow' for s in st) else 'wrong')
" | tr -d '\r')
arn=$(aws iam get-role --role-name "$role" --query Role.Arn --output text | tr -d '\r')
sim() { aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names "$1" --resource-arns "$2" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; }
simlist() { if [ -n "$2" ]; then aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names s3:ListBucket --resource-arns arn:aws:s3:::opal-data-assets --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$1,ContextKeyType=string" "ContextKeyName=s3:delimiter,ContextKeyValues=$2,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d ''; else aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names s3:ListBucket --resource-arns arn:aws:s3:::opal-data-assets --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$1,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d ''; fi; }
e=denied; f=allowed; if [ -n "$rootp" ]; then e=$(simlist "$rootp" "/"); f=$(simlist "$rootp" ""); fi
a=$(sim events:DescribeRule "$rule"); b=$(sim s3:GetObject "$key"); c=$(sim events:PutRule "$rule"); d=$(sim s3:PutObject "$key")
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; policy $pol shape $shape; simulate DescribeRule $a, GetObject $b; root list with delimiter $e, root list with NO delimiter (negative control) $f; negative controls PutRule $c, PutObject $d"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$shape" = ok ] && [ "$a" = allowed ] && [ "$b" = allowed ] && [ "$e" = allowed ] && [ "$f" != allowed ] && [ "$c" != allowed ] && [ "$d" != allowed ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
