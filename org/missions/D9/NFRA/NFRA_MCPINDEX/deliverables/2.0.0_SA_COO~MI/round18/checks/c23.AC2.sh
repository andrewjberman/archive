#!/usr/bin/env bash
# MX-c-23 c23.AC2 -- see c23_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c23_check.py")" ac2 | tr -d '\r'
exit ${PIPESTATUS[0]}
