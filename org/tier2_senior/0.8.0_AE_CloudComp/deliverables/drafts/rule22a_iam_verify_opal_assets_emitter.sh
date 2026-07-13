#!/usr/bin/env bash
# Rule-22a LIVE IAM verification for the OPAL_ASSETS bucket-emitter DynamoDB write.
# Author: 0.8.0_AE_CloudComp | 2026-07-13 | PRE-STAGED -- fill the 4 ARNs on ~A handoff.
#
# WHY (Rule 22a): comp-iam models (action) NOT (action,resource) -- a role holding
# dynamodb:PutItem on ANY table reports GRANTED for a call to a NEW table. So a NEW
# resource (opal-assets-daily-aum + its GSI) is verified with simulate-principal-policy
# on the EXACT ARNs, WITH a positive control on a resource the role DOES hold (else a
# 403/SigV4/policy refusal reads as implicitDeny and you learn nothing).
#
# FILL ON HANDOFF (from ~A): EMITTER_ROLE_ARN, TABLE_ARN, GSI_ARN. The positive control
# defaults to the emitter's own s3:GetObject on the mdpf served prefix (a grant it MUST
# hold to read its one input) -- override if ~A's role scopes it differently.
set -euo pipefail

EMITTER_ROLE_ARN="${EMITTER_ROLE_ARN:-FILL:arn:aws:iam::<ACCT>:role/opal-assets-bucket-emitter-role}"
TABLE_ARN="${TABLE_ARN:-FILL:arn:aws:dynamodb:us-east-1:<ACCT>:table/opal-assets-daily-aum}"
GSI_ARN="${GSI_ARN:-${TABLE_ARN}/index/by-day}"
# Positive control: an action+resource the role DOES hold. Default = its input read.
POS_CTRL_ACTION="${POS_CTRL_ACTION:-s3:GetObject}"
POS_CTRL_ARN="${POS_CTRL_ARN:-arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/aggregate_aua/*}"

if [[ "$EMITTER_ROLE_ARN" == FILL:* || "$TABLE_ARN" == FILL:* ]]; then
  echo "BLOCKED: fill EMITTER_ROLE_ARN + TABLE_ARN (+ GSI_ARN if not table/index/by-day) from ~A's handoff first." >&2
  echo "  e.g. EMITTER_ROLE_ARN=arn:... TABLE_ARN=arn:... bash $0" >&2
  exit 2
fi

_q='EvaluationResults[].{action:EvalActionName,resource:EvalResourceName,decision:EvalDecision}'

echo "=== [1] THE WRITE GRANT: PutItem + UpdateItem on the EXACT TABLE ARN ==="
# PutItem/UpdateItem act on the TABLE (a GSI is written transitively, never targeted).
aws iam simulate-principal-policy \
  --policy-source-arn "$EMITTER_ROLE_ARN" \
  --action-names dynamodb:PutItem dynamodb:UpdateItem \
  --resource-arns "$TABLE_ARN" \
  --query "$_q" --output table

echo "=== [2] THE READ-BACK GRANT: Query on the EXACT TABLE ARN + GSI ARN ==="
# Query targets the table (cohort history) AND the by-day GSI (a day's 14 rows).
aws iam simulate-principal-policy \
  --policy-source-arn "$EMITTER_ROLE_ARN" \
  --action-names dynamodb:Query \
  --resource-arns "$TABLE_ARN" "$GSI_ARN" \
  --query "$_q" --output table

echo "=== [3] POSITIVE CONTROL: an action the role DOES hold (proves the simulator sees the policy) ==="
aws iam simulate-principal-policy \
  --policy-source-arn "$EMITTER_ROLE_ARN" \
  --action-names "$POS_CTRL_ACTION" \
  --resource-arns "$POS_CTRL_ARN" \
  --query "$_q" --output table

cat <<'EOF'

PASS CRITERIA (all three must hold):
  [1] PutItem + UpdateItem on TABLE_ARN      -> allowed
  [2] Query on TABLE_ARN AND GSI_ARN         -> allowed (both rows)
  [3] positive control                       -> allowed  (if this is DENIED, the sim is
      not seeing the role's policy -> [1]/[2] "implicitDeny" is uninformative, NOT a real deny)

THEN (Rule 22a exercise -- APPLIED truth, not simulator): assume the DEPLOYED emitter role
(or invoke the emitter Lambda) and do ONE real PutItem of a probe row, Query it back via the
GSI, then delete the probe. A green simulator + a green exercise = the grant is real. A
comp-iam DESIRED verdict or a local-cred write does NOT satisfy this (TO invariant 4).
EOF
