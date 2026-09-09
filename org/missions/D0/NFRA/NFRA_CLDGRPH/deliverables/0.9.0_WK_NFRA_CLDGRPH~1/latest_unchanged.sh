#!/usr/bin/env bash
# E2-AC4 -- NO IMAGE MOVED (the cell's bound: a pin is a task-definition revision and
# nothing else moves). The ECR ':latest' digest recorded BEFORE the first act of this
# order (latest_digest_before.txt, written at step 1, before the ledger, before any edit)
# is compared against the digest read NOW. This control CAN fail: a rebuild, a push or a
# re-tag between the two reads moves the tag and prints false.
# ASCII only. Git Bash 3.6.7 safe. The aws shim emits CRLF -- stripped before any test.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT/.tools/aws"
BEFORE_FILE="$ROOT/org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/latest_digest_before.txt"

if [ ! -f "$BEFORE_FILE" ]; then
  echo "ERROR: $BEFORE_FILE absent -- there is no BEFORE reading to compare against."
  echo "LATEST_DIGEST_UNCHANGED=unreadable"
  exit 1
fi
BEFORE="$(tr -d '\r\n' < "$BEFORE_FILE")"

AFTER="$("$AWS" ecr describe-images --repository-name opal-globgrph-derive-runner \
        --image-ids imageTag=latest --query 'imageDetails[0].imageDigest' \
        --output text 2>&1 | tr -d '\r')"

echo "REPOSITORY=opal-globgrph-derive-runner TAG=latest"
echo "BEFORE=$BEFORE  (read before this order's first act, from $BEFORE_FILE)"
echo "AFTER=$AFTER   (read live now)"

if [ -n "$BEFORE" ] && [ "$BEFORE" = "$AFTER" ]; then
  echo "LATEST_DIGEST_UNCHANGED=true"
else
  echo "LATEST_DIGEST_UNCHANGED=false"
fi
