#!/usr/bin/env bash
# F2-AC3 AS AMENDED (issuer's re-cut @a12187c5a3 on row W1-S33, standing
# authority @9f4a57262f) -- THE STORE CENSUS, MATCHING WHOLE NAMES.
#
# BOTH READS ARE KEPT, side by side and in this order, because the pair is the
# evidence that the re-cut changed the INSTRUMENT and not the BAR:
#   (1) the AMENDED invocation, anchored to whole store names -> expected 0
#   (2) the ORIGINAL invocation, a substring match             -> 1, and the one
#       name it matches printed, so the difference is visible and not asserted
#   (3) ls -d on the three store paths, which measured 0 of 3 BEFORE the re-cut
#       and is what makes (1) a confirmation rather than a new claim
#
# THE CONTROL THE AMENDED PATTERN NEEDS IS NOT THE OLD ONE. An anchored regex
# can read 0 because nothing matches it EVER -- a typo in the anchors, a stray
# space, a CR from a Windows listing -- and that zero is indistinguishable from
# a clean machine. So the control here runs the SAME anchored form against a
# whole name that IS present (kuzu_stitch_db, S26's, deliberately still on this
# device and NOT the canonical graph) and must return non-zero.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
AMENDED='^(kuzu_nessie_db|kuzu_db|kuzu_ac7|kuzu_ac7\.db)$'
ORIGINAL='kuzu_nessie_db|kuzu_db|kuzu_ac7'
CONTROL='^(kuzu_stitch_db)$'

echo "=== f2_census_amended.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "AMENDED BY: 2.0.0_SA_COO~A @a12187c5a3 on NFRA_CLDGRPH-W1-S33, standing authority @9f4a57262f"
echo

echo "--- (1) THE AMENDED INVOCATION, verbatim from the face at HEAD ---"
echo "ls $W/ | grep -c -E '$AMENDED'"
AMENDED_N=$(ls "$W/" | grep -c -E "$AMENDED")
echo "AMENDED_COUNT=$AMENDED_N"
echo "  matching name(s):"
ls "$W/" | grep -E "$AMENDED" | sed 's/^/    /'
echo "  (no lines above = no whole store name in the listing)"
echo

echo "--- (2) THE ORIGINAL INVOCATION, kept beside it (the read that failed) ---"
echo "ls $W/ | grep -c -E '$ORIGINAL'"
ORIG_N=$(ls "$W/" | grep -c -E "$ORIGINAL")
echo "ORIGINAL_COUNT=$ORIG_N"
echo "  matching name(s):"
ls "$W/" | grep -E "$ORIGINAL" | sed 's/^/    /'
echo

echo "--- (3) THE STORES THEMSELVES, ls -d by absolute path (unchanged since the first read) ---"
PRESENT=0
for p in "$W/kuzu_db" "$W/kuzu_ac7.db" "$W/kuzu_nessie_db"; do
  if ls -d "$p" 2>&1; then PRESENT=$((PRESENT+1)); echo "    -> PRESENT"; else echo "    -> ABSENT $p"; fi
done
echo "STORES_PRESENT_BY_LS_D=$PRESENT of 3"
echo

echo "--- (4) CONTROL: the SAME ANCHORED FORM on a whole name that IS present ---"
echo "ls $W/ | grep -c -E '$CONTROL'"
CTRL_N=$(ls "$W/" | grep -c -E "$CONTROL")
echo "CONTROL_ANCHORED_COUNT=$CTRL_N  (kuzu_stitch_db: S26's, LAST in its chain, CG-s-20's question, NOT the canonical graph)"
if [ "$CTRL_N" -ge 1 ]; then
  echo "AMENDED_PATTERN_CONTROL=FIRED  (the anchored form returns NON-ZERO on a whole name that is there, so AMENDED_COUNT=0 is a reading and not an anchor that can never match)"
else
  echo "AMENDED_PATTERN_CONTROL=DEAD  (the anchored form could not match a whole name known to be present -- AMENDED_COUNT above is worthless)"
fi
echo

echo "--- F2-AC3 (AMENDED) VERDICT LINES ---"
echo "LOCAL_STORE_NAMES_MAIN_WORKSPACE=$AMENDED_N"
echo "STORES_PRESENT_BY_LS_D=$PRESENT of 3"
echo "ORIGINAL_PATTERN_COUNT=$ORIG_N (kept: the substring read that caught F-1's tombstone)"
echo "AMENDED_PATTERN_CONTROL=$( [ "$CTRL_N" -ge 1 ] && echo FIRED || echo DEAD )"
echo "=== f2_census_amended.sh END ==="
