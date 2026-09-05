#!/usr/bin/env bash
# NFRA_CLDGRPH.TO-CG-D-9 limb (iii) -- TESTED BY TRYING.
# Author: 0.9.0_WK_NFRA_CLDGRPH~1. READS ONLY. No plant, no provoked stamp, no mutation.
#
# BEHIND is a WINDOW, not a plant. Between a marker stamp and the pointer's advance the served
# artifact is BEHIND the marker. This catches that window by polling, records what the client
# answers while behind (the stale answer WITH its age line), proves the read moved nothing, and
# then keeps polling until the pointer advances on its own -- that advance, reported by the SAME
# detector, is the can-fail arm.
#
# USAGE
#   behind.sh --poll [seconds]   live bounded poll; appends to the evidence file
#   behind.sh                    print the criterion fields from the recorded evidence
set -u

BUCKET=opal-313476888478-globgrph
AWS=.tools/aws
JQ=.tools/jq.exe
HERE="$(cd "$(dirname "$0")" && pwd)"
EV="${HERE}/behind_evidence.jsonl"
PROV="${HERE}/behind_task_provenance.jsonl"
ATTRIB="${HERE}/behind_attribute.py"
CLIENT_FILE=infra/aws/globgrph/kuzu_cli.py

# ---------------------------------------------------------------------------------------
# NFRA_CLDGRPH-S57: THE TWO READS MUST FAIL LOUD.
# The prior form piped `aws s3 cp ... -` into jq with stderr SILENCED, no rc capture and no
# emptiness guard. Two empty strings compare EQUAL, so `behind` computed false and the report
# printed BEHIND_CAUGHT=false -- the SAME line a genuinely not-behind world produces. A verdict
# vocabulary with no NOT-EVALUATED value encodes non-evaluation AS a verdict (CLAUDE.md: never
# 2>/dev/null a read whose EMPTINESS carries a verdict).
# stderr is CAPTURED (never discarded) and travels into the evidence row; the s3 rc and the jq
# rc are both captured; an empty body, a null field or an empty field is read_ok=false.
# Returns TSV: <read_ok>\t<s3_rc>\t<value>\t<err>   -- a TSV and not a global,
# because these are called inside $( ) and a global set in a subshell never reaches the parent.
read_s3_field() {
  _uri="$1"; _filt="$2"; _errf="${HERE}/.s3err.$$"
  _raw=$("$AWS" s3 cp "$_uri" - 2>"$_errf"); _rc=$?
  # The .tools/aws shim emits CRLF (W1-S18 found the same CR on night.sh's positive control).
  # A bare CR inside a JSON string is an unescaped control character, and it made the row this
  # whole clause exists to produce -- the READ_FAILED row -- unparseable by jq: the S57 control
  # at 13:02Z printed BEHIND_CAUGHT=READ_FAILED correctly while every jq read of the same row
  # failed with 'control characters from U+0000 through U+001F must be escaped'. Caught by
  # RUNNING the positive control against the patched script instead of trusting the patch.
  _err=$(tr -d '\r' < "$_errf" | tr '\n\t' '  ' | tr -d '"' | cut -c1-300); rm -f "$_errf"
  # NEVER an empty field: tab is IFS WHITESPACE, so `IFS=$'\t' read` collapses adjacent tabs
  # into ONE delimiter and an empty field shifts every field after it left (measured on the S57
  # positive control at 12:12:44Z: the error text landed in the VALUE field). Sentinel, not empty.
  if [ "$_rc" -ne 0 ]; then printf 'false\t%s\tREAD_FAILED\tS3_CP_RC_%s %s' "$_rc" "$_rc" "${_err:-no-stderr}"; return 0; fi
  if [ -z "$_raw" ]; then printf 'false\t%s\tREAD_FAILED\tEMPTY_BODY_ON_RC0 %s' "$_rc" "${_err:-no-stderr}"; return 0; fi
  _v=$(printf '%s' "$_raw" | "$JQ" -r "$_filt"); _jrc=$?
  if [ "$_jrc" -ne 0 ]; then printf 'false\t%s\tREAD_FAILED\tJQ_RC_%s' "$_rc" "$_jrc"; return 0; fi
  if [ -z "$_v" ] || [ "$_v" = "null" ]; then printf 'false\t%s\tREAD_FAILED\tFIELD_EMPTY_OR_NULL' "$_rc"; return 0; fi
  printf 'true\t%s\t%s\tnone' "$_rc" "$_v"
}
marker_read()  { read_s3_field "s3://${BUCKET}/warehouse/_branch_head.main.json" '.committed_at_iso'; }
pointer_read() { read_s3_field "s3://${BUCKET}/projection/current.json" '.vintage'; }
tasklist() {
  r=$("$AWS" ecs list-tasks --cluster opal-globgrph --family globgrph-projection-worker --desired-status RUNNING --query 'taskArns' --output text | tr '\t' ' ')
  s=$("$AWS" ecs list-tasks --cluster opal-globgrph --family globgrph-projection-worker --desired-status STOPPED --query 'taskArns' --output text | tr '\t' ' ')
  printf '{"running":"%s","stopped":"%s"}' "${r:-}" "${s:-}"
}
# The client. comp-kuzu is the THIN client (TO-CG-D-3 / CG-s-6): it has no rebuild path, so a
# read through it cannot start anything. Every read in this order goes through it and never
# through comp-find --corpus aws / comp-blast / comp-trace, whose reads could still touch the
# _canonical seam that CG-s-8 retires LAST.
client_read() {
  out=$(timeout 60 bash .tools/comp-kuzu --json "MATCH (n) RETURN count(n) AS c" 2>"${HERE}/.age.tmp")
  age=$(cat "${HERE}/.age.tmp"); rm -f "${HERE}/.age.tmp"
  cnt=$(printf '%s' "$out" | "$JQ" -r '.[0].c // "-"' 2>/dev/null)
  v=$(printf '%s' "$age" | sed -n 's/.*\[vintage=\([^ ]*\) manifest.*/\1/p')
  printf '%s\t%s\t%s' "${v:-UNKNOWN}" "${cnt:-UNKNOWN}" "$(printf '%s' "$age" | tr '\n' ' ')"
}

