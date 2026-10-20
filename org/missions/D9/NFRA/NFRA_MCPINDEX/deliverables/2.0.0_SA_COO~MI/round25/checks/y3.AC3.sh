#!/usr/bin/env bash
# y3.AC3 -- round 25 (workstream GATEWAY): see y3_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y3_check.py" y3.AC3 "$@"
