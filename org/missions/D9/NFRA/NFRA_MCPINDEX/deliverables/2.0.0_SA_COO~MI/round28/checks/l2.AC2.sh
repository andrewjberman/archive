#!/usr/bin/env bash
# l2.AC2 -- round 28 (workstream GATEWAY): see l2_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/l2_check.py" l2.AC2 "$@"
