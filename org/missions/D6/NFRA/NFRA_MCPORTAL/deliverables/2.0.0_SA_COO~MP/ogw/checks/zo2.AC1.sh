#!/usr/bin/env bash
# MP-zo-2 AC1 (PRD v0.10 FWD-28; decomposition v20 OGW1.2): the audit list on /opalgateway, with the unattributed negative arm.
# THREE named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources), and `bun test src`
# exits 0 with >=PASS_MIN pass and 0 fail (79 at DEV 21ad404, plus the seven of MP-zo-1, plus these three):
#   "the audit list shows every add, subtract and stop with who, when, before and after, for every person"
#   "a change with no attributing writer is flagged unattributed and never shown as an owner act"
#   "the audit list orders newest first and names the person"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_OGW_PASS_MIN:-89}"
P=mcportal/src/pages
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in "the audit list shows every add, subtract and stop with who, when, before and after, for every person" \
         "a change with no attributing writer is flagged unattributed and never shown as an owner act" \
         "the audit list orders newest first and names the person"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1))
done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 3; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 3 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
