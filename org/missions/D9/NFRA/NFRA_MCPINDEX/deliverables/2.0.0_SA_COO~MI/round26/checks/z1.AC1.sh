#!/usr/bin/env bash
# z1.AC1 -- round 26 (workstream GATEWAY): see z1_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/z1_check.py" z1.AC1 "$@"