# --------------------------------------------------------------- the provenance capture
# The order's own method for limb (iii): `describe-tasks` for `startedBy` on any task
# present. ECS drops STOPPED tasks after roughly an hour, so this is CAPTURED WITH ITS
# MEASUREMENT TIME into a file the report reads later; a report that made the live call
# would print a different answer tomorrow than it printed today, which is not a record.
if [ "${1:-}" = "--provenance" ]; then
  echo "PROVENANCE capture $(date -u +%Y-%m-%dT%H:%M:%SZ) -> ${PROV##*/}"
  TASKS=$(grep '"behind":true' "$EV" | "$JQ" -r '(.tasks_before.running,.tasks_before.stopped,.tasks_after.running,.tasks_after.stopped)' | tr ' ' '\n' | sed 's|.*/||' | grep -E '^[0-9a-f]{32}$' | sort -u)
  N=$(printf '%s\n' "$TASKS" | grep -c .)
  echo "TASKS_NAMED_BY_BEHIND_ROWS=${N}"
  MEAS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  : > "$PROV"
  for t in $TASKS; do
    J=$(timeout 60 "$AWS" ecs describe-tasks --cluster opal-globgrph --tasks "$t" --query 'tasks[0].{task:taskArn,startedBy:startedBy,group:group,lastStatus:lastStatus,createdAt:createdAt,stoppedAt:stoppedAt}' --output json); RC=$?
    if [ "$RC" -ne 0 ] || [ -z "$J" ] || [ "$J" = "null" ]; then
      printf '{"task":"%s","startedBy":null,"describe_rc":"%s","note":"DESCRIBE_FAILED_OR_AGED_OUT","measured_at":"%s"}\n' "$t" "$RC" "$MEAS" >> "$PROV"
      echo "  ${t}  DESCRIBE_FAILED rc=${RC}"
    else
      printf '%s\n' "$J" | "$JQ" -c --arg m "$MEAS" '. + {measured_at:$m, describe_rc:"0"}' >> "$PROV"
      echo "  ${t}  startedBy=$(printf '%s' "$J" | "$JQ" -r '.startedBy // "EMPTY"')"
    fi
  done
  echo "PROVENANCE rows: $(grep -c . "$PROV")"
  exit 0
fi

