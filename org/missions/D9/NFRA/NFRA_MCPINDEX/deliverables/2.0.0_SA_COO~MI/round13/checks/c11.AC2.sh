#!/usr/bin/env bash
# MX-c-11 AC2 -- see c11_check.py (ac2).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c11_check.py")" ac2 | tr -d '\r'
exit ${PIPESTATUS[0]}
