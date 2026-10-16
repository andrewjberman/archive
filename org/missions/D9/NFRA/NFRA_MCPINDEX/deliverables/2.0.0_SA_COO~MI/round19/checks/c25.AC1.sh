#!/usr/bin/env bash
# MX-c-25 c25.AC1 -- see c25_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c25_check.py")" ac1 | tr -d ''
exit ${PIPESTATUS[0]}
