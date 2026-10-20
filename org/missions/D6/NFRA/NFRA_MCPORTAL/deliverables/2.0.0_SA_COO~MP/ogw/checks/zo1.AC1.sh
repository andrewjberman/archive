#!/usr/bin/env bash
# MP-zo-1 AC1 (PRD v0.10 FWD-23, 24, 25, 27; decomposition v20 OGW1.1): the /opalgateway page.
# SEVEN named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources), and `bun test src`
# exits 0 with >=PASS_MIN pass and 0 fail (79 at mcportal DEV 21ad404, plus these seven):
#   "the opalgateway page lists each person and shows the selected person's channels, tools and tier"
#   "subtracting one tool from the opalgateway page posts one change and the switch reads off after the re-read"
#   "restoring that tool posts one change and the switch reads on again"
#   "stopping and restoring a person each post one change"
#   "the page refuses to stop the last master admin and sends no request"
#   "opalgateway is the last sidebar entry and is listed in routes.json"
#   "the people page links each person into opalgateway"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_OGW_PASS_MIN:-86}"
P=mcportal/src/pages
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in "the opalgateway page lists each person and shows the selected person's channels, tools and tier" \
         "subtracting one tool from the opalgateway page posts one change and the switch reads off after the re-read" \
         "restoring that tool posts one change and the switch reads on again" \
         "stopping and restoring a person each post one change" \
         "the page refuses to stop the last master admin and sends no request" \
         "opalgateway is the last sidebar entry and is listed in routes.json" \
         "the people page links each person into opalgateway"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1))
done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 7; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 7 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
