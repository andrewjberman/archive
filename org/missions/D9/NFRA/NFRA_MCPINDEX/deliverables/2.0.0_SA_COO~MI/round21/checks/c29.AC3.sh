#!/usr/bin/env bash
# MX-c-29 c29.AC3 -- see c29_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c29_check.py")" ac3 | tr -d ''
exit ${PIPESTATUS[0]}
