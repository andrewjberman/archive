#!/usr/bin/env bash
# g2.AC2 -- round 22 (workstream GATEWAY): see g_check.py. Run from anywhere inside the worktree; prints RESULT: PASS|FAIL, exits 0 on PASS.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/g_check.py" g2.AC2
