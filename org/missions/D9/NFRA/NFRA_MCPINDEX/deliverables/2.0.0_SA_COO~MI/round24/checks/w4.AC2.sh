#!/usr/bin/env bash
# w4.AC2 -- round 24 (workstream GATEWAY): see w4_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w4_check.py" w4.AC2 "$@"
