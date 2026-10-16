#!/usr/bin/env bash
# MX-r-20 r20.AC1 -- see r20_check.py (ac1). C20_CATALOG names the candidate file (default: the tracked catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/r20_check.py")" ac1 | tr -d ''
exit ${PIPESTATUS[0]}
