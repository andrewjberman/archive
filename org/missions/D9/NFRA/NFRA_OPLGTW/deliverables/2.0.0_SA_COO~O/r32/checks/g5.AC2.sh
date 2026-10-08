#!/usr/bin/env bash
# OPLGTW OG-g5-1 AC2 (bound): the list-only run changed nothing that lands or runs.
#  (a) no object exists under s3://opal-data-assets/schwab/08403355/ (nothing landed);
#  (b) the scheduled puller's code object is the bytes it was at the cut (ETag 0017f9b549ca9f8013704f50c4327bed);
#  (c) no tracked file under the puller's directory or the two Schwab Terraform roots differs from the cut.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="713ae4ebba384a652b778f378c31a8416ccfe6b0"
ok=1
kc=$(.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix schwab/08403355/ --max-keys 1 --query KeyCount --output text | tr -d '\r'); rc=$?
echo "(a) objects under schwab/08403355/: KeyCount=$kc (aws rc=$rc)"
[ "$rc" = 0 ] && [ "$kc" = 0 ] || ok=0
et=$(.tools/aws s3api head-object --bucket opal-data-assets --key code/canonical-schwab-si2/sdd-daily-pull.ps1 --query ETag --output text | tr -d '\r"'); rc=$?
echo "(b) code object ETag=$et (aws rc=$rc), cut 0017f9b549ca9f8013704f50c4327bed"
[ "$rc" = 0 ] && [ "$et" = 0017f9b549ca9f8013704f50c4327bed ] || ok=0
changed=$(git diff --name-only "$BASE" -- infra/aws/ec2/canonical-schwab-si2 infra/aws/terraform/canonical-schwab-ec2 infra/aws/terraform/canonical-schwab-si2-schedule | grep -c .)
echo "(c) tracked files changed since the cut under the puller and its two Terraform roots: $changed"
[ "$changed" = 0 ] || ok=0
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
