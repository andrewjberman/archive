#!/usr/bin/env bash
# MP-x-3 AC3 (DECLARED: R3's text carves out exactly the two prefixes, citing the ruling): graph-read.tf names both
# prefixes and the ruling (laptop 1.0.0_SA_CTO msg 107359, relayed as msg 32030), and the new file
# mcportal_fabric_read.tf exists and cites the same ruling.
. "$(dirname "$0")/_root.sh"
G=infra/aws/terraform/opal-gateway/graph-read.tf; N=infra/aws/terraform/opal-gateway/mcportal_fabric_read.tf
[ -f "$N" ] || { echo "$N absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for f in "$G" "$N"; do for t in "fabric/activity/v1/" "fabric/open-calls/v1/" "107359"; do
  if grep -qF -- "$t" "$f"; then n=$((n+1)); else echo "  $f lacks $t"; fi; done; done
echo "carve-out tokens present $n of 6"
if [ "$n" = 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
