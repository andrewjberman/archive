#!/usr/bin/env bash
# MX-i-4 AC1 (least privilege, R-12 item 5): the LIVE inline policy AdditionalPermissions on bd-exporter-ec2-role no longer
# names the portal-login secret opal/bd/credentials. Read from IAM, never from the .tf.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
doc=$(timeout 60 "$AWS" iam get-role-policy --role-name bd-exporter-ec2-role --policy-name AdditionalPermissions --query PolicyDocument --output json 2>&1 | tr -d '\r'); rc=$?
stmts=$(printf '%s' "$doc" | grep -c '"Effect"')
n=$(printf '%s' "$doc" | grep -c 'secret:opal/bd/credentials')
echo "get-role-policy rc=$rc; statements read $stmts; resources naming opal/bd/credentials: $n"
if [ "$rc" = 0 ] && [ "$stmts" -ge 1 ] && [ "$n" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
