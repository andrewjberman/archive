#!/usr/bin/env bash
# w5.AC2 -- round 24 (workstream GATEWAY): see w5_check.py. The argument is the deliverable path (relative to the repository root). Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/../../round23/checks/_root.sh"
python "$H/w5_check.py" w5.AC2 "$@"
