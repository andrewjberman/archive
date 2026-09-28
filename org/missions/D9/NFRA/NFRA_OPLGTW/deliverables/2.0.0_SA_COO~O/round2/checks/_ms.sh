#!/usr/bin/env bash
# _ms.sh -- sourced by the OG-m-1 checks: locate the read's JSON record.
. "$(dirname "$0")/_root.sh"
MS=$(git ls-files 'org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/*/MARKER_STORM_READ.json' | head -1)
[ -n "$MS" ] || { echo "MARKER_STORM_READ.json absent at HEAD"; echo "RESULT: FAIL"; exit 1; }
