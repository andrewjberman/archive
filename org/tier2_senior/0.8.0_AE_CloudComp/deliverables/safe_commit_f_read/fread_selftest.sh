#!/usr/bin/env bash
# Self-test for TO safe-commit-F-read-override-fix, Phase 2 step 1.
#
# COVERAGE DENOMINATOR (stated up front, per grounding doctrine):
# This exercises the REAL SHIPPED BYTES of the override-read block, extracted from the live
# .tools/safe-commit.sh by LINE RANGE (never retyped), eval'd with controlled COMMIT_ARGS.
# It covers: the -m read loop, the additive -F/--file read loop, and the CS_OVR extract.
# It does NOT cover: the :530 trigger predicate, the comp-system rc=2 branch, the audit-log
# write, or the git reset/exit-1 block path. Those need a genuine rc=2, which would require
# making 06 stale fabric-wide -- refused deliberately (would risk blocking live agent commits).

set -u
SC="$(git rev-parse --show-toplevel)/.tools/safe-commit.sh"
WORK="$(dirname "$0")/.fread_work.$$"   # script-adjacent; /tmp is not writable in the Cygwin harness
rm -rf "$WORK"; mkdir -p "$WORK"; trap 'rm -rf "$WORK"' EXIT   # self-cleaning: never litter the tree

# --- locate the block by ANCHOR, not by hardcoded line numbers (numbers drift) -------------
START="$(grep -n '^    CS_MSG=""; _csk=0' "$SC" | head -1 | cut -d: -f1)"
END="$(grep -n '^    CS_OVR="\$(printf' "$SC" | head -1 | cut -d: -f1)"
if [ -z "$START" ] || [ -z "$END" ]; then echo "FATAL: could not anchor the block"; exit 9; fi
echo "BLOCK: real safe-commit.sh lines ${START}-${END} (anchored, not hardcoded)"
sed -n "${START},${END}p" "$SC" > "$WORK/block_real.sh"
# MUTANT: the same block with the additive -F loop surgically removed (negative control).
# Removes from the ADDITIVE comment through the end of its while-loop, keeping -m + extract.
awk '
  /ADDITIVE \(TO safe-commit-F-read-override-fix/ {skip=1}
  skip && /^    done$/ {skip=0; next}
  !skip {print}
' "$WORK/block_real.sh" > "$WORK/block_mutant.sh"

if ! grep -q '_cfk' "$WORK/block_real.sh"; then echo "FATAL: real block lacks the -F loop"; exit 9; fi
if grep -q '_cfk' "$WORK/block_mutant.sh"; then echo "FATAL: mutant still has the -F loop -- control is dead"; exit 9; fi
echo "MUTANT: -F loop removed ($(wc -l < "$WORK/block_real.sh") -> $(wc -l < "$WORK/block_mutant.sh") lines)"
echo

# --- bodies --------------------------------------------------------------------------------
printf 'subject line\n\nbody text\n# system-current-override: hashed trailer reason\n'  > "$WORK/b_hash.txt"
printf 'subject line\n\nbody text\nsystem-current-override: plain trailer reason\n'      > "$WORK/b_plain.txt"
printf 'subject line\n\nbody with no trailer at all\n'                                   > "$WORK/b_none.txt"
printf 'subject\n\n# system-current-override: inject $(touch %s/PWNED) tail\n' "$WORK"   > "$WORK/b_inject.txt"

run_case () {  # $1=block  $2=expected  $3=label ; rest: COMMIT_ARGS
  local blk="$1" exp="$2" lbl="$3"; shift 3
  local got
  got="$(
    COMMIT_ARGS=("$@")
    . "$blk" >/dev/null 2>&1
    printf '%s' "${CS_OVR:-}"
  )"
  if [ "$got" = "$exp" ]; then printf 'PASS  %-46s -> %s\n' "$lbl" "${got:-<empty>}"; return 0
  else printf 'FAIL  %-46s -> got=[%s] want=[%s]\n' "$lbl" "$got" "$exp"; return 1; fi
}

fails=0
echo "=== REAL BLOCK (the shipped fix) ==="
run_case "$WORK/block_real.sh" "hashed trailer reason" "T1 -F with '# system-current-override:'" -F "$WORK/b_hash.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" "plain trailer reason"  "T2 -F with plain trailer (-m parity)"    -F "$WORK/b_plain.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" ""                      "T3 -F, NO trailer -> no false override"  -F "$WORK/b_none.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" "m path reason"         "T4 -m trailer (REGRESSION check)"        -m "subj
system-current-override: m path reason" || fails=$((fails+1))
run_case "$WORK/block_real.sh" "hashed trailer reason" "T5 -m AND -F together"                   -m "plain subject" -F "$WORK/b_hash.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" "plain trailer reason"  "T6 --file=<f> form"                      "--file=$WORK/b_plain.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" "plain trailer reason"  "T7 --file <f> form"                      --file "$WORK/b_plain.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" ""                      "T8 -F <missing file> -> no crash/empty"  -F "$WORK/nope.txt" || fails=$((fails+1))
run_case "$WORK/block_real.sh" ""                      "T9 -F - (stdin) skipped"                 -F "-" || fails=$((fails+1))

echo
echo "=== INJECTION CONTROL (the 'zero injection surface' claim) ==="
run_case "$WORK/block_real.sh" 'inject $(touch '"$WORK"'/PWNED) tail' "T10 -F body with \$( ) read LITERALLY" -F "$WORK/b_inject.txt" || fails=$((fails+1))
if [ -e "$WORK/PWNED" ]; then echo "FAIL  T11 command substitution EXECUTED from -F body"; fails=$((fails+1))
else echo "PASS  T11 no execution -- \$( ) in -F body never evaluated"; fi

echo
echo "=== MUTANT CONTROL (does this suite actually discriminate?) ==="
# On the mutant, T1 MUST fail (no -F read) and T4 MUST still pass (-m untouched).
if run_case "$WORK/block_mutant.sh" "hashed trailer reason" "M1 -F read on mutant (MUST FAIL)" -F "$WORK/b_hash.txt" >/dev/null 2>&1; then
  echo "FAIL  M1 mutant still read the -F override -- THE SUITE DOES NOT DISCRIMINATE"; fails=$((fails+1))
else
  echo "PASS  M1 mutant does NOT read -F override (suite discriminates; T1 measures the fix)"
fi
run_case "$WORK/block_mutant.sh" "m path reason" "M2 -m still works on mutant (additive proof)" -m "subj
system-current-override: m path reason" || fails=$((fails+1))

echo
echo "TOTAL FAILURES: $fails"
exit $fails
