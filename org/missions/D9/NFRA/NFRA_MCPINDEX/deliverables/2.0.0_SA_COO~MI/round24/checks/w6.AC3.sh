#!/usr/bin/env bash
# w6.AC3 -- round 24 (workstream GATEWAY): see w6_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w6_check.py" w6.AC3 "$@"
