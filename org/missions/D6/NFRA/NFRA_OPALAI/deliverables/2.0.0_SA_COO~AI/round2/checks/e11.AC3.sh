#!/usr/bin/env bash
# OA-e-11 AC3 (bound: the PARENT repository's lane verdicts do not move). On the same scratch fixture, with the hook
# installed into the superproject's own hooks dir: an OUT-OF-LANE parent commit (docs/architecture/ZZPLANT.md, lane
# ANY_CTO, by 0.4.0_DS_ClientPlatform) is REFUSED, and an IN-LANE one (same path shape, by 1.0.0_SA_CTO) LANDS.
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/e11_fixture.sh"
p1=$(fx_commit "$SUPER" 0.4.0_DS_ClientPlatform docs/architecture/ZZPLANT_OUT.md)
p2=$(fx_commit "$SUPER" 1.0.0_SA_CTO docs/architecture/ZZPLANT_IN.md)
echo "parent out-of-lane: $p1; parent in-lane: $p2 (fixture $FX)"
rm -rf "$FX" 2>/dev/null
case "$p1" in refused*) ;; *) echo "RESULT: FAIL"; exit 1 ;; esac
[ "$p2" = landed ] || { echo "RESULT: FAIL"; exit 1; }
echo "RESULT: PASS"; exit 0
