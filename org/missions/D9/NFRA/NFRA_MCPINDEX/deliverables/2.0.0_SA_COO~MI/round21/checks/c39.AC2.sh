#!/usr/bin/env bash
# MX-c-39 c39.AC2 -- see c39_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c39_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
