#!/usr/bin/env bash
# MX-c-24 c24.AC1 -- see c24_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c24_check.py")" ac1 | tr -d ''
exit ${PIPESTATUS[0]}
