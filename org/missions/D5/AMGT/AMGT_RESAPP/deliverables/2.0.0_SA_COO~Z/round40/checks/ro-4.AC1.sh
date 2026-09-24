#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-4 AC1 -- two labels stop misstating: (a) Posture's "still loading" is keyed to a query
# ACTUALLY FETCHING, never to react-query's isLoading of a DISABLED query (true forever when the comparable key is
# unresolved); (b) the identity header's session badge names itself as the Bloomberg SESSION, so "UNKNOWN" beside the
# ticker no longer reads as an identity attribute. usage: bash <this>
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
P=src/pages/SecurityAnalysis/tabs/PostureTab.tsx; O=src/pages/SecurityAnalysis/components/SecurityOverlay.tsx
a=$(grep -c -E 'comparable(Thesis|Peers)\.isLoading' "$P"); b=$(grep -c "'BLOOMBERG: " "$O"); c=$(grep -c -i "bloomberg session" "$O")
echo "PostureTab comparable *.isLoading reads: $a (want 0); badge labels 'BLOOMBERG: ...': $b (want 0); labels naming the session: $c (want >= 3)"
[ "$a" -eq 0 ] && [ "$b" -eq 0 ] && [ "$c" -ge 3 ]
