#!/usr/bin/env bash
# OA-g-2 AC3 (the SERVED code, not the self-report): the host's /opt/opal-gateway/app/asker_scope.py, read LIVE over
# SSM, has the same md5 as app/asker_scope.py at the tip of the release branch rel-nfra-opalai-portal-grant-gateway (the live
# base at the cut plus OA-f-1's change; the base is not CLOUD, so CLOUD HEAD is not the oracle).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
want=""; git rev-parse -q --verify rel-nfra-opalai-portal-grant-gateway >/dev/null && want=$(git show rel-nfra-opalai-portal-grant-gateway:infra/aws/ec2/opal-gateway/app/asker_scope.py | md5sum | awk '{print $1}')
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids i-07dccb1615503ac99 --document-name AWS-RunShellScript \
  --parameters 'commands=["md5sum /opt/opal-gateway/app/asker_scope.py || echo MISSING"]' --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""
for i in 1 2 3 4 5 6 7 8 9 10; do
  st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id i-07dccb1615503ac99 --query Status --output text 2>/dev/null | tr -d '\r')
  [ "$st" = Success ] || [ "$st" = Failed ] && break
  sleep 3
done
got=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id i-07dccb1615503ac99 --query StandardOutputContent --output text 2>/dev/null | tr -d '\r' | awk '{print $1}' | head -1)
echo "release-branch md5=${want:-NONE}; live md5=${got:-NONE} (ssm status ${st:-NONE}, command ${cid:-NONE})"
if [ -n "$want" ] && [ "$got" = "$want" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
