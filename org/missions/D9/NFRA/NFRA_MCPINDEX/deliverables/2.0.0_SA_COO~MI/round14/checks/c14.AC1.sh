#!/usr/bin/env bash
# MX-c-14 AC1 -- see c14_check.py (ac1). Graded against G2, G5 and G6 at the pins in glib.py.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c14_check.py")" ac1 | tr -d '\r'
exit ${PIPESTATUS[0]}
