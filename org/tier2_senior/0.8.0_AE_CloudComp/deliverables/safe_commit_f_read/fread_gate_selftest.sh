#!/usr/bin/env bash
# EXTENDED self-test for TO safe-commit-F-read-override-fix -- closes the residual that
# fread_selftest.sh explicitly did NOT cover, and adds the two SUBTLE mutants CVO~Z asked for
# (3.0.0_SA_CVO~Z, 170141Z: "keep M1, add the two subtle ones" + "there is likely a safe route
# via an isolated fixture rather than the live gate; that is what I would spend the pass on").
#
# WHAT THIS COVERS THAT THE FIRST HARNESS DID NOT:
#   the :530 TRIGGER PREDICATE · the comp-system rc=2 BRANCH · the AUDIT-LOG WRITE ·
#   the git-reset + exit-1 BLOCK path · the rc=1 fail-safe · the AGE-WARN path
#
# HOW IT REACHES rc=2 WITHOUT ARMING THE LIVE GATE (the whole point):
#   safe-commit.sh resolves the gate tool through PATH (`command -v comp-system`) and honours
#   SAFE_COMMIT_AUDIT_LOG for the audit sink. Those are two isolation seams the script already
#   provides. So we prepend a STUB comp-system whose rc we control, point the audit log into a
#   scratch dir, and run the block inside a THROWAWAY GIT REPO (so the block's real
#   `git reset -q HEAD -- <f>` touches nothing that matters).
#   06_current_state is NEVER made stale. Making the real gate blocking to test our own change
#   would be an outage, not a control.
#
# FIDELITY: the block is extracted from the LIVE file by ANCHOR (never hardcoded line numbers,
# never retyped) and evaluated under `set -euo pipefail`, which safe-commit.sh sets at :30 --
# the block's own comment claims set-e-safety, so testing without it would test a different
# program.

set -uo pipefail
SC="$(git rev-parse --show-toplevel)/.tools/safe-commit.sh"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$HERE/.gate_work.$$"
rm -rf "$WORK"; mkdir -p "$WORK"; trap 'rm -rf "$WORK"' EXIT

# ---- extract the FULL gate block by anchor ------------------------------------------------
START="$(grep -n '^if \[ ${#PATHSPEC\[@\]} -gt 0 \]' "$SC" | head -1 | cut -d: -f1)"
END="$(grep -n '^# Proceed with the actual scoped commit' "$SC" | head -1 | cut -d: -f1)"
[ -n "$START" ] && [ -n "$END" ] || { echo "FATAL: could not anchor the gate block"; exit 9; }
END=$((END - 2))
sed -n "${START},${END}p" "$SC" > "$WORK/gate_real.sh"
grep -q '_cfk'  "$WORK/gate_real.sh" || { echo "FATAL: extracted block lacks the -F loop"; exit 9; }
grep -q 'CS_OVR' "$WORK/gate_real.sh" || { echo "FATAL: extracted block lacks the override extract"; exit 9; }
echo "BLOCK: real safe-commit.sh lines ${START}-${END} (anchored)"

# ---- the two SUBTLE mutants CVO~Z named ----------------------------------------------------
# S1: break ONLY the comment-marker sed  -> '# system-current-override:' must stop being read,
#     while a PLAIN trailer must still work. (A real edit would plausibly break exactly this.)
sed 's@s/\^\[\[:space:\]\]\*#\[\[:space:\]\]\*system-current-override:/system-current-override:/@s/^ZZZ_NEVER_MATCHES/system-current-override:/@' \
    "$WORK/gate_real.sh" > "$WORK/gate_s1.sh"
# S2: break ONLY the --file=<f> form -> -F <f> must still work, --file=<f> must stop working.
sed 's@\[ "\${_cfa#--file=}" != "\$_cfa" \]@[ "ZZZ" != "ZZZ" ]@' "$WORK/gate_real.sh" > "$WORK/gate_s2.sh"

changed () { ! cmp -s "$1" "$2"; }
changed "$WORK/gate_real.sh" "$WORK/gate_s1.sh" || { echo "FATAL: S1 mutant identical to real -- control is dead"; exit 9; }
changed "$WORK/gate_real.sh" "$WORK/gate_s2.sh" || { echo "FATAL: S2 mutant identical to real -- control is dead"; exit 9; }
echo "MUTANTS: S1 (comment-marker sed broken) + S2 (--file= form broken) both differ from real"
echo

# ---- stub comp-system on PATH --------------------------------------------------------------
mkdir -p "$WORK/bin"
cat > "$WORK/bin/comp-system" <<'STUB'
#!/usr/bin/env bash
echo "${STUB_OUT:-STUB comp-system: managed-region drift on 06_current_state (synthetic)}"
exit ${STUB_RC:-2}
STUB
chmod +x "$WORK/bin/comp-system"
export PATH="$WORK/bin:$PATH"

# ---- throwaway git repo so the block's real `git reset` is inert ---------------------------
REPO="$WORK/repo"; mkdir -p "$REPO/org/modules/graph"
git -C "$REPO" init -q
git -C "$REPO" config user.email t@t; git -C "$REPO" config user.name t
echo x > "$REPO/org/modules/graph/boundary_report.py"
git -C "$REPO" add -A; git -C "$REPO" commit -qm base

