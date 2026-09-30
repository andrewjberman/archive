#!/usr/bin/env bash
# MX-i-4 AC2 (regression guard): the same live policy STILL grants GetSecretValue on the 49F session secret the REST
# asset-dim pull reads (MX-s-10 A5), so the least-privilege cut cannot break the scheduled producer.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
doc=$(timeout 60 "$AWS" iam get-role-policy --role-name bd-exporter-ec2-role --policy-name AdditionalPermissions --query PolicyDocument --output json 2>&1 | tr -d '\r'); rc=$?
n=$(printf '%s' "$doc" | grep -c 'secret:blackdiamond/49f/session')
g=$(printf '%s' "$doc" | grep -c 'secretsmanager:GetSecretValue')
echo "get-role-policy rc=$rc; GetSecretValue actions $g; resources naming blackdiamond/49f/session: $n"
if [ "$rc" = 0 ] && [ "$g" -ge 1 ] && [ "$n" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
