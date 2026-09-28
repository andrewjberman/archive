#!/usr/bin/env bash
# OA-e-4 AC3 (bound, C7): against the round-2 nested cut fd8ab8a57f, opal_ai ${OA_NESTED_REF:-HEAD} changes ONLY
# opal/agent/skills/bbg-teams-assist/SKILL.md, and removes at most 3 of its existing lines (the skill's serve steps are
# extended, not rewritten).
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
S="opal/agent/skills/bbg-teams-assist/SKILL.md"
ch=$(git -C opal_ai diff --name-only "$OA_NESTED_PIN" "$REF" 2>&1 | tr -d '\r'); rc=$?
[ $rc -ne 0 ] && { echo "diff failed: $ch"; echo "RESULT: FAIL"; exit 1; }
out=0; for f in $ch; do [ "$f" = "$S" ] || out=$((out+1)); done
rem=$(git -C opal_ai diff -U0 "$OA_NESTED_PIN" "$REF" -- "$S" | tr -d '\r' | grep -cE '^-[^-]')
echo "opal_ai $OA_NESTED_PIN..$REF: files changed other than SKILL.md=$out; SKILL.md lines removed=$rem (max 3)"
if [ "$out" = 0 ] && [ "$rem" -le 3 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
