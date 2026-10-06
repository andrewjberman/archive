#!/usr/bin/env bash
# OPLGTW OG-q-8 AC2 (R30.1, the existing qualify tests stay green): the two existing dim_asset test files pass WHOLE,
# each in its own process -- tests/test_schwab_q7_asset_download.py and tests/test_schwab_rl5_asset_query.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r23_q8b_audit_$$.jsonl"
ok=0; n=0
for f in tests/test_schwab_q7_asset_download.py tests/test_schwab_rl5_asset_query.py; do
  n=$((n+1))
  o=$(cd "$GW" && timeout 300 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  bad=$(printf '%s\n' "$o" | grep -cE '[0-9]+ (failed|error)')
  [ "$rc" = 0 ] && [ "$bad" = 0 ] && ok=$((ok+1))
  echo "$f: rc=$rc; $(printf '%s\n' "$o" | grep -E '(passed|failed|error)' | tail -1)"
done
restore_audit; rm -f "$AUDIT_PATH"
echo "existing asset test files green $ok of $n"
[ "$ok" = "$n" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
