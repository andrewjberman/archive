#!/usr/bin/env bash
# OPLGTW OG-tf-1 AC1 (analysis round 12 s.5 item 3; rows NFRA_MCPINDEX-Z-W21-S19 + ETFS_RIVALS-Z-W5-S3): the COMMITTED
# opal-gateway terraform root plans with ZERO errors from a FRESH linked worktree of HEAD -- no TF_VAR_*, no copied
# build output, no pruned copy. Exit 0 (no changes) or 2 (changes) both count; the summary is printed for the record.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_fresh_tf.sh"
fresh_plan ac1
if { [ "$PLAN_RC" = 0 ] || [ "$PLAN_RC" = 2 ]; } && [ "$PLAN_ERRORS" = 0 ] && [ "$PLAN_NOVALUE" = 0 ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
