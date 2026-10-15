#!/usr/bin/env bash
# MX-c-21 c21.AC3 -- see c21_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 290 python "$(native "$D/c21_check.py")" ac3 | tr -d '\r'
exit ${PIPESTATUS[0]}
