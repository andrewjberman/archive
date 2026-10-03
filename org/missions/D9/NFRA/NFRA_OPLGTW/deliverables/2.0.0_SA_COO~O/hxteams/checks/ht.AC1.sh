#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC1 (CTO ruling CTO_RULING_20261002_NFRA_OPLGTW_HX_TEAMS_RELEASE.md, AC1), LIVE AWS reads:
#  1. iam simulate-principal-policy, opal-gateway-role, GetSecretValue on gateway/teams/bearer -> allowed;
#  2. the same on a SYNTHETIC sibling ARN under gateway/teams/ -> implicitDeny. No real ungranted gateway/* sibling
#     exists after this release (5 gateway/* secrets: 4 granted by gateway-read-secrets-policy, 1 by the Tax policy),
#     so the negative arm is a well-formed ARN the policy would match only through a wildcard;
#  3. gateway-read-secrets-policy holds ONE statement, ONE action and EXACTLY the four named ARNs;
#  4. ALB rule priority 35 on the opal-gateway :443 listener lists 3 path values including /hx/teams/*.
# No secret value is read.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R=us-east-1; ACCT=313476888478; n=0
ROLE_ARN="arn:aws:iam::${ACCT}:role/opal-gateway-role"
TEAMS=$(aws secretsmanager describe-secret --region $R --secret-id gateway/teams/bearer --query ARN --output text | tr -d '\r')
SIB="arn:aws:secretsmanager:${R}:${ACCT}:secret:gateway/teams/sibling-control-AbCdEf"
sim() { aws iam simulate-principal-policy --policy-source-arn "$ROLE_ARN" --action-names secretsmanager:GetSecretValue \
  --resource-arns "$1" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'; }
d1=$(sim "$TEAMS"); d2=$(sim "$SIB")
if [ "$d1" = allowed ]; then echo "arm 1 gateway/teams/bearer -> $d1: OK"; n=$((n+1)); else echo "arm 1 gateway/teams/bearer -> $d1: FAIL"; fi
if [ "$d2" = implicitDeny ]; then echo "arm 2 synthetic sibling gateway/teams/* -> $d2: OK"; n=$((n+1)); else echo "arm 2 synthetic sibling -> $d2: FAIL"; fi
pol=$(aws iam get-role-policy --role-name opal-gateway-role --policy-name gateway-read-secrets-policy --query PolicyDocument --output json | tr -d '\r')
p3=$(printf '%s' "$pol" | python -c "
import json,sys
d=json.loads(sys.stdin.read()); st=d['Statement']
res=st[0]['Resource'] if len(st)==1 else []
res=[res] if isinstance(res,str) else res
acts=st[0]['Action'] if len(st)==1 else []
acts=[acts] if isinstance(acts,str) else acts
names=sorted(a.split(':secret:')[1].rsplit('-',1)[0] for a in res)
want=['gateway/mail/bearer','gateway/principals/rosters','gateway/teams/bearer','gateway/transcripts/bearer']
wild=sum(1 for a in res if '*' in a)
print('statements %d actions %s arns %d wildcard %d names %s exact %s' % (len(st), acts, len(res), wild, names, names==want and wild==0 and acts==['secretsmanager:GetSecretValue']))
")
echo "policy: $p3"
if printf '%s' "$p3" | grep -q "exact True$"; then echo "arm 3 gateway-read-secrets-policy exactly 4 named ARNs: OK"; n=$((n+1)); else echo "arm 3 policy shape: FAIL"; fi
LB=$(aws elbv2 describe-load-balancers --region $R --names opal-gateway --query 'LoadBalancers[0].LoadBalancerArn' --output text | tr -d '\r')
L=$(aws elbv2 describe-listeners --region $R --load-balancer-arn "$LB" --query 'Listeners[?Port==`443`].ListenerArn' --output text | tr -d '\r')
vals=$(aws elbv2 describe-rules --region $R --listener-arn "$L" --query "Rules[?Priority=='35'].Conditions[].PathPatternConfig.Values[]" --output text | tr -d '\r' | tr '\t' '\n' | sort)
nv=$(printf '%s\n' "$vals" | grep -c .); ht=$(printf '%s\n' "$vals" | grep -cx '/hx/teams/\*')
echo "rule 35 path values $nv: $(printf '%s' "$vals" | tr '\n' ' ')"
if [ "$nv" = 3 ] && [ "$ht" = 1 ]; then echo "arm 4 rule 35 lists 3 values incl /hx/teams/*: OK"; n=$((n+1)); else echo "arm 4 rule 35: FAIL"; fi
echo "INFRA ARMS $n of 4"
[ "$n" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
