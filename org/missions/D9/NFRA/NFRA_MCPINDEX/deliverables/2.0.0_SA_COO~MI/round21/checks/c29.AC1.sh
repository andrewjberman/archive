#!/usr/bin/env bash
# MX-c-29 c29.AC1 -- see c29_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c29_check.py")" ac1 | tr -d ''
exit ${PIPESTATUS[0]}
