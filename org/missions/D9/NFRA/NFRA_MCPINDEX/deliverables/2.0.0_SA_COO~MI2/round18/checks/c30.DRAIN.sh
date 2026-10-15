#!/usr/bin/env bash
# MX-c-30 DRAIN -- see c30_check.py (bucket, the drain check).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
timeout 280 python "$(native "$D/c30_check.py")" bucket | tr -d '\r'
exit ${PIPESTATUS[0]}
