#!/usr/bin/env bash
# OPLGTW OG-md-1 AC2 (PRD v1.9 acceptance 3): v1.4 reads as before. The two existing mail test files pass whole, with at
# least the counts they had before this cell (tests/test_mail_route.py 11, tests/test_mail_listing.py as counted at
# the cut), and no test of either file was deleted or renamed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r31_md1b_audit_$$.jsonl"
BASE="4c0f314e864cc4bd84401f8effcce8cf1f8c71e9"
tot=0; ok=1
for f in tests/test_mail_route.py tests/test_mail_listing.py; do
  out=$(cd "$GW" && timeout 200 python -m pytest "$f" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  p=$(printf '%s\n' "$out" | grep -cE ' PASSED'); fl=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
  was=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -cE '^(async )?def test_')
  now=$(grep -cE '^(async )?def test_' "$GW/$f")
  gone=$(MSYS_NO_PATHCONV=1 git show "$BASE:$GW/$f" | grep -oE '^(async )?def test_[A-Za-z0-9_]+' | sed -E 's/^(async )?def //' | while read -r t; do grep -qE "^(async )?def $t\b" "$GW/$f" || echo "$t"; done | grep -c .)
  echo "$f: pytest rc=$rc passed $p failed/error $fl; test functions at the cut $was, now $now, removed or renamed $gone"
  [ "$rc" = 0 ] && [ "$fl" = 0 ] && [ "$gone" = 0 ] && [ "$now" -ge "$was" ] || ok=0
  tot=$((tot+p))
done
restore_audit; rm -f "$AUDIT_PATH"
echo "v1.4 mail tests passed in all: $tot"
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
