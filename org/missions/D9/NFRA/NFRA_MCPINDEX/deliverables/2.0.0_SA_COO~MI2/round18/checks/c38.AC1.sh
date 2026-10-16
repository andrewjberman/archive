#!/usr/bin/env bash
# MX-c-38 AC1 -- see c38_check.py (scope).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 115 python "$(native "$D/c38_check.py")" scope | tr -d '\r'
exit ${PIPESTATUS[0]}
