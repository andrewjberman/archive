#!/usr/bin/env bash
# OA-e-3 AC2 (the SERVED code, not the self-report): the host's /opt/opal-gateway/app/identity_scope.py, read LIVE over SSM, has the same
# md5 as app/identity_scope.py at the tip of the release branch rel-nfra-opalai-r2-asker-switch-on-gateway (the live base at the cut plus this cell's commits; the
# base is not CLOUD, so CLOUD HEAD is not the oracle). The live file also names opal_asker_query at least once.
. "$(dirname "$0")/_root.sh"
want=""; git rev-parse -q --verify rel-nfra-opalai-r2-asker-switch-on-gateway >/dev/null && want=$(git show rel-nfra-opalai-r2-asker-switch-on-gateway:infra/aws/ec2/opal-gateway/app/identity_scope.py | md5sum | awk '{print $1}')
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids "$GW_INSTANCE" --document-name AWS-RunShellScript \
  --parameters 'commands=["md5sum /opt/opal-gateway/app/identity_scope.py || echo MISSING; grep -c opal_asker_query /opt/opal-gateway/app/identity_scope.py || true"]' --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""
for i in 1 2 3 4 5 6 7 8 9 10; do
  st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query Status --output text 2>/dev/null | tr -d '\r')
  [ "$st" = Success ] || [ "$st" = Failed ] && break
  sleep 3
done
outc=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
got=$(printf '%s\n' "$outc" | head -1 | awk '{print $1}')
echo "release-branch md5=${want:-NONE}; live md5=${got:-NONE} (ssm status ${st:-NONE}, command ${cid:-NONE})"
names=$(printf '%s\n' "$outc" | sed -n 2p | tr -d ' '); echo "live lines naming opal_asker_query: ${names:-NONE}"
if [ -n "$want" ] && [ "$got" = "$want" ] && [ "${names:-0}" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
