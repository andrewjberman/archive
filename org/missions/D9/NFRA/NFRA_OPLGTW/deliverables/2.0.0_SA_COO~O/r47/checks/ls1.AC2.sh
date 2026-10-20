#!/usr/bin/env bash
# OPLGTW OG-ls-1 AC2 (round 47, PHASE B): the ledger nfra-oplgtw-grants-ls1 is CLOSED with its sentinel gone, and the narrowed read grant is LIVE in IAM, RE-READ here:
# the gateway role holds the policy named in W/LS_APPLIED.json with exactly FOUR Allow statements over exactly events:DescribeRule, s3:GetObject, s3:ListBucket, no silver pattern that starts with "*/", and the simulator
#   ALLOWS s3:ListBucket on opal-data-assets with s3:prefix = the record's sample_silver_prefix (a prefix under a source, such as schwab/x/silver/t/);
#   does NOT allow it for the three prefixes the census found outside the eight sources (bloomberg/global/silver/, gateway/global/silver/, yahoo/g/silver/) -- these were allowed before this order;
#   still ALLOWS the source-root list with s3:delimiter "/" and does NOT allow it with the delimiter absent;
#   and does NOT allow the write controls events:PutRule on the sample rule ARN or s3:PutObject on the sample key ARN, while ALLOWING events:DescribeRule and s3:GetObject on those two ARNs (the unchanged statements).
# Override (dry-run controls only): LS1_APPLIED_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${LS1_APPLIED_OVERRIDE:-$W/LS_APPLIED.json}"
slug=nfra-oplgtw-grants-ls1; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
role=opal-gateway-role
if [ -f "$REC" ]; then
  read -r pol rule key sp rootp <<<"$(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('policy_name',''),d.get('sample_rule_arn',''),d.get('sample_status_key_arn',''),d.get('sample_silver_prefix',''),d.get('sample_root_prefix',''))" "$(native "$REC")" | tr -d '\r')"
else
  pol=gateway-family-depth-read-policy; rule=""; key=""; sp="schwab/x/silver/t/"; rootp="schwab/"
fi
doc=$(.tools/aws iam get-role-policy --role-name "$role" --policy-name "$pol" --query PolicyDocument --output json | tr -d '\r')
shape=$(printf '%s' "$doc" | python3 -I -c "
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print('unreadable'); sys.exit()
st=d.get('Statement'); st=[st] if isinstance(st,dict) else (st or [])
acts=sorted({a for s in st for a in ([s.get('Action')] if isinstance(s.get('Action'),str) else (s.get('Action') or []))})
broad=False
for s in st:
    c=((s.get('Condition') or {}).get('StringLike') or {}).get('s3:prefix')
    c=[c] if isinstance(c,str) else (c or [])
    if any(p.startswith('*/') for p in c): broad=True
print('ok' if len(st)==4 and acts==['events:DescribeRule','s3:GetObject','s3:ListBucket'] and all(s.get('Effect')=='Allow' for s in st) and not broad else ('broad' if broad else 'wrong'))
" | tr -d '\r')
arn=$(.tools/aws iam get-role --role-name "$role" --query Role.Arn --output text | tr -d '\r')
sim() { .tools/aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names "$1" --resource-arns "$2" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; }
simlist() { if [ -n "$2" ]; then .tools/aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names s3:ListBucket --resource-arns arn:aws:s3:::opal-data-assets --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$1,ContextKeyType=string" "ContextKeyName=s3:delimiter,ContextKeyValues=$2,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; else .tools/aws iam simulate-principal-policy --policy-source-arn "$arn" --action-names s3:ListBucket --resource-arns arn:aws:s3:::opal-data-assets --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$1,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; fi; }
src=$(simlist "$sp" ""); bl=$(simlist "bloomberg/global/silver/" ""); gw=$(simlist "gateway/global/silver/" ""); yh=$(simlist "yahoo/g/silver/" "")
rootd=denied; rootn=allowed; if [ -n "$rootp" ]; then rootd=$(simlist "$rootp" "/"); rootn=$(simlist "$rootp" ""); fi
if [ -n "$rule" ] && [ -n "$key" ]; then a=$(sim events:DescribeRule "$rule"); b=$(sim s3:GetObject "$key"); c=$(sim events:PutRule "$rule"); d=$(sim s3:PutObject "$key"); else a=missing; b=missing; c=allowed; d=allowed; fi
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent; policy $pol shape $shape; silver list under a source $src; census prefixes outside the eight: bloomberg $bl, gateway $gw, yahoo $yh; root list with delimiter $rootd, root list with NO delimiter (negative control) $rootn; unchanged statements DescribeRule $a, GetObject $b; negative controls PutRule $c, PutObject $d"
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$shape" = ok ] && [ "$src" = allowed ] && [ "$bl" != allowed ] && [ "$gw" != allowed ] && [ "$yh" != allowed ] && [ "$rootd" = allowed ] && [ "$rootn" != allowed ] && [ "$a" = allowed ] && [ "$b" = allowed ] && [ "$c" != allowed ] && [ "$d" != allowed ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
