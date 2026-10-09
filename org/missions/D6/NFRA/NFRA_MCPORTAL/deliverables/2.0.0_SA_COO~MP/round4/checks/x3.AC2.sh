#!/usr/bin/env bash
# MP-x-3 AC2 (EXERCISED by simulation, one resource ARN per call -- CLAUDE.md 22a): on opal-gateway-role,
#   GetObject fabric/activity/v1/<key>     allowed
#   GetObject fabric/open-calls/v1/<key>   allowed
#   GetObject warehouse/<key>              implicitDeny   (the third prefix the ruling says is refused)
#   PutObject fabric/activity/v1/<key>     implicitDeny   (no write)
#   ListBucket, s3:prefix=fabric/activity/v1/   allowed
#   ListBucket, s3:prefix=warehouse/            implicitDeny
# 6 of 6 must match.
. "$(dirname "$0")/_root.sh"
ROLE_ARN=$(aws iam get-role --role-name opal-gateway-role --query Role.Arn --output text 2>&1 | tr -d '\r')
case "$ROLE_ARN" in arn:aws:iam::*) ;; *) echo "role read failed: $ROLE_ARN"; echo "RESULT: FAIL"; exit 1;; esac
B="arn:aws:s3:::opal-313476888478-globgrph"
ok=0
sim() { # label expect action resource [prefix]
  local ctx=()
  [ -n "${5:-}" ] && ctx=(--context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$5,ContextKeyType=string")
  local got
  got=$(aws iam simulate-principal-policy --policy-source-arn "$ROLE_ARN" --action-names "$3" --resource-arns "$4" "${ctx[@]}" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r')
  local v=MISMATCH; [ "$got" = "$2" ] && { v=OK; ok=$((ok+1)); }
  echo "  $v  $1: expect $2, got $got"
}
sim "get activity"    allowed      s3:GetObject  "$B/fabric/activity/v1/dt=2026-10-08/box=laptop/x.json"
sim "get open-calls"  allowed      s3:GetObject  "$B/fabric/open-calls/v1/box=laptop/open_calls.json"
sim "get warehouse"   implicitDeny s3:GetObject  "$B/warehouse/x.json"
sim "put activity"    implicitDeny s3:PutObject  "$B/fabric/activity/v1/dt=2026-10-08/box=laptop/x.json"
sim "list activity"   allowed      s3:ListBucket "$B" "fabric/activity/v1/"
sim "list warehouse"  implicitDeny s3:ListBucket "$B" "warehouse/"
echo "simulation arms matched $ok of 6"
if [ "$ok" = 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
