#!/usr/bin/env bash
# MX-s-18 AC3 (hazard disarm): the gold runner's deploy (infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh) can no
# longer delete the runner's engine: every s3 sync whose destination expands to s3://opal-data-bd/code/bronze/ either
# carries no --delete or excludes cot_bronze_ingest.py (grader: s18_sync.py beside this file).
G="$(cd "$(dirname "$0")" && pwd)/s18_sync.py"
. "$(dirname "$0")/_root.sh"
out=$(python "$(native "$G")" infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
