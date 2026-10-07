#!/usr/bin/env bash
# OPLGTW OG-hg-1 AC2 (the gate's existing behaviour holds): .tools/halt-gate-ld0131-test.sh still exits 0, and
# .tools/test-haltgt-recipient-scoping.sh fails no more cases than its pre-cut baseline. That script read
# "0 passed, 9 failed" at the cut in the issuer's worktree AND in the shared tree (2026-10-07 ~02:5xZ), so its baseline
# is 9 failed; a lower number is welcome and a higher one is a regression.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE_FAILED=9
timeout 250 bash .tools/halt-gate-ld0131-test.sh >/dev/null 2>&1; r1=$?
out=$(timeout 250 bash .tools/test-haltgt-recipient-scoping.sh 2>&1 | tr -d '\r')
line=$(printf '%s\n' "$out" | grep -E '^RESULT: [0-9]+ passed, [0-9]+ failed' | tail -1)
failed=$(printf '%s\n' "$line" | sed -n 's/^RESULT: [0-9]* passed, \([0-9]*\) failed.*/\1/p')
echo "halt-gate-ld0131-test rc=$r1; recipient-scoping ${line:-NO RESULT LINE} (baseline failed $BASE_FAILED)"
[ "$r1" = 0 ] && [ -n "$failed" ] && [ "$failed" -le "$BASE_FAILED" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
