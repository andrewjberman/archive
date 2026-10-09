#!/usr/bin/env bash
# MP-k-2 AC1 (APPLIED, live IAM; 1.0.0_SA_CTO~O ruling msg 32404 on Q3): opal-gateway-role carries the inline policy
# gateway-mcportal-close-request-write-policy whose statements allow EXACTLY s3:PutObject on
# arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/* -- no other action, resource or effect.
. "$(dirname "$0")/_root.sh"
doc=$("$AWS" iam get-role-policy --role-name opal-gateway-role --policy-name gateway-mcportal-close-request-write-policy --query PolicyDocument --output json 2>&1 | tr -d '\r'); rc=$?
[ "$rc" = 0 ] || { printf '%s\n' "$doc" | tail -2; echo "get-role-policy rc=$rc"; echo "RESULT: FAIL"; exit 1; }
out=$(printf '%s' "$doc" | python -c "
import json,sys,urllib.parse
d=json.loads(sys.stdin.read())
if isinstance(d,str): d=json.loads(urllib.parse.unquote(d))
W='arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*'
acts=set(); res=set(); bad=[]
for s in d['Statement']:
    a=s['Action']; a=[a] if isinstance(a,str) else a
    r=s['Resource']; r=[r] if isinstance(r,str) else r
    if s.get('Effect')!='Allow': bad.append('effect '+str(s.get('Effect')))
    if 'NotAction' in s or 'NotResource' in s: bad.append('Not* element')
    acts|=set(a); res|=set(r)
if acts!={'s3:PutObject'}: bad.append('actions '+','.join(sorted(acts)))
if res!={W}: bad.append('resources '+','.join(sorted(res)))
print('actions=%s resources=%d problems=%d' % ('+'.join(sorted(acts)),len(res),len(bad)))
for b in bad: print('  '+b)
" 2>&1 | tr -d '\r'); prc=$?
printf '%s\n' "$out"
if [ "$prc" = 0 ] && printf '%s\n' "$out" | grep -q 'actions=s3:PutObject resources=1 problems=0'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
