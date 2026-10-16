#!/usr/bin/env bash
# MX-c-31 AC3 -- see c31_check.py (tests).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c31_check.py")" tests | tr -d '\r'
exit ${PIPESTATUS[0]}
