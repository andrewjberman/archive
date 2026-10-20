#!/usr/bin/env bash
# w2.AC2 -- round 24 (workstream GATEWAY): see w2_check.py. Extra arguments (the plan file path) are passed through. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w2_check.py" w2.AC2 "$@"
