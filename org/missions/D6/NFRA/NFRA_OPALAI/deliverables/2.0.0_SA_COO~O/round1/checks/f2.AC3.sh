#!/usr/bin/env bash
# OA-f-2 AC3 (the SERVED overlay): the host's /opt/opal-gateway/identity_tool_allowlist.txt, read LIVE over SSM, has
# 0 unqualified 'opalbloomberg@opalinvest.com opal_data_refresh_upload' rows and exactly 1 qualified with client=.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids i-07dccb1615503ac99 --document-name AWS-RunShellScript \
  --parameters 'commands=["sed -e s/#.*// /opt/opal-gateway/identity_tool_allowlist.txt | grep -i opal_data_refresh_upload || echo NO-UPLOAD-ROWS"]' \
  --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""
for i in 1 2 3 4 5 6 7 8 9 10; do
  st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id i-07dccb1615503ac99 --query Status --output text 2>/dev/null | tr -d '\r')
  [ "$st" = Success ] || [ "$st" = Failed ] && break
  sleep 3
done
out=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id i-07dccb1615503ac99 --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rows=$(printf '%s\n' "$out" | grep -iE '^[[:space:]]*opalbloomberg@opalinvest\.com[[:space:]]+opal_data_refresh_upload')
unq=$(printf '%s\n' "$rows" | grep . | grep -vc 'client=')
q=$(printf '%s\n' "$rows" | grep -c 'client=')
echo "live upload rows: unqualified=$unq client-qualified=$q (ssm status ${st:-NONE}, command ${cid:-NONE})"
if [ "$st" = Success ] && [ "$unq" = 0 ] && [ "$q" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
