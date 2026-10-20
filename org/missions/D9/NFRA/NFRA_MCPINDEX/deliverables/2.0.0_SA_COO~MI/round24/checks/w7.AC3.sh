#!/usr/bin/env bash
# w7.AC3 -- round 24 (workstream GATEWAY): see w7_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w7_check.py" w7.AC3 "$@"
