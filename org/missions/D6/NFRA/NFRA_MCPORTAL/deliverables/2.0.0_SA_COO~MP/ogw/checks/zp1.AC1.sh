#!/usr/bin/env bash
# MP-zp-1 AC1 (FWD-29, FWD-28 on /opalgateway; decomposition OGP1.1): a stopped person's switches read off and are disabled, and the audit list
# re-reads after the panel writes. TWO named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources),
# and `bun test src` exits 0 with >=PASS_MIN pass and 0 fail (89 at mcportal f90f03a, plus these two):
#   "a stopped person's tool and channel switches read off and are disabled on the opalgateway page, and the page says the gateway admits nothing"
#   "the opalgateway audit list reads again after the panel writes a change"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_OGP_PASS_MIN:-91}"
[ -d mcportal/src/pages ] || { echo "mcportal/src/pages absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in "a stopped person's tool and channel switches read off and are disabled on the opalgateway page, and the page says the gateway admits nothing" \
         "the opalgateway audit list reads again after the panel writes a change"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1))
done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 2; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 2 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
