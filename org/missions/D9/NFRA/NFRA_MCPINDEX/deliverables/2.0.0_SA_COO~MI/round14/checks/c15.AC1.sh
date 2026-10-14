#!/usr/bin/env bash
# MX-c-15 AC1 -- see c15_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c15_check.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
