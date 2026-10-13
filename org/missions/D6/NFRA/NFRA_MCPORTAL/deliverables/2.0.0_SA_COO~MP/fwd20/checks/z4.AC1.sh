#!/usr/bin/env bash
# MP-z-4 AC1 (APPLIED, live IAM): opal-gateway-role carries the inline policy gateway-access-state-principal-scan-policy
# whose statements allow EXACTLY dynamodb:Scan on the gateway-access-state-table ARN -- no other action, resource or effect.
# Then by simulation, one call per arm (CLAUDE.md 22a):
#   Scan    gateway-access-state-table     allowed       (the one new read)
#   Scan    mcportal-grant-changes-table   allowed       (the existing read, unchanged: control)
#   Scan    opal-users-v2                  implicitDeny  (no other table)
#   GetItem gateway-access-state-table     allowed       (the existing strong read: control)
# policy exact AND 4 of 4 arms must match.
. "$(dirname "$0")/_root.sh"
doc=$("$AWS" iam get-role-policy --role-name opal-gateway-role --policy-name gateway-access-state-principal-scan-policy --query PolicyDocument --output json 2>&1 | tr -d '\r'); rc=$?
[ "$rc" = 0 ] || { printf '%s\n' "$doc" | tail -2; echo "get-role-policy rc=$rc"; echo "RESULT: FAIL"; exit 1; }
ACC=$("$AWS" sts get-caller-identity --query Account --output text 2>&1 | tr -d '\r')
T="arn:aws:dynamodb:us-east-1:$ACC:table"
out=$(printf '%s' "$doc" | python -c "
import json,sys,urllib.parse
d=json.loads(sys.stdin.read())
if isinstance(d,str): d=json.loads(urllib.parse.unquote(d))
W=sys.argv[1]+'/gateway-access-state-table'
acts=set(); res=set(); bad=[]
for s in d['Statement']:
    a=s['Action']; a=[a] if isinstance(a,str) else a
    r=s['Resource']; r=[r] if isinstance(r,str) else r
    if s.get('Effect')!='Allow': bad.append('effect '+str(s.get('Effect')))
    if 'NotAction' in s or 'NotResource' in s: bad.append('Not* element')
    acts|=set(a); res|=set(r)
if acts!={'dynamodb:Scan'}: bad.append('actions '+','.join(sorted(acts)))
if res!={W}: bad.append('resources '+','.join(sorted(res)))
print('actions=%s resources=%d problems=%d' % ('+'.join(sorted(acts)),len(res),len(bad)))
for b in bad: print('  '+b)
" "$T" 2>&1 | tr -d '\r')
printf '%s\n' "$out"
ROLE_ARN=$("$AWS" iam get-role --role-name opal-gateway-role --query Role.Arn --output text 2>&1 | tr -d '\r')
ok=0
sim() { # label expect action resource
  local got v=MISMATCH
  got=$("$AWS" iam simulate-principal-policy --policy-source-arn "$ROLE_ARN" --action-names "$3" --resource-arns "$4" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r')
  [ "$got" = "$2" ] && { v=OK; ok=$((ok+1)); }
  echo "  $v  $1: expect $2, got $got"
}
sim "scan access-state"  allowed      dynamodb:Scan    "$T/gateway-access-state-table"
sim "scan changes"       allowed      dynamodb:Scan    "$T/mcportal-grant-changes-table"
sim "scan other table"   implicitDeny dynamodb:Scan    "$T/opal-users-v2"
sim "getitem control"    allowed      dynamodb:GetItem "$T/gateway-access-state-table"
echo "simulation arms matched $ok of 4"
if printf '%s\n' "$out" | grep -q 'actions=dynamodb:Scan resources=1 problems=0' && [ "$ok" = 4 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
