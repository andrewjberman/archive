#!/usr/bin/env bash
# OA-e-11 AC1 (built, three arms on a scratch fixture; row Z-S17): with the owned-paths hook installed into the nested
# repo's shared hooks dir, (1) an OUT-OF-LANE commit in an opal_ai LINKED worktree OUTSIDE every parent worktree is
# REFUSED; (2) the same commit in the MAIN nested checkout is REFUSED; (3) an IN-LANE commit in the main nested checkout
# LANDS (positive control -- a hook that refuses everything fails here). opal_ai/** is lane ANY_EXEC_OR_AE:
# 0.4.0_DS_ClientPlatform is out of it, 1.0.0_SA_CTO is in it.
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/e11_fixture.sh"
a1=$(fx_commit "$OUTSIDE" 0.4.0_DS_ClientPlatform planted_outside.md)
a2=$(fx_commit "$NESTED" 0.4.0_DS_ClientPlatform planted_nested_out.md)
a3=$(fx_commit "$NESTED" 1.0.0_SA_CTO planted_nested_in.md)
echo "arm1 outside-worktree out-of-lane: $a1; arm2 main-nested out-of-lane: $a2; arm3 main-nested in-lane: $a3 (fixture $FX)"
rm -rf "$FX" 2>/dev/null
case "$a1" in refused*) ;; *) echo "RESULT: FAIL"; exit 1 ;; esac
case "$a2" in refused*) ;; *) echo "RESULT: FAIL"; exit 1 ;; esac
[ "$a3" = landed ] || { echo "RESULT: FAIL"; exit 1; }
echo "RESULT: PASS"; exit 0
