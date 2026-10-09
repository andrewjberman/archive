#!/usr/bin/env bash
# OPLGTW OG-ap-3 AC1 (r29 apply, ANNOUNCE section 10): the secret gateway/mail/commassist-bearer exists (describe only,
# never its value), and the live inline policy gateway-read-secrets-policy on opal-gateway-role grants GetSecretValue on
# exactly 5 secret ARNs, one of them that secret's.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
arn=$(.tools/aws secretsmanager describe-secret --secret-id gateway/mail/commassist-bearer --region us-east-1 --query ARN --output text | tr -d '\r'); rc1=$?
pol=$(.tools/aws iam get-role-policy --role-name opal-gateway-role --policy-name gateway-read-secrets-policy --output json | tr -d '\r'); rc2=$?
res=$(printf '%s' "$pol" | ARN="$arn" python -c "
import json,os,sys
d=json.load(sys.stdin)['PolicyDocument']
st=d['Statement'] if isinstance(d['Statement'],list) else [d['Statement']]
rs=[]
for s in st:
    r=s.get('Resource',[]); rs+= r if isinstance(r,list) else [r]
a=os.environ.get('ARN','')
print(len(st), len(rs), sum(1 for r in rs if a and (r==a or r.startswith(a.rsplit('-',1)[0]))))" | tr -d '\r'); rc3=$?
set -- $res
echo "secret gateway/mail/commassist-bearer: describe rc=$rc1 arn_present=$([ -n "$arn" ] && [ "$arn" != None ] && echo yes || echo no)"
echo "gateway-read-secrets-policy: get rc=$rc2; statements $1; resources $2 (want 5); naming the new secret $3 (want 1)"
[ "$rc1" = 0 ] && [ -n "$arn" ] && [ "$rc2" = 0 ] && [ "$rc3" = 0 ] && [ "$2" = 5 ] && [ "$3" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
