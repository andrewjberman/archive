#!/usr/bin/env bash
# MX-q-2 AC2 (R-3, the Eclipse tenancy read, recorded): round2-reads.result.md at HEAD carries the line
#   ECLIPSE-SCOPE rows=<n> distinct_ids=<d> outside_allowlist=<k> allowlist=<repo path> read_at=<UTC>
# with n > 0, d >= 1, 0 <= k <= d, and an allowlist path that exists at HEAD.
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~4/round2-reads.result.md"
t=$(git show "HEAD:$F" 2>/dev/null | tr -d '\r')
[ -n "$t" ] || { echo "$F absent at HEAD"; echo "RESULT: FAIL"; exit 1; }
l=$(printf '%s\n' "$t" | grep -m1 '^ECLIPSE-SCOPE ')
n=$(printf '%s' "$l" | sed -n 's/.* rows=\([0-9]*\) .*/\1/p'); d=$(printf '%s' "$l" | sed -n 's/.* distinct_ids=\([0-9]*\) .*/\1/p')
k=$(printf '%s' "$l" | sed -n 's/.* outside_allowlist=\([0-9]*\) .*/\1/p'); a=$(printf '%s' "$l" | sed -n 's/.* allowlist=\([^ ]*\) .*/\1/p')
ap=no; [ -n "$a" ] && git cat-file -e "HEAD:${a%%:*}" 2>/dev/null && ap=yes
r=$(printf '%s' "$l" | grep -c ' read_at=20')
echo "Eclipse read: rows=${n:-?} distinct_ids=${d:-?} outside_allowlist=${k:-?} allowlist=${a:-?} (at HEAD=$ap) read_at present=$r"
if [ -n "$n" ] && [ "$n" -gt 0 ] && [ -n "$d" ] && [ "$d" -ge 1 ] && [ -n "$k" ] && [ "$k" -le "$d" ] && [ "$ap" = yes ] && [ "$r" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
