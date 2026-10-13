#!/bin/bash
# AMGT_RESAPP round-103 PREP -- FWD-40 promote: the feature branch is GREEN: the portal's own typecheck, its lint, and the Security Analysis harness suite.
#   bash r103_feature_green.sh <nested portal checkout>
# The suite is every `src/pages/SecurityAnalysis/__harness__/*.harness.{cjs,mjs}` run as `node <file>` with no argument; a harness that exits non-zero is NAMED. bun resolves via PATH
# (the profile's), never a baked path. Prints `R103 FEATURE GREEN: YES|NO (typecheck rc A, lint rc B, harness C of D)`.
set -u
P="${1:?nested portal checkout}"
cd "$P" || { echo "R103 FEATURE GREEN: NO (no such directory)"; exit 1; }
BUN="$(command -v bun || true)"
[ -z "$BUN" ] && { echo "R103 FEATURE GREEN: NO (bun not on PATH)"; exit 1; }
[ -d node_modules ] || "$BUN" install --frozen-lockfile >/dev/null 2>&1
"$BUN" run typecheck >/tmp/r103_typecheck.txt 2>&1; TC=$?
"$BUN" run lint >/tmp/r103_lint.txt 2>&1; LI=$?
PASS=0; TOTAL=0; BAD=""
for f in src/pages/SecurityAnalysis/__harness__/*.harness.cjs src/pages/SecurityAnalysis/__harness__/*.harness.mjs; do
  [ -f "$f" ] || continue
  TOTAL=$((TOTAL + 1))
  if node "$f" >/tmp/r103_harness_one.txt 2>&1; then PASS=$((PASS + 1)); else BAD="$BAD $(basename "$f")"; fi
done
echo "typecheck rc $TC | lint rc $LI | harness $PASS of $TOTAL | failing:${BAD:- none}"
if [ "$TC" -eq 0 ] && [ "$LI" -eq 0 ] && [ "$TOTAL" -gt 0 ] && [ "$PASS" -eq "$TOTAL" ]; then
  echo "R103 FEATURE GREEN: YES (typecheck rc $TC, lint rc $LI, harness $PASS of $TOTAL)"; exit 0
fi
echo "R103 FEATURE GREEN: NO (typecheck rc $TC, lint rc $LI, harness $PASS of $TOTAL)"; exit 1
