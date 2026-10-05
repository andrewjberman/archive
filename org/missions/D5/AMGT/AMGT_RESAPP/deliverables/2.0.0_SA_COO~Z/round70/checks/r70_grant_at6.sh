#!/usr/bin/env bash
# AMGT_RESAPP round 70, cell AMGT-at-6 grant leg: does opal-amgt-scoped-api-role read the issuer-site filing_source silver prefix
# that at-2's exec-roster chain reads at request time? APPLIED plane (simulate-principal-policy), one resource per call, each arm
# beside an isolated positive control on sec/harvest/silver/filing_source/ (already granted; the same table family).
# PASS = both target arms "allowed" AND both controls "allowed". Prints R70 AT6 GRANT: YES|NO.
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
check "control GetObject sec/harvest/silver/filing_source/" "$(sim s3:GetObject "arn:aws:s3:::$B/sec/harvest/silver/filing_source/x.parquet")"
check "control ListBucket prefix sec/harvest/silver/filing_source/" "$(sim s3:ListBucket "arn:aws:s3:::$B" sec/harvest/silver/filing_source/)"
check "C1 GetObject issuer-site/harvest/silver/filing_source/" "$(sim s3:GetObject "arn:aws:s3:::$B/issuer-site/harvest/silver/filing_source/x.parquet")"
check "C2 ListBucket prefix issuer-site/harvest/silver/filing_source/" "$(sim s3:ListBucket "arn:aws:s3:::$B" issuer-site/harvest/silver/filing_source/)"
if [ "$ok" = 1 ]; then echo "R70 AT6 GRANT: YES"; exit 0; else echo "R70 AT6 GRANT: NO"; exit 1; fi
