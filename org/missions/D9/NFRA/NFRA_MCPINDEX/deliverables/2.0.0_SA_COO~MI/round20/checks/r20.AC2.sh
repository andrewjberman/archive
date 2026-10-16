#!/usr/bin/env bash
# MX-r-20 r20.AC2 -- see r20_check.py (ac2). C20_CATALOG names the candidate file (default: the tracked catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/r20_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
