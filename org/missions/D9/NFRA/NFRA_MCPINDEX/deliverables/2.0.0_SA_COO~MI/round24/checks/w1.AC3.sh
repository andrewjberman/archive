#!/usr/bin/env bash
# w1.AC3 -- round 24 (workstream GATEWAY): see w1_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w1_check.py" w1.AC3 "$@"
