#!/usr/bin/env bash
# MX-i-5 AC1 (R-15 (a)): the 4 dead-leg EventBridge rules read DISABLED 4 of 4 LIVE, and the live REST leg bd-asset-dim-pipeline-trigger still reads ENABLED (the negative control).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; d=0
for r in bd-allocation-pipeline-trigger bd-realized-pipeline-trigger bd-transaction-pipeline-trigger bd-unrealized-pipeline-trigger; do s=$(timeout 40 "$AWS" events describe-rule --name "$r" --query State --output text 2>&1 | tr -d '\r'); echo "  $r: $s"; [ "$s" = DISABLED ] && d=$((d+1)); done
c=$(timeout 40 "$AWS" events describe-rule --name bd-asset-dim-pipeline-trigger --query State --output text 2>&1 | tr -d '\r')
echo "dead-leg rules DISABLED $d of 4; negative control bd-asset-dim-pipeline-trigger=$c"
rc=1; [ "$d" = 4 ] && [ "$c" = ENABLED ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
