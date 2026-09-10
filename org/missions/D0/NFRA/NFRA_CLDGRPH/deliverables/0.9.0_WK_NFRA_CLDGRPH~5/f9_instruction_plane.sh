#!/usr/bin/env bash
# f9_instruction_plane.sh -- F9-AC2 prober. 0.9.0_WK_NFRA_CLDGRPH~5, TO-CG-F-9 (CG-s-29).
#
# Proves the INSTRUCTION plane is retired per R16:
#   - both hook files ABSENT at HEAD (git show rc!=0) beside positive controls
#     (the tombstone IS at HEAD; both files WERE at the last hash carrying them)
#   - the tombstone carries its six fields
#   - the SUPERSEDED block is present in .tools/stitch-refresh
#   - Andrew's 2026-07-07 words (lines 6-12) are BYTE-KEPT across the edit
#   - a planted tombstone with one field removed is CAUGHT by the same probe
# Reads only. No S3, no device file, no writes outside $TMPDIR.
set -u
WS="$(git rev-parse --show-toplevel 2>/dev/null)"; [ -n "$WS" ] || { echo "ERROR: no repo root"; exit 9; }
cd "$WS" || exit 9
TMP="${TMPDIR:-/tmp}"
HOOKSH=".tools/git-hooks/stitch-refresh-post-commit.sh"
INST=".tools/git-hooks/install-stitch-refresh.sh"
TOMB=".tools/git-hooks/stitch-refresh-post-commit.TOMBSTONE.md"
SR=".tools/stitch-refresh"

echo "F9-AC2 -- THE INSTRUCTION PLANE RETIRED PER R16"
echo "RUN_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "HEAD=$(git rev-parse HEAD)"

# --- the retiring commit and the last hash carrying the files (robust to later commits)
DEL="$(git log --full-history --diff-filter=D -1 --format=%H -- "$HOOKSH")"
LASTFULL="$(git rev-parse "$DEL^")"
LAST="$(echo "$LASTFULL" | cut -c1-10)"
echo "RETIRING_COMMIT=$DEL"
echo "LAST_HASH_CARRYING_FILES=$LAST"

at_head() { # prints true/false + the rc and git's own message (never 2>/dev/null on a verdict)
  local p="$1" out rc
  out="$(git show "HEAD:$p" 2>&1 >/dev/null)"
  rc=$?
  if [ "$rc" = "0" ]; then echo "true rc=$rc"; else echo "false rc=$rc msg=$(echo "$out" | head -1 | tr -d '\r')"; fi
}
echo "HOOK_SCRIPT_AT_HEAD=$(at_head "$HOOKSH")"
echo "INSTALLER_AT_HEAD=$(at_head "$INST")"
# POSITIVE CONTROLS: the same instrument must read true for a path that IS at HEAD,
# and true for these very paths at the last hash that carried them (so 'false' above
# is absence, not a typo and not a broken instrument).
echo "POSITIVE_CONTROL_TOMBSTONE_AT_HEAD=$(at_head "$TOMB")"
git show "$LASTFULL:$HOOKSH" >/dev/null 2>&1; echo "POSITIVE_CONTROL_HOOK_AT_LAST_HASH=$([ $? = 0 ] && echo true || echo false)"
git show "$LASTFULL:$INST" >/dev/null 2>&1; echo "POSITIVE_CONTROL_INSTALLER_AT_LAST_HASH=$([ $? = 0 ] && echo true || echo false)"

