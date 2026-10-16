#!/usr/bin/env bash
# OPLGTW OG-ng-2 AC3 (round-37, XA-20261016T034740Z-28da): the diff is limited to .tools/naming-gate.py (its selftest lives in the file) and, if wanted, one new .tools/tests/test_naming_gate_rulings.py. Anything else outside org/ is a defect.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
# the fork point of the worker's branch from trunk (box/sitez): run this from the worker's worktree
BASE=$(git merge-base HEAD box/sitez | tr -d '')
git cat-file -e "${BASE}^{commit}" || { echo "base $BASE absent"; echo "RESULT: FAIL"; exit 1; }
files=$(git diff --name-only "$BASE" HEAD -- . ':(exclude)org/' | tr -d '\r')
n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE '^\.tools/(naming-gate\.py|tests/test_naming_gate_rulings\.py)$' | grep -c .)
touched=$(printf '%s\n' "$files" | grep -c '^\.tools/naming-gate\.py$')
echo "files differing from the base outside org/: $n; outside the allowed two files: $outside (want 0); naming-gate.py changed: $touched (want 1)"
[ "$outside" = 0 ] && [ "$touched" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
