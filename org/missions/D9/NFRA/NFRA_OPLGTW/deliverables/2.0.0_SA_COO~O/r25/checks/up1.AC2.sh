#!/usr/bin/env bash
# OPLGTW OG-up-1 AC2 (the new tool is classified wherever a tool is enumerated, and no grant widened): five gateway test
# files pass with no failure beyond the live baseline r25/UP1_BASELINE.txt, each file in its own process; and
# identity_tool_allowlist.txt is unchanged since live (adding a row is an Andrew ruling, PRD 4.3).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
B="$(cd "$(dirname "$0")/.." && pwd)/UP1_BASELINE.txt"
export AUDIT_PATH="${TMP:-/tmp}/og_r25_up1b_audit_$$.jsonl"
fails=""
for f in tests/test_data_entitlement_guard.py tests/test_tool_classification_composition.py tests/test_principal_cutover.py tests/test_scoped_consent_r253.py tests/test_min_tier_gate.py; do
  if [ ! -f "$GW/$f" ]; then fails="$fails ABSENT::$f"; continue; fi
  o=$(cd "$GW" && timeout 300 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r')
  fails="$fails $(printf '%s\n' "$o" | sed -n 's/^\(FAILED\|ERROR\) \([^ ]*\).*/\2/p' | tr '\n' ' ')"
done
restore_audit; rm -f "$AUDIT_PATH"
new=0; newids=""
for id in $fails; do
  id=$(printf '%s' "$id" | tr '\\' '/')
  if [ -f "$B" ] && grep -qxF "$id" "$B"; then continue; fi
  new=$((new+1)); newids="$newids $id"
done
al=$(git diff --name-only 7d65a28db026a44d7199ffe52a97e44952df75a1 HEAD -- "$GW/identity_tool_allowlist.txt" | grep -c .)
echo "failures beyond the live baseline $new$newids; allowlist file changed since live: $al (want 0)"
[ "$new" = 0 ] && [ "$al" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
