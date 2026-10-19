#!/usr/bin/env bash
# MP-z-8 AC1 (CTO round analysis z-round1 @11c572fef9, item 1; defect P1, class display): a Gateway segment table lists only the indexes whose (vendor, firm) is that segment's.
# FIVE named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources), and `bun test src` exits 0 with >=PASS_MIN pass and 0 fail:
#   "a segment table lists only the indexes whose vendor and firm are that segment's"
#   "a tool serving two pairs shows each pair its own indexes"
#   "a tool with no index_pairs keeps listing its indexes unchanged"
#   "a tool with an empty index_pairs lists none under any segment"
#   "the audit case: client_get_holdings shows 6 of its 13 indexes under Schwab / 49 Financial"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_GWZ_PASS_MIN:-79}"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in "a segment table lists only the indexes whose vendor and firm are that segment's" \
         "a tool serving two pairs shows each pair its own indexes" \
         "a tool with no index_pairs keeps listing its indexes unchanged" \
         "a tool with an empty index_pairs lists none under any segment" \
         "the audit case: client_get_holdings shows 6 of its 13 indexes under Schwab / 49 Financial"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1))
done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 5; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 5 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
