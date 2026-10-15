#!/usr/bin/env bash
# MX-c-30 AC2 -- see c30_check.py (tests).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 280 python "$(native "$D/c30_check.py")" tests | tr -d '\r'
exit ${PIPESTATUS[0]}
