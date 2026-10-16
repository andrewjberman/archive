#!/usr/bin/env bash
# c40 landed -- see c40_check.py (landed).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c40_check.py")" landed | tr -d '\r'
exit ${PIPESTATUS[0]}
