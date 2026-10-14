#!/usr/bin/env bash
# MX-c-13 AC3 -- see c13_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c13_check.py")" ac3 | tr -d '\r'
exit ${PIPESTATUS[0]}
