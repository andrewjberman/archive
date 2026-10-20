#!/usr/bin/env bash
# y6.AC3 -- round 25 (workstream GATEWAY): see y6_check.py. Optional env Y6_PKG_DIR names the folder holding cheatsheet.py and tests/. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/y6_check.py" y6.AC3 "$@"
