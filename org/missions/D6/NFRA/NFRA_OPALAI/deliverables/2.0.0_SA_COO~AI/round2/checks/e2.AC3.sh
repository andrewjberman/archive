#!/usr/bin/env bash
# OA-e-2 AC3 (bound, C7): against the round-2 nested cut fd8ab8a57f, opal_ai ${OA_NESTED_REF:-HEAD} changes ONLY the
# cell's three files (opal/agent/hooks/concierge-gate.sh, opal/agent/hooks/test_concierge_gate.sh,
# opal/agent/refs/RELAUNCH.md): prompt.md (its hard lines), REQUEST_CATALOG.md and every other file are byte-unchanged.
# The fence's G1-G3 blocks are unchanged too: the lines of concierge-gate.sh outside the G4 case that the diff REMOVES
# number 0 (only additions are allowed outside G4).
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
ALLOW="opal/agent/hooks/concierge-gate.sh opal/agent/hooks/test_concierge_gate.sh opal/agent/refs/RELAUNCH.md"
ch=$(git -C opal_ai diff --name-only "$OA_NESTED_PIN" "$REF" 2>&1 | tr -d '\r'); rc=$?
[ $rc -ne 0 ] && { echo "diff failed: $ch"; echo "RESULT: FAIL"; exit 1; }
n=$(printf '%s\n' "$ch" | grep -c .)
out=0; for f in $ch; do case " $ALLOW " in *" $f "*) ;; *) out=$((out+1));; esac; done
rem=$(git -C opal_ai diff -U0 "$OA_NESTED_PIN" "$REF" -- opal/agent/hooks/concierge-gate.sh | tr -d '\r' | grep -E '^-[^-]' | grep -vc 'G4\|opal-gateway-bbg__')
echo "opal_ai $OA_NESTED_PIN..$REF: files changed=$n, outside the cell's three=$out; fence lines removed outside G4=$rem"
if [ "$out" = 0 ] && [ "$rem" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
