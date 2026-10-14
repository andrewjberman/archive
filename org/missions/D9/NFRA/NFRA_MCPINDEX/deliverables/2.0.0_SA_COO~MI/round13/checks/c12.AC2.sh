#!/usr/bin/env bash
# MX-c-12 AC2 -- see c12_check.py (ac2). Graded against G1 at the pin in g1lib.py.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 110 python "$(native "$D/c12_check.py")" ac2 | tr -d '\r'
exit ${PIPESTATUS[0]}
