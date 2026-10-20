#!/usr/bin/env bash
# y5.AC2 -- round 25 (workstream GATEWAY): see y5_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y5_check.py" y5.AC2 "$@"
