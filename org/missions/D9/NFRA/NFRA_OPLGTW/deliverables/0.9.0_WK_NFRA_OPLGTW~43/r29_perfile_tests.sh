#!/usr/bin/env bash
# OG-rl-15 PHASE A step 3: every test file of a gateway tree in ITS OWN pytest process; one summary line per file.
# usage: r29_perfile_tests.sh <gateway dir> <out file>.  AUDIT_PATH points at a scratch file (never the tracked audit.jsonl).
GWD="$1"; OUT="$2"
export AUDIT_PATH="${TMP:-/tmp}/og_r29_audit_$$.jsonl"
: > "$OUT"
cd "$GWD" || exit 9
n=0
for f in $(ls tests/test_*.py tests/acceptance/test_*.py app/tests/test_*.py 2>/dev/null | sort); do
  n=$((n+1))
  echo "== $f" >> "$OUT"
  timeout 280 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' | grep -E '^(FAILED|ERROR) |passed|failed|error|no tests ran|skipped' | tail -8 >> "$OUT"
  echo "rc=${PIPESTATUS[0]}" >> "$OUT"
done
rm -f "$AUDIT_PATH"
echo "FILES $n" >> "$OUT"
git -C "$GWD" status --short | head -5 >> "$OUT"
echo "DONE" >> "$OUT"