printf 'subject\n\n# system-current-override: fixture hashed reason\n' > "$WORK/b_hash.txt"
printf 'subject\n\nsystem-current-override: fixture plain reason\n'    > "$WORK/b_plain.txt"
printf 'subject\n\nno trailer here\n'                                  > "$WORK/b_none.txt"

# ---- runner: each case in its own subshell (the block calls `exit 1`) -----------------------
# echoes: <rc>|<audit-line-count>|<stderr-has-BLOCKED>
run_gate () {
  local blk="$1" rc_stub="$2" audit="$WORK/audit.$RANDOM.log"; shift 2
  local out err rc
  err="$(
    (
      cd "$REPO" || exit 90
      set -euo pipefail                      # FIDELITY: safe-commit.sh sets this at :30
      export STUB_RC="$rc_stub"; export STUB_OUT="${STUB_OUT:-}"
      AUDIT_LOG="$audit"; ISO_TS="1970-01-01T00:00:00Z"; AGENT="TESTAGENT"
      PATHSPEC=("$1"); shift
      COMMIT_ARGS=("$@")
      . "$blk"
    ) 2>&1
  )"; rc=$?
  local n=0; [ -f "$audit" ] && n="$(grep -c 'SYSTEM-CURRENT-OVERRIDE' "$audit" 2>/dev/null || echo 0)"
  local blocked=no; printf '%s' "$err" | grep -q 'BLOCKED' && blocked=yes
  local agewarn=no; printf '%s' "$err" | grep -q 'AGE-WARN' && agewarn=yes
  printf '%s|%s|%s|%s' "$rc" "$n" "$blocked" "$agewarn"
}

check () {  # $1=label $2=expected $3=got
  if [ "$3" = "$2" ]; then printf 'PASS  %-52s -> %s\n' "$1" "$3"; return 0
  else printf 'FAIL  %-52s -> got=[%s] want=[%s]\n' "$1" "$3" "$2"; return 1; fi
}

TP="org/modules/graph/boundary_report.py"     # matches the :530 trigger regex
NP="org/tier2_senior/somefile.md"             # does NOT match
fails=0

echo "=== REAL GATE BLOCK -- rc=2 branch, audit write, block path ==="
check "E1 rc2 + -F override  -> pass, AUDITED, no block" "0|1|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$TP" -F "$WORK/b_hash.txt")" || fails=$((fails+1))
check "E2 rc2 + -F plain trailer -> pass, AUDITED"       "0|1|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$TP" -F "$WORK/b_plain.txt")" || fails=$((fails+1))
check "E3 rc2 + -F no trailer -> BLOCKS, exit1, NO audit" "1|0|yes|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$TP" -F "$WORK/b_none.txt")" || fails=$((fails+1))
check "E4 rc2 + -m override -> pass, AUDITED (regression)" "0|1|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$TP" -m "s
system-current-override: m reason")" || fails=$((fails+1))
check "E5 rc2 + NO message at all -> BLOCKS"              "1|0|yes|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$TP")" || fails=$((fails+1))

echo
echo "=== TRIGGER PREDICATE + FAIL-SAFE branches ==="
check "E6 NON-trigger path, rc2 stub -> gate never runs"  "0|0|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 2 "$NP" -F "$WORK/b_none.txt")" || fails=$((fails+1))
check "E7 trigger path, rc=1 -> WARN, NOT blocking"       "0|0|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 1 "$TP" -F "$WORK/b_none.txt")" || fails=$((fails+1))
check "E8 trigger path, rc=0 -> clean pass"               "0|0|no|no" \
      "$(run_gate "$WORK/gate_real.sh" 0 "$TP" -F "$WORK/b_none.txt")" || fails=$((fails+1))
check "E9 rc=0 + AGE-WARN in output -> surfaced, no block" "0|0|no|yes" \
      "$(STUB_OUT='comp-system: AGE-WARN 06 is aging' run_gate "$WORK/gate_real.sh" 0 "$TP" -F "$WORK/b_none.txt")" || fails=$((fails+1))

echo
echo "=== SUBTLE MUTANTS (CVO~Z 170141Z) ==="
# S1: hashed trailer must now FAIL to override (blocks); plain must STILL work.
check "S1 hashed trailer on broken-sed mutant -> BLOCKS"  "1|0|yes|no" \
      "$(run_gate "$WORK/gate_s1.sh" 2 "$TP" -F "$WORK/b_hash.txt")" || fails=$((fails+1))
check "S1 plain trailer still honored (scoped mutation)"  "0|1|no|no" \
      "$(run_gate "$WORK/gate_s1.sh" 2 "$TP" -F "$WORK/b_plain.txt")" || fails=$((fails+1))
# S2: --file=<f> must now FAIL; -F <f> must STILL work.
check "S2 --file=<f> on broken-form mutant -> BLOCKS"     "1|0|yes|no" \
      "$(run_gate "$WORK/gate_s2.sh" 2 "$TP" "--file=$WORK/b_plain.txt")" || fails=$((fails+1))
check "S2 -F <f> still honored (scoped mutation)"         "0|1|no|no" \
      "$(run_gate "$WORK/gate_s2.sh" 2 "$TP" -F "$WORK/b_plain.txt")" || fails=$((fails+1))

echo
echo "TOTAL FAILURES: $fails"
exit $fails
