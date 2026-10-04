#!/usr/bin/env bash
# _ssm.sh -- sourced by round-13 checks: run one AWS-RunShellScript parameters JSON on the opal-gateway host, print its
# stdout. ssm_run <params-json> -> sets SSM_OUT, SSM_STATUS, SSM_ID.
INST="i-07dccb1615503ac99"
ssm_run() {
  SSM_ID=$(aws ssm send-command --instance-ids "$INST" --document-name AWS-RunShellScript --region us-east-1 \
    --parameters "$1" --query Command.CommandId --output text | tr -d '\r')
  SSM_STATUS=""
  for _ in $(seq 1 30); do
    SSM_STATUS=$(aws ssm get-command-invocation --command-id "$SSM_ID" --instance-id "$INST" --region us-east-1 \
      --query Status --output text 2>&1 | tr -d '\r')
    case "$SSM_STATUS" in Success|Failed|Cancelled|TimedOut) break;; esac; sleep 3
  done
  SSM_OUT=$(aws ssm get-command-invocation --command-id "$SSM_ID" --instance-id "$INST" --region us-east-1 \
    --query StandardOutputContent --output text | tr -d '\r')
}
