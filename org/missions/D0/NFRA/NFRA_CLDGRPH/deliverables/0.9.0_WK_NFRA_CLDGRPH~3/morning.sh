#!/bin/bash
# morning.sh -- TO-CG-D-11 / cell CG-x-8 / criteria D11-AC1 + D11-AC3.
# THE MORNING READ: the operator status read taken on a real morning, plus the two negative
# controls that make "nothing was rerun" a measurement rather than an assumption.
#
# READS ONLY. No rerun, no rebuild, no stamp, no S3 write, no engine call. Every AWS call is a
# GET/HEAD. The plant fixture is not touched by this script (that is missed.sh).
#
# THREE HAZARDS THIS SCRIPT IS BUILT AGAINST, each paid for on TO-CG-D-9:
#  (1) row S57 -- NEVER 2>/dev/null a read whose EMPTINESS carries a verdict. Every read here
#      captures its rc and its stderr and PRINTS them; a failed read says READ_FAILED and can
#      never fall through to a number. PROCS=0 from a broken probe and PROCS=0 from a quiet
#      machine are different worlds and this script says which one it saw.
#  (2) row W1-S18 -- the .tools/aws shim emits CRLF, and a guard that does not strip the
#      trailing \r rejects every row and prints a clean-looking ZERO. Every shim read is
#      CR-stripped here and the raw bytes are printed beside the stripped value.
#  (3) row W1-S19 -- a BARE before-vs-after difference can convict a correct world. A producer
#      may legitimately move the pointer between the two reads; that has nothing to do with the
#      read. So the STRICT difference is printed on its own line, and the VERDICT line is the
#      attributed one: a move whose artifact was stamped before this read even started cannot
#      have been caused by this read.
#
# Usage:  bash morning.sh                 the real morning read (the criterion invocation)
#         bash morning.sh --selftest      the can-fail proof: the comparator and the proc probe
#                                         are fed inputs that MUST produce the other answer.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel)"
cd "$WS" || { echo "FATAL: cannot cd to workspace root"; exit 1; }

AWS_BIN="$WS/.tools/aws"
BUCKET="opal-313476888478-globgrph"
POINTER_KEY="projection/current.json"
PROC_PATTERN='kuzu_nessie_load|derive_runner|projection_worker'
POSITIVE_CONTROL_PATTERN='bash'
TMP="$WS/.scratch/d11"
mkdir -p "$TMP"

# ---------------------------------------------------------------------------------------------
# strip_cr -- hazard (2). The shim's stdout arrives CRLF; a bare compare or a numeric guard on
# that value fails on the invisible \r and the failure mode is SILENCE.
strip_cr() { printf '%s' "$1" | tr -d '\r'; }

# read_etag <label> -- hazard (1). Prints three lines: the rc, the raw bytes, the stripped value.
# On a non-zero rc or an empty body it sets the value to READ_FAILED(...), which is NOT an ETag
# and cannot be silently compared as one.
ETAG_VALUE=""
read_etag() {
  local label="$1" out rc err raw
  out="$(timeout 60 bash "$AWS_BIN" s3api head-object --bucket "$BUCKET" --key "$POINTER_KEY" \
        --query ETag --output text 2>"$TMP/etag_$label.err")"
  rc=$?
  err="$(cat "$TMP/etag_$label.err")"
  raw="$(printf '%s' "$out" | od -c | head -2 | tr '\n' ' ')"
  echo "  etag_read[$label] rc=$rc"
  echo "  etag_read[$label] raw_bytes=$raw"
  echo "  etag_read[$label] stderr=${err:-<empty>}"
  if [ "$rc" -ne 0 ] || [ -z "$out" ]; then
    ETAG_VALUE="READ_FAILED(rc=$rc)"
  else
    ETAG_VALUE="$(strip_cr "$out")"
  fi
  echo "  etag_read[$label] value=$ETAG_VALUE"
}