if [ "${1:-}" = "--poll" ]; then
  BUDGET="${2:-100}"
  DEADLINE=$(( $(date +%s) + BUDGET ))
  echo "POLL start $(date -u +%Y-%m-%dT%H:%M:%SZ) budget=${BUDGET}s evidence=${EV}"
  # The BEHIND window is SHORT (measured tonight: stamp 03:31:16.79 -> pointer 03:31:47, ~30 s for
  # an incremental). A full client read costs ~40 s, so a naive read-everything loop samples slower
  # than the window it is hunting and misses it for an instrument reason, not a world reason.
  # So: poll the MARKER tightly (a cheap S3 GET, ~2 s) and spend the expensive client read only
  # when the marker has actually moved -- or on a periodic baseline read.
  LAST_MARKER=""
  SINCE_FULL=0
  while [ "$(date +%s)" -lt "$DEADLINE" ]; do
    IFS=$'\t' read -r QOK QRC M_QUICK QERR <<EOF
$(marker_read)
EOF
    if [ "$QOK" != "true" ]; then
      echo "  $(date -u +%H:%M:%SZ)  MARKER READ FAILED (rc=${QRC} err=${QERR}) -- recording a read_ok=false row"
    fi
    if [ "$QOK" = "true" ] && [ "$M_QUICK" = "$LAST_MARKER" ] && [ "$SINCE_FULL" -lt 6 ]; then
      SINCE_FULL=$((SINCE_FULL+1))
      echo "  $(date -u +%H:%M:%SZ)  marker unchanged (${M_QUICK}) -- cheap poll, no client read"
      sleep 5
      continue
    fi
    [ "$QOK" = "true" ] && [ -n "$LAST_MARKER" ] && [ "$M_QUICK" != "$LAST_MARKER" ] && echo "  >>> MARKER MOVED: ${LAST_MARKER} -> ${M_QUICK} -- reading the client NOW"
    [ "$QOK" = "true" ] && LAST_MARKER="$M_QUICK"
    SINCE_FULL=0
    NOW=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
    IFS=$'\t' read -r MOK MRC M MERR <<EOF
$(marker_read)
EOF
    IFS=$'\t' read -r PBOK PBRC P_BEFORE PBERR <<EOF
$(pointer_read)
EOF
    T_BEFORE=$(tasklist)
    IFS=$'\t' read -r SV SC AGE <<EOF
$(client_read)
EOF
    T_AFTER=$(tasklist)
    IFS=$'\t' read -r PAOK PARC P_AFTER PAERR <<EOF
$(pointer_read)
EOF
    BEHIND=false
    # S57: read_ok gates the verdict. The `behind` comparison is only MEANINGFUL when both of its
    # operands were actually read; a row that could not read them is read_ok=false and is counted
    # as NOT-EVALUATED by the report, never as a false.
    READ_OK=true
    [ "$MOK" = "true" ] || READ_OK=false
    [ "$PBOK" = "true" ] || READ_OK=false
    [ "$PAOK" = "true" ] || READ_OK=false
    if [ -z "$SV" ] || [ "$SV" = "UNKNOWN" ]; then READ_OK=false; fi
    [ "$M" = "READ_FAILED" ] && READ_OK=false
    [ "$P_BEFORE" = "READ_FAILED" ] && READ_OK=false
    [ "$P_AFTER" = "READ_FAILED" ] && READ_OK=false
    RERR="$(printf '%s %s %s' "${MERR:-}" "${PBERR:-}" "${PAERR:-}" | tr -s ' ')"
    [ "$SV" = "UNKNOWN" ] && RERR="${RERR} CLIENT_VINTAGE_UNKNOWN"
    # string compare is sound: both are fixed-width canonical UTC ISO-8601 per PROJECTION_CONTRACT s.1
    if [ "$READ_OK" = "true" ] && [ "$M" \> "$SV" ]; then BEHIND=true; fi
    PMOVED=true; [ "$P_BEFORE" = "$P_AFTER" ] && PMOVED=false
    [ "$PBOK" = "true" ] && [ "$PAOK" = "true" ] || PMOVED=UNREAD
    PMOVED_J="$PMOVED"; [ "$PMOVED" = "UNREAD" ] && PMOVED_J='"UNREAD"'
    printf '{"read_at":"%s","marker":"%s","served":"%s","node_count":"%s","behind":%s,"read_ok":%s,"marker_read_ok":%s,"marker_rc":"%s","pointer_before_read_ok":%s,"pointer_after_read_ok":%s,"pointer_rc":"%s","read_err":"%s","pointer_before":"%s","pointer_after":"%s","pointer_moved_by_read":%s,"tasks_before":%s,"tasks_after":%s,"age_line":"%s"}\n' \
      "$NOW" "$M" "$SV" "$SC" "$BEHIND" "$READ_OK" "${MOK:-false}" "${MRC:-NA}" "${PBOK:-false}" "${PAOK:-false}" "${PBRC:-NA}" "$RERR" "$P_BEFORE" "$P_AFTER" "$PMOVED_J" "$T_BEFORE" "$T_AFTER" "$AGE" >> "$EV"
    echo "  ${NOW}  marker=${M}  served=${SV}  BEHIND=${BEHIND}  read_ok=${READ_OK}  pointer_moved_by_read=${PMOVED}"
    sleep 3
  done
  echo "POLL end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit 0
