#!/usr/bin/env bash
###############################################################################################
# END-TO-END self-test for safe-commit-F-read-override-fix.
#
# Drives the REAL .tools/safe-commit.sh in isolated temp repos with a stubbed comp-system
# (rc via STUB_RC), so the override-read block actually runs. This covers argument parsing,
# the pathspec plumbing and the real commit -- coverage the block-level harnesses in
# deliverables/safe_commit_f_read/ do NOT have. That is why this file was repaired rather
# than deleted (CTO~Z disposition 173326Z).
#
#=============================================================================================
# !! THIS HARNESS USED TO FAIL OPEN. READ THIS BEFORE TRUSTING ANY GREEN FROM IT. !!
#
# ORIGINAL DEFECT (written 2026-07-21, found 2026-07-25 by 0.8.0_AE_CloudComp base):
#   `TMP="$(mktemp -d)"` was unchecked. Under the Cygwin harness /tmp is UNWRITABLE, so
#   mktemp failed, $TMP became EMPTY, every path collapsed to root-relative, and the setup
#   died -- yet the run still printed:
#
#       mkdir: cannot create directory '/repo_E1_F_stdin': Permission denied
#       line 27: /repo_E1_F_stdin/org/modules/graph/tf_E1_F_stdin.txt: No such file or directory
#       [PASS] E1_F_stdin  exit=1(exp 1)  audit-override=n(exp n)
#
#   42 setup-error lines in a run reporting PASS=3.
#
# THE GENERAL MECHANISM, which is the reusable part:
#   Every "expect BLOCK" case asserted `exit == 1`. A CATASTROPHICALLY BROKEN INVOCATION
#   ALSO EXITS 1. So the expected-failure cases were UNFALSIFIABLE -- they passed when the
#   gate correctly refused AND when the harness never ran the gate at all.
#   >> A NEGATIVE-RESULT TEST THAT CANNOT DISTINGUISH "THE THING UNDER TEST REFUSED" FROM
#      "MY OWN SETUP COLLAPSED" IS AN INSTRUMENT THAT CANNOT FAIL -- AND IT IS WORSE THAN NO
#      HARNESS, BECAUSE IT RENDERS GREEN. <<
#   The discriminator: assert the SIDE EFFECTS (audit-write, block path), not the exit code
#   alone -- and assert your own SETUP before you assert anything about the subject.
#
# CORRECTION, recorded because the first account of this was wrong and reached a commit
# message (@01c815ef8) via my report:
#   THE 07-21 "9/9 PASS" WAS ALMOST CERTAINLY GENUINE. It is NOT retired-as-fake.
#   Proof: the six expect-PASS cases assert `audit-override=y`, which requires safe-commit to
#   actually run and WRITE the audit file. A collapsed setup provably cannot produce that --
#   under collapse all six report audit=n and FAIL (exactly what happens today). For 07-21 to
#   have recorded 9/9, its setup must have WORKED. The defect is that this harness DEGRADES
#   SILENTLY when the environment changes underneath it -- not that it never measured anything.
#   I inferred "historical output unreliable" from "fails open today" without checking whether
#   the historical result was even ACHIEVABLE under the failure mode. It was not.
#
# REPAIR (2026-07-25): scratch dir is created explicitly and ABORTS LOUDLY if unavailable;
# every case ASSERTS ITS OWN SETUP (repo, fixture, output capture) before comparing rc, and
# reports [SETUP-FAIL] -- never [PASS] -- when its preconditions did not hold. `--prove-guard`
# exercises that the guard actually fires, so the repair is itself verified rather than
# asserted.
#=============================================================================================
set -u

SC="$(git rev-parse --show-toplevel 2>/dev/null)/.tools/safe-commit.sh"
[ -f "$SC" ] || { echo "SETUP-ABORT: cannot locate safe-commit.sh at [$SC]"; exit 9; }

HERE="$(cd "$(dirname "$0")" && pwd)"
# /tmp is unwritable under the Cygwin harness -- do NOT use mktemp here, and NEVER leave the
# scratch-dir creation unchecked. That omission is the entire original defect.
TMP="${SAFE_COMMIT_SELFTEST_TMP:-$HERE/.fread_e2e.$$}"

