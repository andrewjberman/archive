#!/usr/bin/env bash
# OPLGTW OG-rf-1 AC2 (bound): the durable OAuth suite reads as before. tests/test_oauth_durable.py passes whole: its
# summary line reports at least as many passed as it has test functions, none failed or errored, and none of the test
# functions it had at the cut was deleted or renamed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_rf1b_audit_$$.jsonl"
BASE="713ae4ebba384a652b778f378c31a8416ccfe6b0"
ok=1
for f in tests/test_oauth_durable.py; do
  out=$(cd "$GW" && timeout 110 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r'); rc=$?
  summary=$(printf '%s\n' "$out" | grep -E '[0-9]+ passed|failed|error' | tail -1)
  p=$(printf '%s\n' "$summary" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); p=${p:-0}
  fl=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
  was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -cE '^(async )?def test_')
  now=$(grep -cE '^(async )?def test_' "$GW/$f")
  gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -oE '^(async )?def test_[A-Za-z0-9_]+' | sed -E 's/^(async )?def //' | while read -r t; do grep -qE "^(async )?def $t\b" "$GW/$f" || echo "$t"; done | grep -c .)
  echo "$f: pytest rc=$rc passed $p ($summary); failed/error lines $fl; test functions at the cut $was, now $now, removed or renamed $gone"
  [ "$rc" = 0 ] && [ "$fl" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] && [ "$was" -gt 0 ] && [ "$p" -ge "$was" ] || ok=0
done
restore_audit; rm -f "$AUDIT_PATH"
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
