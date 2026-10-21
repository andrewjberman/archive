#!/usr/bin/env bash
# MP-zb-1 AC1 (FWD-30; decomposition OGB1.1) -- DRAFT, NOT DRY-RUN (written before the cut; dry-run at the base in the provisioned slot when cut).
# THREE named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources), and `bun test src` exits 0
# with >=PASS_MIN pass and 0 fail (91 at mcportal a577f99, plus these three = 94):
#   "turning a bucket or folder on adds its string to channels_allow and needs the owner's WIDENING confirm before it is sent"
#   "turning a bucket or folder off adds it to channels_deny, restoring removes it, and channels_allow is never edited by either"
#   "widening_confirm rides only on the one confirmed add and never on an off or a restore"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_OGB_PASS_MIN:-94}"
[ -d mcportal/src/pages ] || { echo "mcportal/src/pages absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in "turning a bucket or folder on adds its string to channels_allow and needs the owner's WIDENING confirm before it is sent" \
         "turning a bucket or folder off adds it to channels_deny, restoring removes it, and channels_allow is never edited by either" \
         "widening_confirm rides only on the one confirmed add and never on an off or a restore"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1))
done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 3; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 3 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
