#!/usr/bin/env bash
# MX-c-27 c27.AC2 -- see c27_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 285 python "$(native "$D/c27_check.py")" ac2 | tr -d ''
exit ${PIPESTATUS[0]}
