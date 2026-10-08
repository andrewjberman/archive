#!/usr/bin/env bash
# OPLGTW OG-cm-1 AC2 (bound): the catalog, query and grant suites read as before, and the two contract copies agree.
# tests/test_schwab_catalog.py, tests/test_schwab_query.py and tests/test_admin_grants.py each pass whole with at least
# the test functions they had at the cut and none deleted or renamed; org/standards/NFRA_OPLGTW_CONTRACT.json and
# infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json are byte-identical.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_cm1b_audit_$$.jsonl"
BASE="713ae4ebba384a652b778f378c31a8416ccfe6b0"
ok=1
for f in tests/test_schwab_catalog.py tests/test_schwab_query.py tests/test_admin_grants.py; do
  out=$(cd "$GW" && timeout 110 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r'); rc=$?
  fl=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
  was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -cE '^(async )?def test_')
  now=$(grep -cE '^(async )?def test_' "$GW/$f")
  gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -oE '^(async )?def test_[A-Za-z0-9_]+' | sed -E 's/^(async )?def //' | while read -r t; do grep -qE "^(async )?def $t\b" "$GW/$f" || echo "$t"; done | grep -c .)
  tail1=$(printf '%s\n' "$out" | grep -E 'passed|failed|error' | tail -1)
  echo "$f: pytest rc=$rc ($tail1); failed/error lines $fl; test functions at the cut $was, now $now, removed or renamed $gone"
  [ "$rc" = 0 ] && [ "$fl" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] && [ "$was" -gt 0 ] || ok=0
done
restore_audit; rm -f "$AUDIT_PATH"
if cmp -s org/standards/NFRA_OPLGTW_CONTRACT.json "$GW/deploy/NFRA_OPLGTW_CONTRACT.json"; then
  echo "contract copies: identical"
else
  echo "contract copies: DIFFER"; ok=0
fi
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
