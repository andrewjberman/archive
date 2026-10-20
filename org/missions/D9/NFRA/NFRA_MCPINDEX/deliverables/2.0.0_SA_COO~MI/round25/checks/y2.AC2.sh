#!/usr/bin/env bash
# y2.AC2 -- round 25 (workstream GATEWAY): see y2_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y2_check.py" y2.AC2 "$@"
