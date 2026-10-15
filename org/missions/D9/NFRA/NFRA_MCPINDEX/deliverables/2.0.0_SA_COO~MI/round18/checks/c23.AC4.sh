#!/usr/bin/env bash
# MX-c-23 c23.AC4 -- see c23_check.py (ac4).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c23_check.py")" ac4 | tr -d '\r'
exit ${PIPESTATUS[0]}
