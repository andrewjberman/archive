#!/usr/bin/env bash
# MX-c-28 c28.AC1 -- see c28_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c28_check.py")" ac1 | tr -d ''
exit ${PIPESTATUS[0]}
