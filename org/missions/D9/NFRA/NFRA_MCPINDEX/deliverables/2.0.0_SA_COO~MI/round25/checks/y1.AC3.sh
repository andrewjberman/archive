#!/usr/bin/env bash
# y1.AC3 -- round 25 (workstream GATEWAY): see y1_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y1_check.py" y1.AC3 "$@"
