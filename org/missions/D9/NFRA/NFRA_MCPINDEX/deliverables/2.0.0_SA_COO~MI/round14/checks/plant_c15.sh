#!/usr/bin/env bash
# plant_c15.sh -- the ISSUER's cut-time planted arms for c15.AC1 and AC2 (standing battery clause 1). Not a criterion.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
C="$(native "$D/c15_check.py")"; P="$(native "$D/plant_impl_c15.py")"
ok=0; wrong=0
arm() { name="$1"; want="$2"; shift 2; env "$@" >/tmp/c15plant.$$ 2>&1; rc=$?
  if [ "$rc" = "$want" ]; then ok=$((ok+1)); echo "ARM ok:   $name -> rc=$rc"; else wrong=$((wrong+1)); echo "ARM WRONG: $name -> rc=$rc want $want"; tail -8 /tmp/c15plant.$$ | cut -c1-220; fi; }
arm "reference loader, ac1" 0 C15_IMPL="$P" python "$C" ac1
arm "reference writer, ac2" 0 C15_IMPL="$P" python "$C" ac2
arm "lax table validator, ac1" 1 C15_IMPL="$P" C15_PLANT_LAX=1 python "$C" ac1
arm "a loader that does not join, ac1" 1 C15_IMPL="$P" C15_PLANT_NOJOIN=1 python "$C" ac1
arm "a loader that does not join, ac2" 1 C15_IMPL="$P" C15_PLANT_NOJOIN=1 python "$C" ac2
echo "PLANTED ARMS: ok $ok, wrong $wrong"; rm -f /tmp/c15plant.$$; [ "$wrong" = 0 ]