# count_procs <pattern> -- the ps -ef | grep trap. A bare `ps -ef | grep -c -E <pat>` counts the
# GREP PROCESS ITSELF and returns 1 (here: 2) where the truth is 0. The discipline is grep -v grep
# on a snapshot taken ONCE, with the snapshot's own rc and its ROW COUNT (the denominator) printed
# so a zero from a dead probe is distinguishable from a zero from a quiet machine.
PROC_COUNT=""
PROC_ROWS=""
count_procs() {
  local pattern="$1" snap rc rows n
  snap="$(ps -ef 2>"$TMP/ps.err")"
  rc=$?
  rows="$(printf '%s\n' "$snap" | wc -l | tr -d ' \r')"
  if [ "$rc" -ne 0 ] || [ "$rows" -lt 2 ]; then
    PROC_COUNT="UNREADABLE(ps rc=$rc rows=$rows)"
    PROC_ROWS="$rows"
    return
  fi
  n="$(printf '%s\n' "$snap" | grep -E "$pattern" | grep -v grep | wc -l | tr -d ' \r')"
  PROC_COUNT="$n"
  PROC_ROWS="$rows"
}

# attribute_pointer -- hazard (3). Given a pointer object, print WHOSE stamp it carries, read from
# the artifact's own manifest and not inferred from recency: vintage, writer_id, producer.mode,
# built_at, producer.source_commit. Sets ATTR_BUILT_AT / ATTR_WRITER.
ATTR_BUILT_AT=""
ATTR_WRITER=""
attribute_pointer() {
  local label="$1" rc
  timeout 60 bash "$AWS_BIN" s3api get-object --bucket "$BUCKET" --key "$POINTER_KEY" \
      "$TMP/pointer_$label.json" >"$TMP/pointer_$label.head" 2>"$TMP/pointer_$label.err"
  rc=$?
  echo "  attribute[$label] pointer_get rc=$rc stderr=$(cat "$TMP/pointer_$label.err")"
  if [ "$rc" -ne 0 ]; then ATTR_BUILT_AT="READ_FAILED"; ATTR_WRITER="READ_FAILED"; return; fi
  local mkey
  mkey="$(python -c "import json,sys;print(json.load(open(sys.argv[1]))['manifest_key'])" "$TMP/pointer_$label.json" 2>>"$TMP/pointer_$label.err")"
  echo "  attribute[$label] manifest_key=$mkey"
  timeout 60 bash "$AWS_BIN" s3api get-object --bucket "$BUCKET" --key "$mkey" \
      "$TMP/manifest_$label.json" >"$TMP/manifest_$label.head" 2>>"$TMP/pointer_$label.err"
  rc=$?
  echo "  attribute[$label] manifest_get rc=$rc"
  if [ "$rc" -ne 0 ]; then ATTR_BUILT_AT="READ_FAILED"; ATTR_WRITER="READ_FAILED"; return; fi
  ATTR_BUILT_AT="$(python -c "import json,sys;print(json.load(open(sys.argv[1]))['built_at'])" "$TMP/manifest_$label.json")"
  ATTR_WRITER="$(python -c "import json,sys;m=json.load(open(sys.argv[1]));print('%s mode=%s source_commit=%s' % (m.get('writer_id'),(m.get('producer') or {}).get('mode'),(m.get('producer') or {}).get('source_commit')))" "$TMP/manifest_$label.json")"
  echo "  attribute[$label] vintage=$(python -c "import json,sys;print(json.load(open(sys.argv[1]))['vintage'])" "$TMP/manifest_$label.json")"
  echo "  attribute[$label] writer=$ATTR_WRITER"
  echo "  attribute[$label] built_at=$ATTR_BUILT_AT"
}

# compare_etags <before> <after> -- pure function, so it can be exercised on inputs that MUST
# produce the other answer (--selftest). Echoes true|false for the STRICT difference.
compare_etags() { if [ "$1" = "$2" ]; then echo "false"; else echo "true"; fi; }

