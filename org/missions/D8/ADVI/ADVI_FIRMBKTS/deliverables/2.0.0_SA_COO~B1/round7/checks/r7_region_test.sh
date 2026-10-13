#!/bin/bash
# ADVI_FIRMBKTS round 7, FB-j-4: the dispatcher's put-events call takes its region from ONE variable, EVENTS_REGION, and nothing
# else in the script changes how a region resolves (the CTO's ruling, ROUND_ANALYSIS.round6.md ADDENDUM 1 item 2: NOT a global export).
# usage: bash r7_region_test.sh <path to gold_dispatch.sh>
# Prints a last line `REGION TEST: <n> of 3 arms`. No network, no AWS call. Issuer-owned; never edit.
SCRIPT="$1"
if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then echo "REGION TEST: 0 of 3 arms (script not found)"; exit 1; fi
PASS=0
ASSIGN=$(grep -n '^[[:space:]]*EVENTS_REGION=' "$SCRIPT" | head -5)
NASSIGN=$(grep -c '^[[:space:]]*EVENTS_REGION=' "$SCRIPT")
if [ "$NASSIGN" = "1" ] && printf '%s' "$ASSIGN" | grep -q 'EVENTS_REGION="\${EVENTS_REGION:-[a-z0-9-]*}"'; then
  echo "PASS R1 exactly one EVENTS_REGION assignment, an overridable default"; PASS=$((PASS+1))
else
  echo "FAIL R1 exactly one EVENTS_REGION assignment, an overridable default (count=$NASSIGN)"
fi
NREG=$(grep -c -- '--region' "$SCRIPT")
if grep -q 'aws events put-events[^|]*--region "\$EVENTS_REGION"' "$SCRIPT" && [ "$NREG" = "1" ]; then
  echo "PASS R2 the put-events call carries --region \"\$EVENTS_REGION\" and no other call in the script names a region"; PASS=$((PASS+1))
else
  echo "FAIL R2 the put-events call carries --region \"\$EVENTS_REGION\" and no other call in the script names a region (--region lines=$NREG)"
fi
if ! grep -q 'AWS_DEFAULT_REGION\|AWS_REGION' "$SCRIPT"; then
  echo "PASS R3 no global region export (AWS_DEFAULT_REGION and AWS_REGION are absent)"; PASS=$((PASS+1))
else
  echo "FAIL R3 no global region export (AWS_DEFAULT_REGION or AWS_REGION present)"
fi
echo "REGION TEST: $PASS of 3 arms"
[ "$PASS" = "3" ]
