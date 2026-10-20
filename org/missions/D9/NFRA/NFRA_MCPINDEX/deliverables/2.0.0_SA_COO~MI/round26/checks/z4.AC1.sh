#!/usr/bin/env bash
# z4.AC1 -- round 26 (workstream GATEWAY): see z4_check.py. The argument is the deliverable path (relative to the repository root). Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/../../round23/checks/_root.sh"
python "$H/z4_check.py" z4.AC1 "$@"
