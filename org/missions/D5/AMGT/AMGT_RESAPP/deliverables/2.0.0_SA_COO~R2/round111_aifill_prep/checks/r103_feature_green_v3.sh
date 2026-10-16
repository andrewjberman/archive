#!/bin/bash
# r103_feature_green_v3.sh = r103_feature_green_v2.sh with the two output files moved from /tmp/r103_typecheck.txt and /tmp/r103_lint.txt into a per-run mktemp directory (W486-S3, CTO 6756). The verdict lines (the last two printed) are unchanged; the output directory is printed first.
# AMGT_RESAPP round-103 PREP -- FWD-40 promote: the feature branch is GREEN, v2: typecheck and lint pass, and NO Security Analysis harness regresses against the PROD release it was cut from.
#   bash r103_feature_green_v2.sh <nested portal checkout on the feature branch> [<base ref, default 15c9754975>]
# v1 ran every `__harness__/*.harness.{cjs,mjs}` bare and required all to exit 0; three exit non-zero at PROD itself (two need arguments, one has a stale import), which made the
# criterion unmeetable by any branch. v2 runs each harness bare on the branch AND on a detached worktree of the base ref (removed at the end) and classes it:
#   PASS            exit 0 on the branch
#   PRE-EXISTING    non-zero on the branch AND non-zero on the base (named; the branch did not cause it)
#   REGRESSION      non-zero on the branch and exit 0 at the base, or a harness the base lacks that fails
# Prints `R103 FEATURE GREEN: YES|NO (typecheck rc A, lint rc B, harness P of T pass, base Q of U, regressions R, pre-existing: names)`.
set -u
P="${1:?nested portal checkout}"
BASE="${2:-15c9754975}"
cd "$P" || { echo "R103 FEATURE GREEN: NO (no such directory)"; exit 1; }
BUN="$(command -v bun || true)"
[ -z "$BUN" ] && { echo "R103 FEATURE GREEN: NO (bun not on PATH)"; exit 1; }
HERE="$(pwd)"
TMPB="$(mktemp -d -u /tmp/r103_base_XXXXXX)"
cleanup() { git -C "$HERE" worktree remove --force "$TMPB" >/dev/null 2>&1; }
trap cleanup EXIT

# v3 (W486-S3, CTO 6756): the typecheck and lint output go to a per-run directory, never to a fixed path two runs share.
OUTD="$(mktemp -d /tmp/r103_out_XXXXXX)"
echo "R103 OUTPUT DIR: $OUTD (typecheck.txt, lint.txt)"
"$BUN" run typecheck >"$OUTD/typecheck.txt" 2>&1; TC=$?
"$BUN" run lint >"$OUTD/lint.txt" 2>&1; LI=$?

git -C "$HERE" worktree add --detach "$TMPB" "$BASE" >/dev/null 2>&1 || { echo "R103 FEATURE GREEN: NO (cannot cut the base worktree at $BASE)"; exit 1; }
WINTMP="$(cd "$TMPB" && pwd -W 2>/dev/null || pwd)"
WINNM="$(cd "$HERE" && pwd -W 2>/dev/null || pwd)/node_modules"
cmd //c "mklink /J ${WINTMP//\//\\}\\node_modules ${WINNM//\//\\}" >/dev/null 2>&1

run_one() { # <dir> <file> -> rc
  ( cd "$1" && timeout 120 node "$2" >/dev/null 2>&1 ); echo $?
}
PASS=0; TOTAL=0; BASEPASS=0; BASETOTAL=0; REG=0; PRE=""; REGN=""
for f in $(cd "$HERE" && ls src/pages/SecurityAnalysis/__harness__/*.harness.cjs src/pages/SecurityAnalysis/__harness__/*.harness.mjs 2>/dev/null); do
  TOTAL=$((TOTAL + 1))
  RC=$(run_one "$HERE" "$f")
  if [ -f "$TMPB/$f" ]; then
    BRC=$(run_one "$TMPB" "$f"); BASETOTAL=$((BASETOTAL + 1)); [ "$BRC" -eq 0 ] && BASEPASS=$((BASEPASS + 1))
  else
    BRC=absent
  fi
  if [ "$RC" -eq 0 ]; then
    PASS=$((PASS + 1))
  elif [ "$BRC" != "absent" ] && [ "$BRC" != "0" ]; then
    PRE="$PRE $(basename "$f")"
  else
    REG=$((REG + 1)); REGN="$REGN $(basename "$f")"
  fi
done
echo "typecheck rc $TC | lint rc $LI | harness $PASS of $TOTAL pass | base $BASEPASS of $BASETOTAL | regressions $REG:${REGN:- none} | pre-existing:${PRE:- none}"
if [ "$TC" -eq 0 ] && [ "$LI" -eq 0 ] && [ "$TOTAL" -gt 0 ] && [ "$REG" -eq 0 ] && [ "$PASS" -ge "$BASEPASS" ]; then
  echo "R103 FEATURE GREEN: YES (typecheck rc $TC, lint rc $LI, harness $PASS of $TOTAL pass, base $BASEPASS of $BASETOTAL, regressions 0, pre-existing:${PRE:- none})"; exit 0
fi
echo "R103 FEATURE GREEN: NO (typecheck rc $TC, lint rc $LI, harness $PASS of $TOTAL pass, base $BASEPASS of $BASETOTAL, regressions $REG)"; exit 1
