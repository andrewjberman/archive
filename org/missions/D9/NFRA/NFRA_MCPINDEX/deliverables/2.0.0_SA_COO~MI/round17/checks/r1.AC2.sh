#!/usr/bin/env bash
# MX-c-20 R1 AC2 -- see r1_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 280 python "$(native "$D/r1_check.py")" ac2 | tr -d '\r'
exit ${PIPESTATUS[0]}
