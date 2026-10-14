#!/usr/bin/env bash
# MX-c-11 AC1 -- see c11_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c11_check.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
