#!/usr/bin/env bash
# plant_c13.sh -- the ISSUER's cut-time planted arms for c13.AC1 and AC3 (standing battery clause 1). Not a criterion.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
C="$(native "$D/c13_check.py")"; P="$(native "$D/plant_impl_c13.py")"
ok=0; wrong=0
arm() { name="$1"; want="$2"; shift 2; env "$@" >/tmp/c13plant.$$ 2>&1; rc=$?
  if [ "$rc" = "$want" ]; then ok=$((ok+1)); echo "ARM ok:   $name -> rc=$rc"; else wrong=$((wrong+1)); echo "ARM WRONG: $name -> rc=$rc want $want"; tail -8 /tmp/c13plant.$$ | cut -c1-200; fi; }
arm "reference impl, ac1" 0 C13_IMPL="$P" python "$C" ac1
arm "reference impl, ac3" 0 C13_IMPL="$P" python "$C" ac3
arm "lax table validator, ac1" 1 C13_IMPL="$P" C13_PLANT_LAX=1 python "$C" ac1
echo "PLANTED ARMS: ok $ok, wrong $wrong"; rm -f /tmp/c13plant.$$; [ "$wrong" = 0 ]
