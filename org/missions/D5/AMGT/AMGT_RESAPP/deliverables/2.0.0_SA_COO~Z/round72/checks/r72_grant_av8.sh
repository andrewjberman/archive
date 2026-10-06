#!/usr/bin/env bash
# AMGT_RESAPP round 72, cell AMGT-av-8 grant leg: does opal-amgt-scoped-api-role read what av-4 and av-6 add at request time?
#   C1/C2: av-4's segment read -- GetObject and ListBucket(s3:prefix) on filings/v1/ (removed from the grant at
#          scoped-amgt-api.tf:123);
#   C3:    av-6's one-call classification read -- dynamodb:BatchGetItem on the etf-classifications table.
# APPLIED plane (simulate-principal-policy), one resource per call, each beside a control the role already holds
# (sec/harvest/silver/filing_source/ for S3; GetItem on the same table for DynamoDB).
# PASS = every arm "allowed". Prints R72 AV8 GRANT: YES|NO.
set -u
ROLE="arn:aws:iam::313476888478:role/opal-amgt-scoped-api-role"
B="opal-data-harvest"
TABLE="arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications"
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
check "control GetObject sec/harvest/silver/filing_source/" "$(sim s3:GetObject "arn:aws:s3:::$B/sec/harvest/silver/filing_source/x.parquet")"
check "control ListBucket prefix sec/harvest/silver/filing_source/" "$(sim s3:ListBucket "arn:aws:s3:::$B" sec/harvest/silver/filing_source/)"
check "control dynamodb:GetItem etf-classifications" "$(sim dynamodb:GetItem "$TABLE")"
check "C1 GetObject filings/v1/<key>/<acc>.analysis.json" "$(sim s3:GetObject "arn:aws:s3:::$B/filings/v1/BA_US_Equity/0000000000.analysis.json")"
check "C2 ListBucket prefix filings/v1/<key>/" "$(sim s3:ListBucket "arn:aws:s3:::$B" filings/v1/BA_US_Equity/)"
check "C3 dynamodb:BatchGetItem etf-classifications" "$(sim dynamodb:BatchGetItem "$TABLE")"
if [ "$ok" = 1 ]; then echo "R72 AV8 GRANT: YES"; exit 0; else echo "R72 AV8 GRANT: NO"; exit 1; fi
