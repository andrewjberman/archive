#!/usr/bin/env bash
# OG-rl-15 PHASE A step 3 (baseline): the named failing files of the release run, each in its own process, on a given gateway tree; prints failing ids.
# usage: r29_baseline_files.sh <gateway dir> <out file> <test file>...
GWD="$1"; OUT="$2"; shift 2
export AUDIT_PATH="${TMP:-/tmp}/og_r29_base_audit_$$.jsonl"
: > "$OUT"
cd "$GWD" || exit 9
for f in "$@"; do
  echo "== $f" >> "$OUT"
  timeout 280 python -m pytest "$f" -q -p no:cacheprovider --color=no -rfE 2>&1 | tr -d '\r' | grep -E '^(FAILED|ERROR) |[0-9]+ (passed|failed)' | sed -e 's/ - .*//' | tail -8 >> "$OUT"
done
rm -f "$AUDIT_PATH"
echo DONE >> "$OUT"
