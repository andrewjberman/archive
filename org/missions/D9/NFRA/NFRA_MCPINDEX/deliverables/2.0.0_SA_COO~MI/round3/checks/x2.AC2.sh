#!/usr/bin/env bash
# MX-x-2 AC2 (the reader moves with the section): tests/test_portal_index.py exits 0 with 0 failed/error tests.
. "$(dirname "$0")/_root.sh"
F=tests/test_portal_index.py
[ -f "$GW/$F" ] || { echo "$GW/$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$GW" && timeout 300 python -m pytest "$F" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=$(printf '%s\n' "$out" | grep -cE '^PASSED ')
f=$(printf '%s\n' "$out" | grep -cE '^(FAILED|ERROR) ')
echo "pytest rc=$rc; passed $p; failed/error $f"
if [ "$rc" = 0 ] && [ "$p" -ge 1 ] && [ "$f" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
