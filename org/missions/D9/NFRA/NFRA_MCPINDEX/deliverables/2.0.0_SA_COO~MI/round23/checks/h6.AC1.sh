#!/usr/bin/env bash
# h6.AC1 -- round 23 (workstream GATEWAY): see h_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/h_check.py" h6.AC1 "$@"
