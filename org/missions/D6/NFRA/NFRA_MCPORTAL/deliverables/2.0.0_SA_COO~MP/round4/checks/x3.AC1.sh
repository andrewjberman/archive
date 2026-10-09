#!/usr/bin/env bash
# MP-x-3 AC1 (APPLIED, live IAM, ruling (a) relayed as msg 32030): opal-gateway-role carries the inline policy
# gateway-mcportal-fabric-read-policy, whose statements allow EXACTLY s3:GetObject on the two prefixes
# fabric/activity/v1/* and fabric/open-calls/v1/* of opal-313476888478-globgrph, and s3:ListBucket on that bucket
# conditioned on s3:prefix to those two prefixes only. No other action, resource or effect.
. "$(dirname "$0")/_root.sh"
doc=$(aws iam get-role-policy --role-name opal-gateway-role --policy-name gateway-mcportal-fabric-read-policy --query PolicyDocument --output json 2>&1 | tr -d '\r'); rc=$?
[ "$rc" = 0 ] || { printf '%s\n' "$doc" | tail -2; echo "get-role-policy rc=$rc"; echo "RESULT: FAIL"; exit 1; }
out=$(printf '%s' "$doc" | python -c "
import json,sys,urllib.parse
d=json.loads(sys.stdin.read())
if isinstance(d,str): d=json.loads(urllib.parse.unquote(d))
B='arn:aws:s3:::opal-313476888478-globgrph'
P=['fabric/activity/v1/','fabric/open-calls/v1/']
acts=set(); res=set(); bad=[]
for s in d['Statement']:
    a=s['Action']; a=[a] if isinstance(a,str) else a
    r=s['Resource']; r=[r] if isinstance(r,str) else r
    if s.get('Effect')!='Allow': bad.append('effect '+str(s.get('Effect')))
    acts|=set(a); res|=set(r)
    if 'NotAction' in s or 'NotResource' in s: bad.append('Not* element')
    if a==['s3:ListBucket']:
        c=json.dumps(s.get('Condition',{}))
        for p in P:
            if p not in c: bad.append('ListBucket condition lacks '+p)
        if 'warehouse' in c or 'projection' in c: bad.append('ListBucket condition names a third prefix')
        if not s.get('Condition'): bad.append('ListBucket unconditioned')
want_res={B+'/'+p+'*' for p in P}|{B}
if acts!={'s3:GetObject','s3:ListBucket'}: bad.append('actions '+','.join(sorted(acts)))
if res!=want_res: bad.append('resources '+','.join(sorted(res)))
print('actions=%s resources=%d problems=%d' % ('+'.join(sorted(acts)),len(res),len(bad)))
for b in bad: print('  '+b)
" 2>&1 | tr -d '\r'); prc=$?
printf '%s\n' "$out"
if [ "$prc" = 0 ] && printf '%s\n' "$out" | grep -q 'problems=0'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
