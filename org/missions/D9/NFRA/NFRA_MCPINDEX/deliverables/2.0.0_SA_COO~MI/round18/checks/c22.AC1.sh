#!/usr/bin/env bash
# MX-c-22 c22.AC1 -- see c22_equal.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c22_equal.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
