#!/usr/bin/env bash
# MP-t-3 AC2 (comp-iam, the APPLIED plane): the writer function is Active; the gateway role MAY invoke it (allowed); and
# the gateway role still may NOT assume the operator role opal-gateway-access-admin (implicitDeny or explicitDeny) --
# the grant is the one new edge and the trust condition stands.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
acct=$(timeout 30 "$AWS" sts get-caller-identity --query Account --output text 2>/dev/null | tr -d '\r')
st=$(timeout 30 "$AWS" lambda get-function --function-name "$nm" --query Configuration.State --output text 2>&1 | tr -d '\r' | tail -1)
fa=$(timeout 30 "$AWS" lambda get-function --function-name "$nm" --query Configuration.FunctionArn --output text 2>/dev/null | tr -d '\r')
GW="arn:aws:iam::${acct}:role/opal-gateway-role"; OP="arn:aws:iam::${acct}:role/opal-gateway-access-admin"
inv=$(timeout 40 "$AWS" iam simulate-principal-policy --policy-source-arn "$GW" --action-names lambda:InvokeFunction --resource-arns "$fa" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r' | tail -1)
asm=$(timeout 40 "$AWS" iam simulate-principal-policy --policy-source-arn "$GW" --action-names sts:AssumeRole --resource-arns "$OP" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r' | tail -1)
echo "function $nm state=$st; gateway invoke=$inv; gateway assume operator role=$asm"
if [ "$st" = Active ] && [ "$inv" = allowed ] && { [ "$asm" = implicitDeny ] || [ "$asm" = explicitDeny ]; }; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
