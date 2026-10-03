#!/usr/bin/env bash
# OPLGTW OG-tf-2 AC1 (analysis round 14 R2/R3; rows NFRA_MCPINDEX-Z-W21-S19, ETFS_RIVALS-Z-W5-S3): from a FRESH linked
# worktree of HEAD with every TF_VAR_* unset and no copied build output, the UNTARGETED opal-gateway plan exits 0 under
# -detailed-exitcode (No changes) with 0 errors and 0 missing required variables.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_fresh_tf.sh"
fresh_plan ac1
case "$PLAN_SUMMARY" in *"No changes."*) nc=yes;; *) nc=no;; esac
echo "untargeted plan reads No changes: $nc"
[ "$PLAN_RC" = 0 ] && [ "$PLAN_ERRORS" = 0 ] && [ "$PLAN_NOVALUE" = 0 ] && [ "$nc" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
