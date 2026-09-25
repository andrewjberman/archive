#!/usr/bin/env bash
# MX-q-2 AC1 (R-2 (1), the Black Diamond read, recorded): round2-reads.result.md at HEAD carries the line
#   BD-NULL-CUSIP rows=<n> null_cusip=<k> since=2026-04-14 source=<s3 prefix> read_at=<UTC>
# with n > 0 and 0 <= k <= n, and the line
#   BD-SERVED-CUSIP-JOINS served_figures_checked=<m> carrying_null=<j>
# with m >= 1 (the served figures that join on cusip, each named in the file) and j <= m.
. "$(dirname "$0")/_root.sh"
F="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~4/round2-reads.result.md"
t=$(git show "HEAD:$F" 2>/dev/null | tr -d '\r')
[ -n "$t" ] || { echo "$F absent at HEAD"; echo "RESULT: FAIL"; exit 1; }
l1=$(printf '%s\n' "$t" | grep -m1 '^BD-NULL-CUSIP '); l2=$(printf '%s\n' "$t" | grep -m1 '^BD-SERVED-CUSIP-JOINS ')
n=$(printf '%s' "$l1" | sed -n 's/.* rows=\([0-9]*\) .*/\1/p'); k=$(printf '%s' "$l1" | sed -n 's/.* null_cusip=\([0-9]*\) .*/\1/p')
s=$(printf '%s' "$l1" | sed -n 's/.* since=\([0-9-]*\) .*/\1/p'); r=$(printf '%s' "$l1" | grep -c ' read_at=20')
m=$(printf '%s' "$l2" | sed -n 's/.* served_figures_checked=\([0-9]*\).*/\1/p'); j=$(printf '%s' "$l2" | sed -n 's/.* carrying_null=\([0-9]*\).*/\1/p')
echo "BD read: rows=${n:-?} null_cusip=${k:-?} since=${s:-?} read_at present=$r; served figures checked=${m:-?} carrying null=${j:-?}"
if [ -n "$n" ] && [ "$n" -gt 0 ] && [ -n "$k" ] && [ "$k" -le "$n" ] && [ "$s" = 2026-04-14 ] && [ "$r" = 1 ] && [ -n "$m" ] && [ "$m" -ge 1 ] && [ -n "$j" ] && [ "$j" -le "$m" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