# =============================================================================================
if [ "${1:-}" = "--selftest" ]; then
  echo "== SELFTEST: the can-fail proof. A control whose failure mode is silence licenses the"
  echo "== arm above it (row W1-S18). These arms are shown returning the OTHER answer."
  echo "SELFTEST_COMPARATOR_SAME=$(compare_etags '\"aaa\"' '\"aaa\"')   (expect false)"
  echo "SELFTEST_COMPARATOR_DIFF=$(compare_etags '\"aaa\"' '\"bbb\"')   (expect true)"
  count_procs "$POSITIVE_CONTROL_PATTERN"
  echo "SELFTEST_PROCS_POSITIVE_CONTROL=$PROC_COUNT  pattern='$POSITIVE_CONTROL_PATTERN'  ps_rows=$PROC_ROWS"
  echo "== the proc probe is ALIVE: it returns non-zero on a pattern that IS running, so a zero"
  echo "== on the engine pattern is an ABSENCE and not a dead arm."
  echo "SELFTEST_BARE_GREP_TRAP=$(ps -ef | grep -c -E "$PROC_PATTERN")   (the trap: counts the grep itself)"
  echo "SELFTEST_DISCIPLINED=$(ps -ef | grep -E "$PROC_PATTERN" | grep -v grep | wc -l | tr -d ' \r')   (grep -v grep)"
  echo "SELFTEST_CR_STRIP_RAW=$(timeout 60 bash "$AWS_BIN" s3api head-object --bucket "$BUCKET" --key "$POINTER_KEY" --query ETag --output text | od -c | head -1)"
  exit 0
fi

echo "=============================================================================="
echo "MORNING READ -- TO-CG-D-11 / CG-x-8 / 0.9.0_WK_NFRA_CLDGRPH~3"
echo "READS ONLY: HEAD/GET on S3, one status read, one process snapshot. Nothing rerun."
echo "=============================================================================="
WALL_CLOCK="$(date -u +%FT%TZ)"
READ_START_EPOCH="$(date -u +%s)"
echo "WALL_CLOCK_UTC=$WALL_CLOCK"
echo "NIGHTLY_BOUNDARY_HOUR=02:00Z  (graph_status_cli.py:60, cron(0 2 * * ? *))"
echo "MORNING_TEST=the read is taken AFTER today's 02:00Z boundary on the calendar day it runs"
echo

echo "--- POINTER ETAG BEFORE (rc printed; a failed read says so and is never a number) ---"
read_etag before
ETAG_BEFORE="$ETAG_VALUE"
echo

echo "--- PROCESS TABLE BEFORE (grep -v grep discipline; denominator printed) ---"
count_procs "$PROC_PATTERN"
PROCS_BEFORE="$PROC_COUNT"
PROC_ROWS_BEFORE="$PROC_ROWS"
echo "  pattern='$PROC_PATTERN'  matches=$PROCS_BEFORE  ps_rows(denominator)=$PROC_ROWS_BEFORE"
echo

echo "--- POSITIVE CONTROL: the proc probe can return NON-ZERO (a zero is an absence, not a dead arm) ---"
count_procs "$POSITIVE_CONTROL_PATTERN"
PROC_POSITIVE="$PROC_COUNT"
echo "  pattern='$POSITIVE_CONTROL_PATTERN'  matches=$PROC_POSITIVE  ps_rows(denominator)=$PROC_ROWS"
echo

echo "--- THE READ: bash .tools/comp-graph status (whole output, verbatim) ---"
timeout 90 bash "$WS/.tools/comp-graph" status >"$TMP/status.out" 2>"$TMP/status.err"
STATUS_RC=$?
cat "$TMP/status.out"
echo "  status_rc=$STATUS_RC"
echo "  status_stderr=$(cat "$TMP/status.err")"
echo

echo "--- PROCESS TABLE AFTER ---"
count_procs "$PROC_PATTERN"
PROCS_AFTER="$PROC_COUNT"
PROC_ROWS_AFTER="$PROC_ROWS"
echo "  pattern='$PROC_PATTERN'  matches=$PROCS_AFTER  ps_rows(denominator)=$PROC_ROWS_AFTER"
echo

echo "--- POINTER ETAG AFTER ---"
read_etag after
ETAG_AFTER="$ETAG_VALUE"
echo

# --- the pointer verdict, hazard (3) -----------------------------------------------------------
STRICT_DIFFERS="$(compare_etags "$ETAG_BEFORE" "$ETAG_AFTER")"
ATTRIBUTION="n/a -- the pair is identical, so there is no movement to attribute"
MOVED_VERDICT="unset"
REREAD_NOTE="not needed -- the pair was stable on the first reading"

