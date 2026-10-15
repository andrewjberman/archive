#!/usr/bin/env bash
# MX-c-18 T1 AC2 -- see t1_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/t1_check.py")" ac2 | tr -d '\r'
exit ${PIPESTATUS[0]}
