#!/usr/bin/env bash
# OPLGTW OG-tf-1 AC2: the fix moves nothing live -- from a FRESH linked worktree of HEAD, a plan TARGETED at the
# grant-writer resources (the ones the fix touches) reads "No changes." (exit 0).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_fresh_tf.sh"
fresh_plan ac2 -target=aws_lambda_function.mcportal_grant_writer -target=aws_lambda_layer_version.mcportal_grant_writer_deps \
  -target=aws_iam_role.mcportal_grant_writer -target=aws_iam_role_policy.mcportal_grant_writer_access_state
case "$PLAN_SUMMARY" in *"No changes."*) nc=yes;; *) nc=no;; esac
echo "targeted grant-writer plan reads No changes: $nc"
if [ "$PLAN_RC" = 0 ] && [ "$PLAN_ERRORS" = 0 ] && [ "$nc" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
