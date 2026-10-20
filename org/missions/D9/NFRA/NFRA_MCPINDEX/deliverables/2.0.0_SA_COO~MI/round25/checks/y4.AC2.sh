#!/usr/bin/env bash
# y4.AC2 -- round 25 (workstream GATEWAY): see y4_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y4_check.py" y4.AC2 "$@"
