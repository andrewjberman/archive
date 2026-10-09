#!/usr/bin/env bash
# OPLGTW OG-tg-1 AC2 (bound): the Teams suites read as before -- tests/test_teams_format.py, test_teams_reader_fallback.py
# and test_teams_route.py each pass whole with at least the test functions they had at the cut, none removed or renamed;
# and the identity-scope suites (test_identity_scope.py, test_identity_scope_status_row.py, test_scoped_consent_r253.py)
# pass (rc 0) after the cell updates ONLY the expectations that pinned the concierge's seed or its two overlay rows.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_tg1b_audit_$$.jsonl"
BASE="38f240bdab"
ok=1
for f in tests/test_teams_format.py tests/test_teams_reader_fallback.py tests/test_teams_route.py; do
  out=$(cd "$GW" && timeout 100 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r'); rc=$?
  fl=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
  was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -cE '^[[:space:]]*(async )?def test_')
  now=$(grep -cE '^[[:space:]]*(async )?def test_' "$GW/$f")
  gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -oE '^[[:space:]]*(async )?def test_[A-Za-z0-9_]+' | sed -E 's/^[[:space:]]*(async )?def //' | while read -r t; do grep -qE "^[[:space:]]*(async )?def $t\b" "$GW/$f" || echo "$t"; done | grep -c .)
  echo "$f: pytest rc=$rc ($(printf '%s\n' "$out" | grep -E 'passed|failed|error' | tail -1)); failed/error lines $fl; test functions at the cut $was, now $now, removed or renamed $gone"
  [ "$rc" = 0 ] && [ "$fl" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] && [ "$was" -gt 0 ] || ok=0
done
for f in tests/test_identity_scope.py tests/test_identity_scope_status_row.py tests/test_scoped_consent_r253.py; do
  out=$(cd "$GW" && timeout 100 python -m pytest "$f" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  echo "$f: pytest rc=$rc ($(printf '%s\n' "$out" | grep -E 'passed|failed|error' | tail -1))"
  [ "$rc" = 0 ] || ok=0
done
restore_audit; rm -f "$AUDIT_PATH"
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
