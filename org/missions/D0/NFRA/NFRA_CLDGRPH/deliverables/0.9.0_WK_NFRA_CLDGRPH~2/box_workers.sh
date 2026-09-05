#!/usr/bin/env bash
# box_workers.sh -- NFRA_CLDGRPH TO-CG-D-2 (D2-AC7): read the gateway's RUNNING uvicorn argv off the
# box by SSM and print it WHOLE, so `--workers 1` is measured on the live process rather than
# asserted from the unit file or the deploy script.
#
# Read-only: one `ps -o args -C python3.11` on i-07dccb1615503ac99. No file is written on the box,
# nothing is restarted. Bounded poll (max ~60 s); the raw StandardOutputContent is printed verbatim.
# ASCII only.
set -uo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
AWS="${REPO_ROOT}/.tools/aws"
INSTANCE_ID="i-07dccb1615503ac99"
REGION="us-east-1"

CMD_ID="$("$AWS" ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name AWS-RunShellScript \
  --comment "NFRA_CLDGRPH D2-AC7 workers read" \
  --parameters 'commands=["echo PROBE-1 the ps -C python3.11 form the TO names:","ps -o args -C python3.11 || true","echo PROBE-2 the RUNNING argv of the unit MainPID:","MP=$(systemctl show -p MainPID --value opal-gateway.service); echo MainPID=$MP; ps -p $MP -o args=","echo PROBE-3 unit state:","systemctl is-active opal-gateway.service || true"]' \
  --region "$REGION" --query Command.CommandId --output text)"
echo "SSM CommandId: $CMD_ID"

STATUS="Pending"
for _ in $(seq 1 20); do
  sleep 3
  STATUS="$("$AWS" ssm get-command-invocation --command-id "$CMD_ID" \
    --instance-id "$INSTANCE_ID" --region "$REGION" --query Status --output text 2>/dev/null || echo Pending)"
  case "$STATUS" in
    Success|Failed|Cancelled|TimedOut) break ;;
  esac
done
echo "SSM Status: $STATUS"
echo "--- StandardOutputContent (verbatim) ---"
"$AWS" ssm get-command-invocation --command-id "$CMD_ID" --instance-id "$INSTANCE_ID" \
  --region "$REGION" --query StandardOutputContent --output text
echo "--- StandardErrorContent (verbatim) ---"
"$AWS" ssm get-command-invocation --command-id "$CMD_ID" --instance-id "$INSTANCE_ID" \
  --region "$REGION" --query StandardErrorContent --output text
