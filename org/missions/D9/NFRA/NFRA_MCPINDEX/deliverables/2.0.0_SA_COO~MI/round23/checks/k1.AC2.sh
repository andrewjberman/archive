#!/usr/bin/env bash
# k1.AC2 -- round 23 (workstream GATEWAY): see h_check.py. Extra arguments (a deliverable file path) are passed through. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/h_check.py" k1.AC2 "$@"