# --- the tombstone's six fields ------------------------------------------------
probe_tombstone() { # $1 = tombstone file; prints the comma-joined field names found
  local f="$1" found=""
  # 1) the 07-07 word quoted VERBATIM: the quoted block must equal the record's
  #    .tools/stitch-refresh lines 6-12 (the 07-07 paragraph), comment markers stripped.
  local want got
  want="$(git show "HEAD:$SR" | sed -n '6,12p' | sed 's/^# \{0,1\}//' | tr -d '\r')"
  got="$(sed -n '/^> Replaces the cloud stitch-produce/,/^> PORTAL_REPO_PAT/p' "$f" | sed 's/^> \{0,1\}//' | tr -d '\r')"
  [ -n "$got" ] && [ "$want" = "$got" ] && found="$found,superseded_word_verbatim"
  # 2) the later word
  cat "$f" | grep -q 'no machine is in the compile business' && cat "$f" | grep -q '2026-09-02' && found="$found,later_word"
  # 3) the ruling record
  cat "$f" | grep -q 'CTO_ADJUDICATION_NFRA_CLDGRPH_20260909T1856Z_S71_STITCH_KEY_ONE_WRITER.md' && found="$found,ruling_record"
  # 4) the last hash carrying the files
  cat "$f" | grep -q "$LAST" && found="$found,last_hash"
  # 5) the re-enable path
  cat "$f" | grep -q "git show $LAST:$HOOKSH" && cat "$f" | grep -q 'stitch-refresh-post-commit (installed' && found="$found,reenable_path"
  # 6) the S71 numbers
  cat "$f" | grep -q '552' && cat "$f" | grep -q '17:53:55Z' && found="$found,s71_numbers"
  echo "${found#,}"
}
echo "TOMBSTONE_NAMES=$(probe_tombstone "$TOMB")"

# --- the SUPERSEDED block + the byte-kept words --------------------------------
git show "HEAD:$SR" | grep -q '^# SUPERSEDED -- 2026-09-09' && echo "SUPERSEDED_BLOCK_PRESENT=true" || echo "SUPERSEDED_BLOCK_PRESENT=false"

# "kept verbatim" measured on the RECORD plane (parent bytes vs HEAD bytes, both LF)
P_BYTES="$(git show "$LASTFULL:$SR" | sed -n '6,12p' | md5sum | cut -d' ' -f1)"
H_BYTES="$(git show "HEAD:$SR" | sed -n '6,12p' | md5sum | cut -d' ' -f1)"
# and against the WORKING file, CR-stripped: this box is core.autocrlf=true, so the
# checkout is CRLF and the record is LF -- an unstripped compare would false-FAIL.
W_BYTES="$(sed -n '6,12p' "$SR" | tr -d '\r' | md5sum | cut -d' ' -f1)"
echo "PARENT_LINES_6_12_MD5=$P_BYTES"
echo "HEAD_LINES_6_12_MD5=$H_BYTES"
echo "WORKING_LINES_6_12_MD5_CR_STRIPPED=$W_BYTES"
if [ "$P_BYTES" = "$H_BYTES" ] && [ "$P_BYTES" = "$W_BYTES" ]; then
  echo "ORIGINAL_WORDS_BYTE_KEPT=true"
else
  echo "ORIGINAL_WORDS_BYTE_KEPT=false"
fi
# NEGATIVE CONTROL on that comparison: a neighbouring line MUST differ (line 32 is
# the first inserted line), or the md5 test is a constant.
N_PARENT="$(git show "$LASTFULL:$SR" | sed -n '32p' | md5sum | cut -d' ' -f1)"
N_HEAD="$(git show "HEAD:$SR" | sed -n '32p' | md5sum | cut -d' ' -f1)"
[ "$N_PARENT" != "$N_HEAD" ] && echo "BYTE_COMPARE_CONTROL=CAN-FAIL" || echo "BYTE_COMPARE_CONTROL=BROKEN"

# --- the planted tombstone control ---------------------------------------------
PLANT="$TMP/f9_planted_tombstone.$$.md"
cat "$TOMB" | grep -v "$LAST" > "$PLANT"
PLANTED_FIELDS="$(probe_tombstone "$PLANT")"
echo "PLANTED_TOMBSTONE_FIELDS=$PLANTED_FIELDS"
case ",$PLANTED_FIELDS," in
  *,last_hash,*) echo "TOMBSTONE_PROBE_CONTROL=BLIND" ;;
  *)             echo "TOMBSTONE_PROBE_CONTROL=FIRED" ;;
esac
rm -f "$PLANT" "$TMP/f9_ac2_err.$$"
exit 0
