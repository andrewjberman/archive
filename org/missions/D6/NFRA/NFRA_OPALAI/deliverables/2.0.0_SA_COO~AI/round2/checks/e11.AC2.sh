#!/usr/bin/env bash
# OA-e-11 AC2 (the cell's own regression test is committed and green): .tools/tests/test_nested_worktree_failclosed.sh
# exists at HEAD and runs to a zero-failure summary. A test file that is absent, or that reports any failure, fails.
. "$(dirname "$0")/_root.sh"
T=".tools/tests/test_nested_worktree_failclosed.sh"
if ! git cat-file -e "HEAD:$T" 2>/dev/null; then echo "test at HEAD=absent"; echo "RESULT: FAIL"; exit 1; fi
out=$(timeout 110 bash "$T" 2>&1 | tr -d '\r'); rc=$?
last=$(printf '%s\n' "$out" | grep -E 'passed|failed|PASS|FAIL' | tail -1)
fails=$(printf '%s\n' "$out" | grep -cE '^(FAIL|not ok)')
echo "test at HEAD=present; rc=$rc; failing lines=$fails; summary: ${last:-none}"
if [ "$rc" = 0 ] && [ "$fails" = 0 ] && [ -n "$last" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
