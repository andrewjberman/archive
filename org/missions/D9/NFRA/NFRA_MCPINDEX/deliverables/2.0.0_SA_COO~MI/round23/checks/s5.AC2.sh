#!/usr/bin/env bash
# s5.AC2 -- round 23 (workstream GATEWAY-TRACE): see h_check.py. Extra arguments (a deliverable file path) are passed through. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/h_check.py" s5.AC2 "$@"