case "$ETAG_BEFORE$ETAG_AFTER" in
  *READ_FAILED*)
    MOVED_VERDICT="UNVERIFIABLE"
    ATTRIBUTION="a pointer read FAILED; an unread pair is not a stable pair (row S57 discipline)"
    ;;
  *)
    if [ "$STRICT_DIFFERS" = "false" ]; then
      MOVED_VERDICT="false"
    else
      echo "--- THE POINTER MOVED BETWEEN THE TWO READS: attributing it before verdicting ---"
      echo "  A producer may legitimately move the pointer between the reads and that has NOTHING"
      echo "  to do with this read (row W1-S19). The claim under test is that the READ moved"
      echo "  nothing, so the movement is attributed to its own stamp before any verdict."
      attribute_pointer after
      echo "  read_start_epoch=$READ_START_EPOCH  ($WALL_CLOCK)"
      # NOT silenced: this parse decides the attributed verdict, so its stderr and rc are PRINTED.
      STAMP_EPOCH="$(python -c "import sys,datetime;print(int(datetime.datetime.fromisoformat(sys.argv[1]).timestamp()))" "$ATTR_BUILT_AT" 2>"$TMP/stamp_parse.err")"
      STAMP_RC=$?
      echo "  attributed_stamp_parse rc=$STAMP_RC stderr=$(cat "$TMP/stamp_parse.err")"
      echo "  attributed_stamp_epoch=${STAMP_EPOCH:-UNPARSEABLE}"
      echo "  --- RE-READING THE PAIR ONCE (the face's instruction) ---"
      read_etag reread_before
      RB="$ETAG_VALUE"
      timeout 90 bash "$WS/.tools/comp-graph" status >"$TMP/status2.out" 2>"$TMP/status2.err"
      echo "  reread_status_rc=$?"
      read_etag reread_after
      RA="$ETAG_VALUE"
      REREAD_NOTE="re-read pair: before=$RB after=$RA differs=$(compare_etags "$RB" "$RA")"
      if [ -n "$STAMP_EPOCH" ] && [ "$STAMP_EPOCH" -lt "$READ_START_EPOCH" ]; then
        MOVED_VERDICT="false"
        ATTRIBUTION="MOVED BY A PRODUCER, NOT BY THIS READ: the artifact the pointer now names was"
        ATTRIBUTION="$ATTRIBUTION stamped at $ATTR_BUILT_AT by $ATTR_WRITER, which PRECEDES this read's"
        ATTRIBUTION="$ATTRIBUTION start ($WALL_CLOCK). A read that began after the artifact was already"
        ATTRIBUTION="$ATTRIBUTION built cannot have caused it. Strict before/after printed above."
      else
        MOVED_VERDICT="true"
        ATTRIBUTION="MOVEMENT NOT ATTRIBUTABLE to a stamp that predates this read; failing closed."
      fi
    fi
    ;;
esac

echo "=============================================================================="
echo "MORNING_READ=$(grep -o 'REFRESHED LAST NIGHT: .*' "$TMP/status.out" | head -1)"
echo "MORNING_READ_VINTAGE=$(grep -A4 'projection.last_night' "$TMP/status.out" | grep -m1 'vintage:' | sed 's/^ *vintage: *//')"
echo "MORNING_READ_BOUNDARY=$(grep -m1 'boundary:' "$TMP/status.out" | sed 's/^ *boundary: *//')"
echo "STATUS_RC=$STATUS_RC"
echo "PROCS_BEFORE=$PROCS_BEFORE"
echo "PROCS_AFTER=$PROCS_AFTER"
echo "PROCS_POSITIVE_CONTROL=$PROC_POSITIVE  (the probe is alive; a zero above is an absence)"
echo "PS_ROWS_DENOMINATOR=$PROC_ROWS_BEFORE/$PROC_ROWS_AFTER"
if [ "$PROCS_BEFORE" = "0" ] && [ "$PROCS_AFTER" = "0" ]; then
  echo "PROCS=0"
else
  echo "PROCS=$PROCS_BEFORE/$PROCS_AFTER (NOT a clean zero -- read the two lines above)"
fi
echo "POINTER_ETAG_BEFORE=$ETAG_BEFORE"
echo "POINTER_ETAG_AFTER=$ETAG_AFTER"
echo "POINTER_ETAG_STRICT_DIFFERS=$STRICT_DIFFERS"
echo "POINTER_MOVEMENT_ATTRIBUTION=$ATTRIBUTION"
echo "POINTER_REREAD=$REREAD_NOTE"
echo "POINTER_MOVED_ACROSS_READS=$MOVED_VERDICT"
echo "=============================================================================="
exit 0
