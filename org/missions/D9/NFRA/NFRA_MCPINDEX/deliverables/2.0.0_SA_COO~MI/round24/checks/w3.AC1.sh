#!/usr/bin/env bash
# w3.AC1 -- round 24 (workstream GATEWAY): see w3_check.py. The argument is the link_fixes.json path. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/w3_check.py" w3.AC1 "$@"
