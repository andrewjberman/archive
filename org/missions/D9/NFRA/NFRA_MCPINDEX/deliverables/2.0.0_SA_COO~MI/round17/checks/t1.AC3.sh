#!/usr/bin/env bash
# MX-c-18 T1 AC3 -- see t1_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/t1_check.py")" ac3 | tr -d '\r'
exit ${PIPESTATUS[0]}
