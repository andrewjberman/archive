#!/usr/bin/env bash
# MX-c-12 AC3 -- see c12_check.py (ac3). Graded against G1 at the pin in g1lib.py.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c12_check.py")" ac3 | tr -d '\r'
exit ${PIPESTATUS[0]}
