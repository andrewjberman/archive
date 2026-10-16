#!/usr/bin/env bash
# MX-c-26 c26.AC3 -- see c26_check.py (ac3).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c26_check.py")" ac3 | tr -d ''
exit ${PIPESTATUS[0]}
