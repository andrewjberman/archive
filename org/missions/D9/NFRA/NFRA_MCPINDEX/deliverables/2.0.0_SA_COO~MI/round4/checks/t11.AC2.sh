#!/usr/bin/env bash
# t11 AC2 (the reader and its tests): tests/test_portal_index.py exits 0 with 0 failed/error tests and more passing tests than the round-3 baseline of 7.
. "$(dirname "$0")/_root.sh"
F=tests/test_portal_index.py; out=$(cd "$GW" && timeout 300 python -m pytest "$F" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r=$?
p=$(printf '%s\n' "$out" | grep -cE '^PASSED '); f=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "pytest rc=$r; passed $p; failed/error $f"
rc=1; [ "$r" = 0 ] && [ "$p" -gt 7 ] && [ "$f" = 0 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
