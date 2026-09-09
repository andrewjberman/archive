#!/usr/bin/env bash
# E2-AC2 -- THE FOUR PINS ARE THE FIX'S DIGEST (the control that must be able to FAIL).
# Each of the FOUR moved producers' live image digest is compared against
# local.globgrph_image_digest as read from infra/aws/terraform/globgrph/serving.tf
# at HEAD. A pin to SOME OTHER digest passes E2-AC1 and fails HERE.
# ASCII only. Git Bash 3.6.7 safe. The aws shim emits CRLF -- stripped before any test.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT/.tools/aws"
SERVING="$ROOT/infra/aws/terraform/globgrph/serving.tf"

# The DECLARED digest, read from the local's own line (never typed in here).
LOCAL_DIGEST="$(sed -n 's/^[[:space:]]*globgrph_image_digest[[:space:]]*=[[:space:]]*"\(sha256:[0-9a-f]*\)".*/\1/p' "$SERVING" | head -1 | tr -d '\r')"
echo "LOCAL_DIGEST_SOURCE=infra/aws/terraform/globgrph/serving.tf (local.globgrph_image_digest)"
echo "LOCAL_DIGEST=$LOCAL_DIGEST"
if [ -z "$LOCAL_DIGEST" ]; then
  echo "ERROR: could not read local.globgrph_image_digest from $SERVING -- refusing to compare against an empty value."
  echo "DIGEST_MATCHES_LOCAL=0 of 4"
  exit 1
fi

PRODUCERS="globgrph-comp-learns-producer globgrph-cse-producer globgrph-fedobs-producer globgrph-resource-summaries-producer"

total=0
match=0
for f in $PRODUCERS; do
  total=$((total + 1))
  img="$("$AWS" ecs describe-task-definition --task-definition "$f" \
        --query 'taskDefinition.containerDefinitions[0].image' \
        --output text 2>&1 | tr -d '\r')"
  live="${img##*@}"
  if [ "$live" = "$LOCAL_DIGEST" ]; then
    verdict="EQUAL"
    match=$((match + 1))
  else
    verdict="DIFFERENT"
  fi
  echo "PRODUCER=$f LIVE_DIGEST=$live -> $verdict"
done

echo "DIGEST_MATCHES_LOCAL=$match of $total"
