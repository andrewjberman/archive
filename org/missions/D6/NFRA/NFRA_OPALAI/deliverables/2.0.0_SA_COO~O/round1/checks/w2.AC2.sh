#!/usr/bin/env bash
# OA-w-2 AC2 (the lane file lands BEFORE any hook): .owned-paths.yaml at HEAD parses and carries at least one lane row
# naming opal_ai/, and NO pre-commit hook is installed in the main tree's opal_ai hooks dir (the install is the COO's act
# at the round's last merge, never a worker's mid-round).
. "$(dirname "$0")/_root.sh"
rows=$(git show HEAD:.owned-paths.yaml 2>/dev/null | python -c "
import sys, yaml
d = yaml.safe_load(sys.stdin.buffer.read().decode('utf-8'))
def walk(x):
    if isinstance(x, dict):
        for v in x.values(): yield from walk(v)
    elif isinstance(x, list):
        for v in x: yield from walk(v)
    elif isinstance(x, str): yield x
print(sum(1 for s in walk(d) if s.startswith('opal_ai/')))" 2>/dev/null || echo PARSE-FAIL)
M=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
GD=$(git -C "$M/opal_ai" rev-parse --absolute-git-dir 2>/dev/null || echo "")
hook=absent; [ -n "$GD" ] && [ -e "$GD/hooks/pre-commit" ] && hook=present
echo "lane-file entries naming opal_ai/: $rows; main-tree opal_ai git dir: ${GD:-(uninitialised)}; pre-commit hook there: $hook"
if [ "$rows" != PARSE-FAIL ] && [ "$rows" -ge 1 ] && [ "$hook" = absent ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
