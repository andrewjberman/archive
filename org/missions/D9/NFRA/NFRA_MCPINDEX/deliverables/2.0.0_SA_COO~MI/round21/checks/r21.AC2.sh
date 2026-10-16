#!/usr/bin/env bash
# MX-r-21 r21.AC2 -- see r21_check.py (ac2). C21_CATALOG names the candidate file (default: the tracked catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/r21_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
