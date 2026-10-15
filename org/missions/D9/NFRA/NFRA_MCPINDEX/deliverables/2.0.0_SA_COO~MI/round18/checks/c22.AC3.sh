#!/usr/bin/env bash
# MX-c-22 c22.AC3 -- see c22_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 290 python "$(native "$D/c22_check.py")" ac3 | tr -d '\r'
exit ${PIPESTATUS[0]}
