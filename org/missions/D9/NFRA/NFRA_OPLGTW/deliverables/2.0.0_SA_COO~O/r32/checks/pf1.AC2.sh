#!/usr/bin/env bash
# OPLGTW OG-pf-1 AC2 (bound): tests/test_schwab_query.py, test_admin_grants.py, test_entitlement_admin.py pass whole with
# no test removed or renamed; tests/test_data_entitlement_guard.py fails NO test beyond the base's one (test_ogz1_ac08),
# with test_ogz1_ac07's pinned expectation (a restricted profile denied the non-data tools) moved by the cell as named.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_pf1b_audit_$$.jsonl"
BASE="4ad91ce013"
ok=1
for f in tests/test_schwab_query.py tests/test_admin_grants.py tests/test_entitlement_admin.py; do
  out=$(cd "$GW" && timeout 100 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r'); rc=$?
  fl=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
  was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -cE '^[[:space:]]*(async )?def test_')
  now=$(grep -cE '^[[:space:]]*(async )?def test_' "$GW/$f")
  gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -oE '^[[:space:]]*(async )?def test_[A-Za-z0-9_]+' | sed -E 's/^[[:space:]]*(async )?def //' | while read -r t; do grep -qE "^[[:space:]]*(async )?def $t\b" "$GW/$f" || echo "$t"; done | grep -c .)
  echo "$f: pytest rc=$rc ($(printf '%s\n' "$out" | grep -E 'passed|failed|error' | tail -1)); failed/error lines $fl; test functions at the cut $was, now $now, removed or renamed $gone"
  [ "$rc" = 0 ] && [ "$fl" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] && [ "$was" -gt 0 ] || ok=0
done
f=tests/test_data_entitlement_guard.py
out=$(cd "$GW" && timeout 100 python -m pytest "$f" -q -p no:cacheprovider --color=no -rf 2>&1 | tr -d '\r')
extra=$(printf '%s\n' "$out" | grep -E '^FAILED ' | grep -v 'test_ogz1_ac08' | grep -c .)
echo "$f: $(printf '%s\n' "$out" | grep -E 'passed|failed' | tail -1); failures beyond the base's test_ogz1_ac08: $extra"
[ "$extra" = 0 ] || ok=0
restore_audit; rm -f "$AUDIT_PATH"
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
