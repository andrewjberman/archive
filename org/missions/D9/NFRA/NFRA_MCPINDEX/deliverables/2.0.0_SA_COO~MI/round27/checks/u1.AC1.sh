#!/usr/bin/env bash
# u1.AC1 -- round 27 (workstream GATEWAY): see u1_check.py. The argument is the deliverable path (relative to the repository root). Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/u1_check.py" u1.AC1 "$@"
