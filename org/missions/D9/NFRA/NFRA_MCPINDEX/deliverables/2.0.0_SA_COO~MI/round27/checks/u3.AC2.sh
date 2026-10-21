#!/usr/bin/env bash
# u3.AC2 -- round 27 (workstream GATEWAY): see u3_check.py. Optional env U3_PKG_DIR names the folder holding cheatsheet.py and tests/. Prints RESULT: PASS|FAIL.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
python "$H/u3_check.py" u3.AC2 "$@"
