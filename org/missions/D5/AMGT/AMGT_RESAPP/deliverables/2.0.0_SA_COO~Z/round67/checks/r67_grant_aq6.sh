#!/usr/bin/env bash
# AMGT_RESAPP round 67, cell AMGT-aq-6 (row Z-S346): does opal-amgt-scoped-api-role read the chatter_window gold prefix?
# APPLIED plane (simulate-principal-policy), one resource per call, each arm beside an isolated positive control on the
# granted sibling prefix chatter_daily/ (the control proves the call and its --context-entries form were accepted).
# PASS = both target arms read "allowed" AND both controls read "allowed". Prints R67 AQ6 GRANT: YES|NO.
set -u
ROLE="arn:aws:iam::313476888478:role/opal-amgt-scoped-api-role"
B="opal-data-harvest"
sim() {  # $1 action, $2 resource arn, $3 optional s3:prefix context value
  if [ -n "${3:-}" ]; then
    MSYS_NO_PATHCONV=1 aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names "$1" \
      --resource-arns "$2" --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$3,ContextKeyType=string" \
      --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'
  else
    MSYS_NO_PATHCONV=1 aws iam simulate-principal-policy --policy-source-arn "$ROLE" --action-names "$1" \
      --resource-arns "$2" --query 'EvaluationResults[0].EvalDecision' --output text | tr -d '\r'
  fi
}
ok=1
check() {  # $1 label, $2 decision
  if [ "$2" = "allowed" ]; then echo "PASS $1 -> $2"; else echo "FAIL $1 -> ${2:-<empty>}"; ok=0; fi
}
check "control GetObject chatter_daily/" "$(sim s3:GetObject "arn:aws:s3:::$B/amgt/harvest/gold/chatter_daily/x.json")"
check "control ListBucket prefix chatter_daily/" "$(sim s3:ListBucket "arn:aws:s3:::$B" amgt/harvest/gold/chatter_daily/)"
check "C1 GetObject chatter_window/" "$(sim s3:GetObject "arn:aws:s3:::$B/amgt/harvest/gold/chatter_window/date=2026-10-01/part-0.json")"
check "C2 ListBucket prefix chatter_window/" "$(sim s3:ListBucket "arn:aws:s3:::$B" amgt/harvest/gold/chatter_window/)"
if [ "$ok" = 1 ]; then echo "R67 AQ6 GRANT: YES"; exit 0; else echo "R67 AQ6 GRANT: NO"; exit 1; fi
