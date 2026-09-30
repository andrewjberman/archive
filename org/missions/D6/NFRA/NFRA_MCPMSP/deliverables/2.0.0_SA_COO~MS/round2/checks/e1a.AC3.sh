#!/usr/bin/env bash
# MS-ir-2 AC3 (the control -- the Deny is NOT applied by this cell): the gateway role opal-gateway-role still reads
# opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json ALLOWED (its opal-internal serving is unmoved until
# MS-dn-1), and no policy named gateway-firm-deny-policy is attached to it.
. "$(dirname "$0")/_root.sh"
A=$(acct); G="arn:aws:iam::${A}:role/${GW_ROLE}"
r=$(sim "$G" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json")
dn=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('gateway', None, 'firm-deny', 'policy'))" 2>&1 | tr -d '\r' | tail -1)
pol=$(timeout 40 "$AWS" iam list-role-policies --role-name "$GW_ROLE" --query "PolicyNames" --output text 2>&1 | tr -d '\r')
has=$(printf '%s' "$pol" | tr '\t' '\n' | grep -cx "$dn")
echo "gateway role $GW_ROLE: firm-key GetObject=${r:-NONE}; inline policy $dn present=$has"
if [ "$r" = allowed ] && [ "$has" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
