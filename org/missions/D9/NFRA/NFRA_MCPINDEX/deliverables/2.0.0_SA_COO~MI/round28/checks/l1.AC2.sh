#!/usr/bin/env bash
# l1.AC2 -- round 28 (workstream GATEWAY): see l1_check.py. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/l1_check.py" l1.AC2 "$@"
