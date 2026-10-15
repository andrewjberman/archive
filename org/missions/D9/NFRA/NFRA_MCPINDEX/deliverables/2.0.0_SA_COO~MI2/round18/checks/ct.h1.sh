#!/usr/bin/env bash
# curated tags, slice h1 -- see ct_check.py.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 120 python "$(native "$D/ct_check.py")" slice h1 | tr -d '\r'
exit ${PIPESTATUS[0]}
