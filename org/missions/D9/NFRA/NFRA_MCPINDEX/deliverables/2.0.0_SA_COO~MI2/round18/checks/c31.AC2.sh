#!/usr/bin/env bash
# MX-c-31 AC2 -- see c31_check.py (future).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c31_check.py")" future | tr -d '\r'
exit ${PIPESTATUS[0]}
