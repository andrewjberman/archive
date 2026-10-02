#!/usr/bin/env bash
# battery.sh -- DSGN_AMGTV1 rounds 20-26 battery (issuer 2.0.0_SA_COO~D), exactly as run on candidate 0ab75973.
# Usage: bash battery.sh <portal-checkout-parent>   e.g.  bash battery.sh C:/tmp/wk-dsgn-amgtv1-70
#   The argument is the directory whose `portal/` is the checkout under test. Every check renders `<cwd>/portal`
#   (round15/checks/_load.cjs and the round22-26 checks read process.cwd()), so the script cd's there first.
#   The check FILES are read from the main workspace tree (this file's own tree), so a worktree whose outer branch
#   predates rounds 23-26 still runs the current checks. Writes no file. Exit 0 only when every line passes.
set -u
TARGET="${1:?usage: bash battery.sh <dir whose portal/ is under test>}"
M="$(cd "$(dirname "$0")/../.." && pwd)"   # .../deliverables/2.0.0_SA_COO~D
cd "$TARGET" || exit 2
echo "checkout under test: $(git -C portal rev-parse --short HEAD) in $TARGET/portal"
fail=0
for c in round26/checks/liveclass.cjs round24/checks/reasonclass.cjs round24/checks/lushaline.cjs round24/checks/posturezero.cjs \
         round23/checks/peerwords.cjs round23/checks/accession.cjs round23/checks/postureharness.cjs \
         round22/checks/codeface.cjs round22/checks/subjectrow.cjs round22/checks/starredclaims.cjs \
         round21/checks/tipface.cjs round20/checks/namecard.cjs; do
  out="$(timeout 300 node "$M/$c" 2>&1)"; rc=$?
  echo "$(printf '%s\n' "$out" | tail -1)   [rc=$rc]"
  [ "$rc" -eq 0 ] || fail=1
done
out="$(timeout 300 node "$M/round15/checks/bound.cjs" ALL leadPanelPattern.harness.cjs errorEmpty.harness.cjs tabs.harness.cjs \
  shell.harness.cjs drafting.harness.cjs execFallback.harness.cjs execPattern.harness.cjs execText.harness.cjs \
  peersCarry.harness.cjs peersPattern.harness.cjs peersReadFailed.harness.cjs modelPattern.harness.cjs \
  posturePattern.harness.cjs thesisLadder.harness.cjs 2>&1)"; rc=$?
echo "$(printf '%s\n' "$out" | tail -1)   [rc=$rc]"
[ "$rc" -eq 0 ] || fail=1
( cd portal && timeout 900 node node_modules/typescript/bin/tsc -b --noEmit ); rc=$?
echo "tsc -b --noEmit rc=$rc"
[ "$rc" -eq 0 ] || fail=1
[ "$fail" -eq 0 ] && echo "BATTERY: ALL PASS" || echo "BATTERY: FAIL"
exit "$fail"
