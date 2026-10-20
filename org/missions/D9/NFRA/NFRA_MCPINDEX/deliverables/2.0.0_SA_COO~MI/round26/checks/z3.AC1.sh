#!/usr/bin/env bash
# z3.AC1 -- round 26 (workstream GATEWAY): see z3_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/z3_check.py" z3.AC1 "$@"
