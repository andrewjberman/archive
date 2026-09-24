#!/usr/bin/env bash
# OA-w-2 AC1 (built, with its own difference arms): the worker's fixture test builds a SCRATCH superproject + nested repo
# (never the shared opal_ai) and shows four arms:
#   nested-granted-pass         a commit inside the nested repo, on a path the parent lane file grants, PASSes the hook
#   nested-violation-block      the same commit on a path the lane file does not grant is BLOCKed
#   safe-commit-nested-landed   .tools/safe-commit.sh run from inside the nested repo lands a commit (rc 0, git log shows it)
#   parent-unchanged            in the fixture's parent, a granted commit PASSes and a violation BLOCKs, as before
. "$(dirname "$0")/_root.sh"
F=".tools/tests/test_nested_repo_gates.sh"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 bash "$F" 2>&1 | tr -d '\r'); rc=$?
n=0; for a in nested-granted-pass nested-violation-block safe-commit-nested-landed parent-unchanged; do
  printf '%s\n' "$out" | grep -E "^ok +\[?$a\]?" >/dev/null && n=$((n+1)); done
sum=$(printf '%s\n' "$out" | grep -m1 '^ARMS: ' || echo "(no ARMS line)")
echo "rc=$rc; named arms ok $n of 4; $sum"
if [ "$rc" = 0 ] && [ "$n" = 4 ] && [ "$sum" = "ARMS: 4 of 4 PASS" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
