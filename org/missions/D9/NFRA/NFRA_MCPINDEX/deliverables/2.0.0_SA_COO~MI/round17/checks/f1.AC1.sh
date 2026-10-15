#!/usr/bin/env bash
# MX-c-19 F1 AC1 -- see f1_check.py (ac1).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 290 python "$(native "$D/f1_check.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
