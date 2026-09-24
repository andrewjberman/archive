#!/usr/bin/env bash
# OA-w-4 AC1 (built + bound): fabric-commits.py --json --days 30 carries by_repo -- the parent repo's count, and one
# entry per MAPPED submodule: a count when initialised, the string "UNINITIALISED" when not (never a silent 0). opal_ai
# (initialised in this worktree, holding 0.0.0_AB_MSTR~Z's 2026-09-24 init commit) counts >= 1. Bound: the parent count
# sits between two direct `git log` counts taken just before and just after (commits land continuously on this tree).
. "$(dirname "$0")/_root.sh"
b=$(git log --since="30 days ago" --no-merges --oneline | wc -l | tr -d ' ')
j=$(timeout 100 python .tools/fabric-commits.py --json --days 30 2>&1)
a=$(git log --since="30 days ago" --no-merges --oneline | wc -l | tr -d ' ')
r=$(printf '%s' "$j" | python -c "
import json, sys
d = json.loads(sys.stdin.read()).get('by_repo')
if not isinstance(d, dict): print('NO-BY_REPO'); sys.exit()
print('parent=%s opal_ai=%s portal=%s' % (d.get('parent'), d.get('opal_ai'), d.get('portal')))" 2>&1 | tail -1)
echo "direct parent count before=$b after=$a; tool: $r"
p=$(printf '%s' "$r" | sed -n 's/.*parent=\([0-9]*\).*/\1/p'); o=$(printf '%s' "$r" | sed -n 's/.*opal_ai=\([0-9]*\).*/\1/p')
pt=$(printf '%s' "$r" | sed -n 's/.*portal=\([^ ]*\).*/\1/p')
if [ -n "$p" ] && [ "$p" -ge "$b" ] && [ "$p" -le "$a" ] && [ -n "$o" ] && [ "$o" -ge 1 ] \
   && { [ "$pt" = UNINITIALISED ] || printf '%s' "$pt" | grep -Eq '^[0-9]+$'; }; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
