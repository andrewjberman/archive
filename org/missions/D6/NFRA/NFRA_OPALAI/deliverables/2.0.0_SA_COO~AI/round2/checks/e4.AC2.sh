#!/usr/bin/env bash
# OA-e-4 AC2 (seam probe against the REAL neighbour, the served gateway): the tool the skill names is SERVED to the
# Analyst's identity. Read LIVE over SSM on the gateway host: /opt/opal-gateway/app/tools.py defines
# read_chat_message_images, and /opt/opal-gateway/app/identity_scope.py names it (the concierge seed). A skill that
# names a tool the host does not serve fails here. Read-only; nothing on the host changes.
. "$(dirname "$0")/_root.sh"
CMD='commands=["grep -c \"def read_chat_message_images\" /opt/opal-gateway/app/tools.py || echo 0","grep -c read_chat_message_images /opt/opal-gateway/app/identity_scope.py || echo 0"]'
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids "$GW_INSTANCE" --document-name AWS-RunShellScript \
  --parameters "$CMD" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""
for i in 1 2 3 4 5 6 7 8 9 10; do
  st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query Status --output text 2>/dev/null | tr -d '\r')
  [ "$st" = Success ] || [ "$st" = Failed ] && break
  sleep 3
done
got=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
def=$(printf '%s\n' "$got" | sed -n 1p); seed=$(printf '%s\n' "$got" | sed -n 2p)
echo "served tools.py def read_chat_message_images=${def:-NONE}; served identity_scope.py mentions=${seed:-NONE} (ssm status ${st:-NONE}, command ${cid:-NONE})"
if [ "$st" = Success ] && [ "${def:-0}" -ge 1 ] 2>/dev/null && [ "${seed:-0}" -ge 1 ] 2>/dev/null; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