# SWEEP STALE SCRATCH FROM PRIOR RUNS, FIRST. An EXIT trap cannot survive SIGKILL -- a run
# killed by a timeout or a session kill leaves its scratch behind, and no trap can fix that
# from inside the dead process. So the NEXT run cleans up: self-healing beats a promise.
# (Measured 2026-07-25: a timeout-killed run left .fread_e2e.<pid>/ in the deliverables dir,
# and CTO~Z found a second one from another interrupted run. On a day spent finding orphaned
# artifacts, a self-test that litters when interrupted is the wrong instrument to ship.)
for _stale in "$HERE"/.fread_e2e.*; do
  [ -d "$_stale" ] || continue
  [ "$_stale" = "$TMP" ] && continue
  rm -rf "$_stale" 2>/dev/null && echo "swept stale scratch: $(basename "$_stale")"
done

rm -rf "$TMP"; mkdir -p "$TMP" 2>/dev/null || true
if [ ! -d "$TMP" ] || [ ! -w "$TMP" ]; then
  echo "SETUP-ABORT: scratch dir [$TMP] not creatable/writable -- REFUSING TO RUN."
  echo "  (This abort is the repair: the original harness continued here and printed PASS.)"
  exit 9
fi
# INT/TERM as well as EXIT -- covers a Ctrl-C or a timeout's SIGTERM. SIGKILL is uncatchable
# by design; the startup sweep above is what covers that case.
trap 'rm -rf "$TMP"' EXIT INT TERM

BIN="$TMP/bin"; mkdir -p "$BIN"
cat > "$BIN/comp-system" <<'EOF'
#!/usr/bin/env bash
echo "STUB comp-system: rc=${STUB_RC:-2} (simulated drift when 2)"
exit ${STUB_RC:-2}
EOF
chmod +x "$BIN/comp-system"
export PATH="$BIN:$PATH"

PASS=0; FAIL=0; SETUPFAIL=0

# run_case NAME EXPECT_RC EXPECT_AUDIT(y/n) STUB_RC -- <safe-commit args...>
run_case() {
  local name="$1" exp_rc="$2" exp_audit="$3" stub="$4"; shift 4
  [ "$1" = "--" ] && shift
  local repo="$TMP/repo_$name"
  local fixture="$repo/org/modules/graph/tf_$name.txt"
  local out="$TMP/out_$name"
  local audit="$repo/audit.log"

  mkdir -p "$repo/org/modules/graph" 2>/dev/null
  ( cd "$repo" && git init -q && git config user.email t@t && git config user.name t \
      && git commit -q --allow-empty -m init ) >/dev/null 2>&1
  printf 'content %s %s\n' "$name" "$RANDOM" > "$fixture" 2>/dev/null

  # ---- SETUP ASSERTION (the repair). Preconditions must hold BEFORE any claim about the
  # subject under test. Without this, "expect BLOCK" cases pass on total collapse.
  local why=""
  [ -d "$repo/.git" ]  || why="repo not initialised"
  [ -f "$fixture" ]    || why="${why:+$why; }fixture not created"
  ( : > "$out" ) 2>/dev/null || why="${why:+$why; }output capture not writable"
  if [ -n "$why" ]; then
    SETUPFAIL=$((SETUPFAIL+1))
    printf '[SETUP-FAIL] %-18s  %s -- NO CLAIM MADE about the subject under test\n' "$name" "$why"
    echo "     ----"
    return
  fi

  STUB_RC="$stub" SAFE_COMMIT_AUDIT_LOG="$audit" \
    bash -c 'cd "$1"; shift; bash "$@"' _ "$repo" "$SC" "$@" -- "org/modules/graph/tf_$name.txt" \
    >"$out" 2>&1
  local rc=$?
  local has_audit="n"; { [ -f "$audit" ] && grep -q 'SYSTEM-CURRENT-OVERRIDE' "$audit"; } && has_audit="y"
  local ok="PASS"
  { [ "$rc" = "$exp_rc" ] && [ "$has_audit" = "$exp_audit" ]; } || ok="FAIL"
  [ "$ok" = "PASS" ] && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
  printf '[%s] %-18s  exit=%s(exp %s)  audit-override=%s(exp %s)\n' \
         "$ok" "$name" "$rc" "$exp_rc" "$has_audit" "$exp_audit"
  sed 's/^/     | /' "$out"
  echo "     ----"
}

