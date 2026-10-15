#!/usr/bin/env bash
# curated tags, slice h2 -- see ct_check.py.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 120 python "$(native "$D/ct_check.py")" slice h2 | tr -d '\r'
exit ${PIPESTATUS[0]}
