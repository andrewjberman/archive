#!/usr/bin/env bash
# k6.AC1 -- round 23 (workstream GATEWAY): see h_check.py. Extra arguments (a deliverable file path) are passed through. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/h_check.py" k6.AC1 "$@"