# ---- PROVE THE GUARD FIRES -------------------------------------------------------------
# A repair asserted is not a repair exercised. This forces the exact original failure --
# a case whose repo/fixture cannot be created -- and requires [SETUP-FAIL], not [PASS].
if [ "${1:-}" = "--prove-guard" ]; then
  echo "=== GUARD PROOF: force the ORIGINAL failure (uncreatable repo) ==="
  _real_tmp="$TMP"; TMP="/nonexistent_root_path_$$"
  before=$SETUPFAIL
  run_case G1_forced_collapse 1 n 2 -- --author "t <t@opal.agent>" -m "chore: subj only"
  TMP="$_real_tmp"
  if [ "$SETUPFAIL" -gt "$before" ]; then
    echo "GUARD PROOF: PASS -- collapsed setup reported SETUP-FAIL, not PASS."
    echo "  (The ORIGINAL harness printed [PASS] here: exp rc=1, and collapse also exits 1.)"
    exit 0
  fi
  echo "GUARD PROOF: FAIL -- collapse did not trip the setup assertion. The repair is not real."
  exit 1
fi

# ---- body files -------------------------------------------------------------------------
BF_TR="$TMP/body_trailer.txt"
printf 'chore(test): subject line\n\nbody text here\n# system-current-override: F-read-selftest reason\n' > "$BF_TR"
BF_PLAIN="$TMP/body_plain.txt"
printf 'chore(test): subject line\n\nbody text here\nsystem-current-override: F-read-plain reason\n' > "$BF_PLAIN"
BF_NO="$TMP/body_notrailer.txt"
printf 'chore(test): subject line\n\nbody text, no override trailer here\n' > "$BF_NO"

echo "=== POSITIVE CONTROL (no drift: rc0 -> commit proceeds regardless) ==="
run_case P0_nodrift_m       0 n 0 -- --author "t <t@opal.agent>" -m "chore: normal commit"

echo "=== LIMB A: the FIX -- -F body carries the override ==="
run_case A1_F_hash          0 y 2 -- --author "t <t@opal.agent>" -F "$BF_TR"
run_case A1b_F_plain        0 y 2 -- --author "t <t@opal.agent>" -F "$BF_PLAIN"
run_case A2_F_notrailer     1 n 2 -- --author "t <t@opal.agent>" -F "$BF_NO"
run_case A3_fileeq_hash     0 y 2 -- --author "t <t@opal.agent>" --file="$BF_TR"
run_case A4_longfile_hash   0 y 2 -- --author "t <t@opal.agent>" --file "$BF_TR"

echo "=== LIMB B: STRICTLY-ADDITIVE -- -m path byte-unchanged ==="
run_case B1_m_trailer       0 y 2 -- --author "t <t@opal.agent>" -m "chore: subj" -m "system-current-override: m-path reason"
run_case B2_m_notrailer     1 n 2 -- --author "t <t@opal.agent>" -m "chore: subj only"

echo "=== EDGE: -F - (stdin) must not crash; no trailer readable -> BLOCK ==="
run_case E1_F_stdin         1 n 2 -- --author "t <t@opal.agent>" -F -

echo ""
echo "SELF-TEST RESULT: PASS=$PASS FAIL=$FAIL SETUP-FAIL=$SETUPFAIL"
[ "$SETUPFAIL" = "0" ] || echo "  >> SETUP-FAIL is NOT a pass and NOT a fail of the subject -- the harness did not measure."
[ "$FAIL" = "0" ] && [ "$SETUPFAIL" = "0" ]
