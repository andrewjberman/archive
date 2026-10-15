#!/usr/bin/env bash
# MX-c-16 AC1 -- see c16_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c16_check.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
