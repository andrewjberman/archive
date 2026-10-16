#!/usr/bin/env bash
# MX-c-26 c26.AC2 -- see c26_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c26_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
