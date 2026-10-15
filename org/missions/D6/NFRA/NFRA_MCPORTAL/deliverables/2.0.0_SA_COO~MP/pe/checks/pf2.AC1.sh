#!/usr/bin/env bash
# MP-pf-2 AC1 (the Gateway page segments buckets and assets/bd vendor/firm pairs; decomposition PF.2): the seven named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE,
# so names are read from the sources) and `bun test src` exits 0 with >=68 pass (61 after MP-pe-2, six tests of the cut, one of A1) and 0 fail.
#   "a segmented bucket renders one sub-section per vendor and firm"
#   "a segment heading reads vendor words slash firm words"
#   "multi none and unresolved firms are labelled segments with their reason"
#   "the summary table lists each segment under its bucket with a link"
#   "a bucket with no segments renders as before"
#   "every tools table sits in a scroll container"
#   "every table cell keeps its text on one line"                (A1)
. "$(dirname "$0")/../../pd/checks/_root.sh"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "a segmented bucket renders one sub-section per vendor and firm" "a segment heading reads vendor words slash firm words" "multi none and unresolved firms are labelled segments with their reason" "the summary table lists each segment under its bucket with a link" "a bucket with no segments renders as before" "every tools table sits in a scroll container" "every table cell keeps its text on one line"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 7; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 7 ] && [ "${pass:-0}" -ge 68 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
