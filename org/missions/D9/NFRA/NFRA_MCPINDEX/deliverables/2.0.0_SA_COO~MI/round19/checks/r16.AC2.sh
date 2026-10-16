#!/usr/bin/env bash
# MX-r-16 r16.AC2 -- see r16_check.py (ac2). C16_CATALOG names the candidate file (default: the tracked catalog).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/r16_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
