#!/usr/bin/env bash
# MP-pd-2 AC2 (F2, the writer; the bound): the Lambda's whole test directory still passes. The base reads 24 passed, 0 failed
# (measured 2026-10-14 ~18:0xZ); the new file adds at least 7, so the run must read 0 failed and at least 31 passed.
. "$(dirname "$0")/_root.sh"
out=$(cd "$LAM" && timeout 115 python -m pytest tests -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
pass=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' | head -1); pass=${pass:-0}
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "writer suite: $tail; passed=$pass failed=$failed"
if [ "$failed" = 0 ] && [ "$pass" -ge 31 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