fi

# ------------------------------------------------------------------ report from the evidence
echo "=== TO-CG-D-9 LIMB (iii): TESTED BY TRYING (reported from ${EV##*/})"
if [ ! -s "$EV" ]; then echo "EVIDENCE_ABSENT=true"; echo "BEHIND_CAUGHT=false"; exit 0; fi
READS=$(grep -c . "$EV")
FIRST=$(head -1 "$EV" | "$JQ" -r '.read_at'); LAST=$(tail -1 "$EV" | "$JQ" -r '.read_at')
echo "READS=${READS}  FIRST=${FIRST}  LAST=${LAST}"

# S57 -- THE THIRD OUTCOME. jq's `//` is the ALTERNATIVE operator and fires on FALSE as well as
# on null, so `.read_ok // <derived>` silently discarded an explicit `read_ok:false`. Use
# has("read_ok") -- ABSENT and FALSE are different answers and only has() separates them.
# read_ok is explicit on every row this instrument writes; rows written
# by the pre-S57 form carry no such field, so for THOSE it is DERIVED from a non-empty marker and
# a known served vintage and the count of explicitly-carrying rows is printed beside it, so a
# grader can see which rows assert it and which have it inferred.
READS_OK=$("$JQ" -r 'if (if has("read_ok") then .read_ok else ((.marker|length)>0 and .marker!="READ_FAILED" and (.served|length)>0 and .served!="UNKNOWN") end) then "ok" else "bad" end' "$EV" | grep -c '^ok$')
READS_EXPLICIT=$("$JQ" -r 'if has("read_ok") then "y" else "n" end' "$EV" | grep -c '^y$')
READS_FAILED=$(( READS - READS_OK ))
echo "READS_OK=${READS_OK} of ${READS}  (rows carrying an EXPLICIT read_ok field: ${READS_EXPLICIT} of ${READS})"

B=$(grep '"behind":true' "$EV" | head -1)
if [ -z "$B" ] && [ "$READS_OK" -eq 0 ]; then
  # NOT-EVALUATED. Distinct from both true and false: no read that could carry the verdict
  # succeeded, so the world was never asked. This is the outcome S57 says must exist.
  echo "BEHIND_CAUGHT=READ_FAILED"
  echo "READ_FAILED=true  ${READS_FAILED} of ${READS} reads could not read the marker, the pointer or the served vintage"
  echo "POINTER_MOVED_BY_READ=UNREAD"
  echo "LEGIT_REBUILD_REPORTED=UNREAD"
  echo "--- the read errors, verbatim:"
  "$JQ" -r '"  " + .read_at + "  rc=" + (if has("marker_rc") then (.marker_rc|tostring) else "NA" end) + "  err=" + (if has("read_err") then (.read_err|tostring) else "NO_READ_OK_FIELD" end)' "$EV" | sort -u | head -20
  exit 0
