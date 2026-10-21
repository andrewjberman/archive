#!/usr/bin/env bash
# u2.AC2 -- round 27 (workstream GATEWAY): see u2_check.py. Argument: the deliverable path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/u2_check.py" u2.AC2 "$@"
