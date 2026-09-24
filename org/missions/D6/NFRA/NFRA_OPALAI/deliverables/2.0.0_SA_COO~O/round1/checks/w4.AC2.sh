#!/usr/bin/env bash
# OA-w-4 AC2 (built): activity-check.py's header line names the repos it read -- "repos: parent=N opal_ai=M portal=..."
# -- with opal_ai >= 1 in this worktree; an uninitialised mapped submodule reads UNINITIALISED, never 0.
. "$(dirname "$0")/_root.sh"
h=$(timeout 100 python .tools/activity-check.py --days 30 2>&1 | tr -d '\r' | grep -m1 -oE 'repos: .*' || echo "(no repos: field)")
echo "$h"
o=$(printf '%s' "$h" | sed -n 's/.*opal_ai=\([0-9]*\).*/\1/p')
if [ -n "$o" ] && [ "$o" -ge 1 ] && printf '%s' "$h" | grep -Eq 'portal=(UNINITIALISED|[0-9]+)'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
