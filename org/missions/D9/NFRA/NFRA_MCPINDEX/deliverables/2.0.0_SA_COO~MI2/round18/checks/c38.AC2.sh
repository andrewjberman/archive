#!/usr/bin/env bash
# MX-c-38 AC2 -- see c38_check.py (tests).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c38_check.py")" tests | tr -d '\r'
exit ${PIPESTATUS[0]}
