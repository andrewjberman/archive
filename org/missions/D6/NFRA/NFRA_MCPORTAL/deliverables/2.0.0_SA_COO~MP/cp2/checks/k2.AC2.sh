#!/usr/bin/env bash
# MP-k-2 AC2 (EXERCISED by simulation, one resource ARN per call -- CLAUDE.md 22a): on opal-gateway-role,
#   PutObject    open-calls/v1/box=sitez/requests/<id>.json   allowed       (the one write)
#   PutObject    open-calls/v1/box=sitez/open_calls.json      implicitDeny  (the list itself: C11, never edited)
#   PutObject    open-calls/v1/box=sitez/request_results/x    implicitDeny  (the box's result, not the page's)
#   PutObject    activity/v1/dt=2026-10-09/box=sitez/x.json   implicitDeny
#   DeleteObject open-calls/v1/box=sitez/requests/<id>.json   implicitDeny  (no delete)
#   GetObject    open-calls/v1/box=sitez/open_calls.json      allowed       (MP-x-3's read, unchanged: control)
# 6 of 6 must match.
. "$(dirname "$0")/_root.sh"
ROLE_ARN=$("$AWS" iam get-role --role-name opal-gateway-role --query Role.Arn --output text 2>&1 | tr -d '\r')
case "$ROLE_ARN" in arn:aws:iam::*) ;; *) echo "role read failed: $ROLE_ARN"; echo "RESULT: FAIL"; exit 1;; esac
B="arn:aws:s3:::opal-313476888478-globgrph/fabric"
ok=0
sim() { # label expect action resource
  local got v=MISMATCH
  got=$("$AWS" iam simulate-principal-policy --policy-source-arn "$ROLE_ARN" --action-names "$3" --resource-arns "$4" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r')
  [ "$got" = "$2" ] && { v=OK; ok=$((ok+1)); }
  echo "  $v  $1: expect $2, got $got"
}
sim "put request"      allowed      s3:PutObject    "$B/open-calls/v1/box=sitez/requests/20261009T120000Z-0a1b2c3d.json"
sim "put list"         implicitDeny s3:PutObject    "$B/open-calls/v1/box=sitez/open_calls.json"
sim "put result"       implicitDeny s3:PutObject    "$B/open-calls/v1/box=sitez/request_results/x.json"
sim "put activity"     implicitDeny s3:PutObject    "$B/activity/v1/dt=2026-10-09/box=sitez/x.json"
sim "delete request"   implicitDeny s3:DeleteObject "$B/open-calls/v1/box=sitez/requests/20261009T120000Z-0a1b2c3d.json"
sim "get list"         allowed      s3:GetObject    "$B/open-calls/v1/box=sitez/open_calls.json"
echo "simulation arms matched $ok of 6"
if [ "$ok" = 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
