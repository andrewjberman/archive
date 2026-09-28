#!/usr/bin/env bash
# MP-c-1 AC2 (A1n, the two arms reachable LIVE): (i) the DEPLOYED writer invoked with no owner header answers REFUSED
# NO-OWNER-HEADER; (iv) from the gateway host, whose instance role is the gateway role, `sts assume-role` on the operator
# role opal-gateway-access-admin is DENIED (the trust's ArnNotEquals stands, PRD C4). Arms (ii) a valid non-owner header
# and (iii) an owner header past its `exp` need an ALB-signed header no seat can mint; they stand on MP-b-2's in-package
# tests (fixture, per the diet's clause (b)), named on the face.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_c1_ac2_$$"; mkdir -p "$T"
p='{"action":"narrow","tid":"00000000-0000-4000-8000-0000000000e5","oid":"00000000-0000-4000-8000-0000000000f6","candidate":{}}'
timeout 60 "$AWS" lambda invoke --function-name "$nm" --cli-binary-format raw-in-base64-out --payload "$p" "$(cygpath -w "$T/r.json")" >/dev/null 2>&1
v=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('verdict'),d.get('reason'))" "$T/r.json" 2>/dev/null || echo "NONE NONE")
python - "$T/params.json" <<'EOF'
import json, sys
cmd = ('A=$(aws sts get-caller-identity --query Account --output text 2>&1); '
       'echo CALLER=$(aws sts get-caller-identity --query Arn --output text 2>&1 | sed -E "s/[0-9]{12}/ACCT/"); '
       'aws sts assume-role --role-arn arn:aws:iam::$A:role/opal-gateway-access-admin --role-session-name mp-c1-a1n '
       '--query AssumedRoleUser.Arn --output text 2>&1 | sed -E "s/[0-9]{12}/ACCT/g" | head -c 300; echo')
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$T/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
o=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$T"
denied=no; printf '%s' "$o" | grep -q 'AccessDenied' && ! printf '%s' "$o" | grep -q 'assumed-role/opal-gateway-access-admin' && denied=yes
echo "arm (i) function $nm, no header -> $v"
echo "arm (iv) ssm command=${cid:-NONE} status=${st:-NONE}; $(printf '%s' "$o" | tr '\n' ' ' | cut -c1-260); denied=$denied"
if [ "$v" = "REFUSED NO-OWNER-HEADER" ] && [ "$st" = Success ] && [ "$denied" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
