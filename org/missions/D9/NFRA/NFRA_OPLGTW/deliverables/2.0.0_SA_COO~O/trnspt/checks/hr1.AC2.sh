#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-hr-1 AC2 (PRD v1.3 C7): the transcripts route's prefix is the fixed literal /hx/transcripts,
# graded for distinctness, and used in the app code; its bearer secret grades CONFORMANT (grade(), SECRET); and /ms/*
# is byte-unchanged since the cut base (C7: "a new capability, never a widening of /ms/*").
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
J="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~16/ROUTE_NAMES.json"
[ -f "$J" ] || { echo "$J absent"; echo "RESULT: FAIL"; exit 1; }
nm=$(timeout 60 python "$(native "$H/_names.py")" transcripts "$(native "$J")" 2>&1 | tr -d '\r'); printf '%s\n' "$nm"
add=$(git log --diff-filter=A --format=%H HEAD -- "$GW/app/transcript_route.py" | tail -1)
# cut base: the parent of the commit that added the route module (graded the same before and after the drain)
if [ -n "$add" ]; then base=$(git rev-parse "$add^"); else base=$(git merge-base HEAD CLOUD 2>/dev/null); fi
ms=$( [ -n "$base" ] && git diff --name-only "$base" HEAD -- "$GW/app/ms_ingest.py" | grep -c . )
echo "app/ms_ingest.py changed since base ${base:0:10}: ${ms:-UNREAD}"
if printf '%s\n' "$nm" | grep -q "^NAMES ok transcripts$" && [ "$ms" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
