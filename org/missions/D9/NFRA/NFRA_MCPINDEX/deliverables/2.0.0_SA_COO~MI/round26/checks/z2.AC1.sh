#!/usr/bin/env bash
# z2.AC1 -- round 26 (workstream GATEWAY): see z2_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/z2_check.py" z2.AC1 "$@"
