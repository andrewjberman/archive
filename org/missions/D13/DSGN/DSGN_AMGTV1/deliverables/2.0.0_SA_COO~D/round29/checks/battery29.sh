#!/usr/bin/env bash
# battery29.sh -- DSGN_AMGTV1 round 29 battery (issuer 2.0.0_SA_COO~D): the round 20-26 battery (round26/checks/battery.sh) with a
# per-cell SKIP list.
# Usage: bash battery29.sh <portal-checkout-parent> [--skip name1,name2,...]
#   A name is a check file's basename without .cjs (e.g. namecard, tipface) or a harness file's basename without .harness.cjs
#   (e.g. shell, leadPanelPattern). A SKIP is legal only for an item whose re-anchor belongs to a SIBLING cell of round 29 (the
#   order names each skip and why). Every skipped item prints "SKIPPED <name>"; the summary names the skip count. At the drain the
#   issuer runs this with NO skip on the combined candidate: that run is the battery's real grade.
# Exit 0 only when every non-skipped line passes. Writes no file.
set -u
TARGET="${1:?usage: bash battery29.sh <dir whose portal/ is under test> [--skip a,b]}"
SKIP=""
if [ "${2:-}" = "--skip" ]; then SKIP=",${3:-},"; fi
M="$(cd "$(dirname "$0")/../.." && pwd)"   # .../deliverables/2.0.0_SA_COO~D
cd "$TARGET" || exit 2
echo "checkout under test: $(git -C portal rev-parse --short HEAD) in $TARGET/portal"
skipped=0
is_skipped() { case "$SKIP" in *",$1,"*) return 0 ;; *) return 1 ;; esac; }
fail=0
for c in round26/checks/liveclass.cjs round24/checks/reasonclass.cjs round24/checks/lushaline.cjs round24/checks/posturezero.cjs \
         round23/checks/peerwords.cjs round23/checks/accession.cjs round23/checks/postureharness.cjs \
         round22/checks/codeface.cjs round22/checks/subjectrow.cjs round22/checks/starredclaims.cjs \
         round21/checks/tipface.cjs round20/checks/namecard.cjs; do
  n="$(basename "$c" .cjs)"
  if is_skipped "$n"; then echo "SKIPPED $n"; skipped=$((skipped+1)); continue; fi
  out="$(timeout 300 node "$M/$c" 2>&1)"; rc=$?
  echo "$(printf '%s\n' "$out" | tail -1)   [rc=$rc]"
  [ "$rc" -eq 0 ] || fail=1
done
H=""
for h in leadPanelPattern errorEmpty tabs shell drafting execFallback execPattern execText peersCarry peersPattern peersReadFailed \
         modelPattern posturePattern thesisLadder; do
  if is_skipped "$h"; then echo "SKIPPED $h"; skipped=$((skipped+1)); continue; fi
  H="$H $h.harness.cjs"
done
out="$(timeout 300 node "$M/round15/checks/bound.cjs" ALL $H 2>&1)"; rc=$?
echo "$(printf '%s\n' "$out" | tail -1)   [rc=$rc]"
[ "$rc" -eq 0 ] || fail=1
( cd portal && timeout 900 node node_modules/typescript/bin/tsc -b --noEmit ); rc=$?
echo "tsc -b --noEmit rc=$rc"
[ "$rc" -eq 0 ] || fail=1
# ISSUER AMENDMENT 1 (round 33, 2026-10-03): the CI's "Run ESLint" step, errors only (warnings do not fail CI), over this project's
# paths. DEV 49c6e94a0f passed this battery and tsc, then failed CI on one ESLint error (WhatChangedPanel.tsx:395, MSTR~Z msg 29015).
# eslint exits 0 clean, 1 on an error, 2 when it cannot run; anything but 0 fails the battery.
if is_skipped eslint; then echo "SKIPPED eslint"; skipped=$((skipped+1)); else
  out="$( cd portal && timeout 600 node node_modules/eslint/bin/eslint.js --quiet --no-color src/pages/SecurityAnalysis \
    src/api/endpoints/amgt-lead-panel.ts src/lib/chartColors.ts src/lib/sentimentColor.ts src/components/market-performance/TopicCloud.tsx 2>&1 )"; rc=$?
  [ "$rc" -eq 0 ] || printf '%s\n' "$out" | grep -E "error|problem" | tail -6
  echo "eslint --quiet (SecurityAnalysis + the lead-panel endpoint + chart libs) rc=$rc"
  [ "$rc" -eq 0 ] || fail=1
fi
if [ "$fail" -eq 0 ]; then echo "BATTERY29: ALL PASS ($skipped skipped)"; else echo "BATTERY29: FAIL ($skipped skipped)"; fi
exit "$fail"