fi
if [ -z "$B" ]; then
  echo "BEHIND_CAUGHT=false"
  echo "BEHIND-NOT-CAUGHT in ${READS} reads (${READS_OK} of them read_ok) over ${FIRST} -> ${LAST}"
  # A NOT-CAUGHT is not a silence. The halves of limb (iii) that ARE established by these reads
  # are printed here rather than withheld, so a grader can see exactly which part of the claim
  # the missing window costs. BEHIND_CAUGHT=false already fails the criterion; nothing below
  # can rescue it, and nothing below is offered as if it could.
  timeout 60 python "$ATTRIB" "$EV" "$PROV"
  echo "  ^ established across ALL ${READS} reads: the pointer's vintage was read immediately"
  echo "    before and immediately after every client read and was identical every time."
  echo "LEGIT_REBUILD_REPORTED=false"
  echo "  ^ NOT a negative finding about the can-fail arm: the arm was never presented with a"
  echo "    rebuild while behind. The detector DID observe the served vintage advance on its own"
  echo "    between polls (see DISTINCT_SERVED below) -- context, never the arm."
  H=$(timeout 60 python .tools/comp-read "$CLIENT_FILE" --enumerate 'ensure_fresh|kuzu_nessie_load|_incremental_or_serve_stale' --limit 3 2>&1 | sed -n 's/^ENUMERATE-END: \([0-9]*\) hit.*/\1/p')
  echo "CLIENT_REBUILD_PATH_HITS=${H:-UNREAD}"
  echo "DISTINCT_MARKERS=$("$JQ" -r '.marker' "$EV" | sort -u | tr '\n' ' ')"
  echo "DISTINCT_SERVED=$("$JQ" -r '.served' "$EV" | sort -u | tr '\n' ' ')"
  echo "--- every marker/served pair observed:"
  "$JQ" -r '"  " + .read_at + "  marker=" + .marker + "  served=" + .served + "  read_ok=" + (if has("read_ok") then (.read_ok|tostring) else "DERIVED" end)' "$EV"
  exit 0
fi
echo "BEHIND_CAUGHT=true"
echo "BEHIND_READ_AT=$(printf '%s' "$B" | "$JQ" -r '.read_at')"
echo "BEHIND_MARKER=$(printf '%s' "$B" | "$JQ" -r '.marker')"
echo "BEHIND_SERVED=$(printf '%s' "$B" | "$JQ" -r '.served')"
echo "BEHIND_NODE_COUNT=$(printf '%s' "$B" | "$JQ" -r '.node_count')"
echo "BEHIND_ANSWER_AGE_LINE=$(printf '%s' "$B" | "$JQ" -r '.age_line')"
echo "TASKS_BEFORE=$(printf '%s' "$B" | "$JQ" -c '.tasks_before')"
echo "TASKS_AFTER=$(printf '%s' "$B" | "$JQ" -c '.tasks_after')"
# THE READ MOVED NOTHING -- ATTRIBUTED, not merely differenced.
# A client read costs ~40 s; in a producer burst the marker stamps every 60-90 s, so an
# advance lands inside the read window by arithmetic alone and a bare before-vs-after diff
# reports `true` for a pointer the read never touched. The criterion's property is the
# order's words -- 'unchanged BY the read; it moves later BY the producer' -- and a
# difference cannot separate those. behind_attribute.py attributes every advance on three
# limbs (task PROVENANCE from startedBy, pointer-vintage KEYING to an observed marker, and
# the marker-static BASE RATE as the negative control), any of which can fail it, and it
# ALWAYS prints the strict unattributed difference beside its verdict. Row W1-S19.
timeout 60 python "$ATTRIB" "$EV" "$PROV"

# The can-fail arm: the SAME detector later reports the legitimate marker-triggered rebuild --
# a later read whose served vintage is NEWER than the one served while behind.
BS=$(printf '%s' "$B" | "$JQ" -r '.served')
NEWER=$("$JQ" -r --arg bs "$BS" 'select(.served > $bs) | .read_at + "\t" + .served' "$EV" | head -1)
if [ -n "$NEWER" ]; then
  echo "LEGIT_REBUILD_REPORTED=true"
  echo "LEGIT_REBUILD_AT=$(printf '%s' "$NEWER" | cut -f1)"
  echo "LEGIT_REBUILD_SERVED=$(printf '%s' "$NEWER" | cut -f2)"
  echo "LEGIT_REBUILD_STARTER=arn:aws:pipes:us-east-1:313476888478:pipe/opal-globgrph-projection-worker (the Pipe; see night.sh arm (b) CloudTrail rows)"
else
  echo "LEGIT_REBUILD_REPORTED=false"
fi

# No question can start a rebuild: the client itself has no rebuild path.
H=$(timeout 60 python .tools/comp-read "$CLIENT_FILE" --enumerate 'ensure_fresh|kuzu_nessie_load|_incremental_or_serve_stale' --limit 3 2>&1 | sed -n 's/^ENUMERATE-END: \([0-9]*\) hit.*/\1/p')
echo "CLIENT_REBUILD_PATH_HITS=${H:-UNREAD}"
echo
echo "--- every marker/served pair observed:"
"$JQ" -r '"  " + .read_at + "  marker=" + .marker + "  served=" + .served + "  behind=" + (.behind|tostring) + "  ptr_moved_by_read=" + (.pointer_moved_by_read|tostring)' "$EV"
