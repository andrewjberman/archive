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
CLIENT_FILE=infra/aws/globgrph/kuzu_cli.py

marker_iso() { "$AWS" s3 cp "s3://${BUCKET}/warehouse/_branch_head.main.json" - 2>/dev/null | "$JQ" -r '.committed_at_iso'; }
pointer_vintage() { "$AWS" s3 cp "s3://${BUCKET}/projection/current.json" - 2>/dev/null | "$JQ" -r '.vintage'; }
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
    M_QUICK=$(marker_iso)
    if [ "$M_QUICK" = "$LAST_MARKER" ] && [ "$SINCE_FULL" -lt 6 ]; then
      SINCE_FULL=$((SINCE_FULL+1))
      echo "  $(date -u +%H:%M:%SZ)  marker unchanged (${M_QUICK}) -- cheap poll, no client read"
      sleep 5
      continue
    fi
    [ -n "$LAST_MARKER" ] && [ "$M_QUICK" != "$LAST_MARKER" ] && echo "  >>> MARKER MOVED: ${LAST_MARKER} -> ${M_QUICK} -- reading the client NOW"
    LAST_MARKER="$M_QUICK"; SINCE_FULL=0
    NOW=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
    M=$(marker_iso); P_BEFORE=$(pointer_vintage)
    T_BEFORE=$(tasklist)
    IFS=$'\t' read -r SV SC AGE <<EOF
$(client_read)
EOF
    T_AFTER=$(tasklist); P_AFTER=$(pointer_vintage)
    BEHIND=false
    # string compare is sound: both are fixed-width canonical UTC ISO-8601 per PROJECTION_CONTRACT s.1
    if [ -n "$M" ] && [ -n "$SV" ] && [ "$M" \> "$SV" ]; then BEHIND=true; fi
    PMOVED=true; [ "$P_BEFORE" = "$P_AFTER" ] && PMOVED=false
    printf '{"read_at":"%s","marker":"%s","served":"%s","node_count":"%s","behind":%s,"pointer_before":"%s","pointer_after":"%s","pointer_moved_by_read":%s,"tasks_before":%s,"tasks_after":%s,"age_line":"%s"}\n' \
      "$NOW" "$M" "$SV" "$SC" "$BEHIND" "$P_BEFORE" "$P_AFTER" "$PMOVED" "$T_BEFORE" "$T_AFTER" "$AGE" >> "$EV"
    echo "  ${NOW}  marker=${M}  served=${SV}  BEHIND=${BEHIND}  pointer_moved_by_read=${PMOVED}"
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

B=$(grep '"behind":true' "$EV" | head -1)
if [ -z "$B" ]; then
  echo "BEHIND_CAUGHT=false"
  echo "BEHIND-NOT-CAUGHT in ${READS} reads over ${FIRST} -> ${LAST}"
  echo "--- every marker/served pair observed:"
  "$JQ" -r '"  " + .read_at + "  marker=" + .marker + "  served=" + .served' "$EV"
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
# The read moved nothing: TRUE only if EVERY behind-read left the pointer where it found it.
if grep '"behind":true' "$EV" | "$JQ" -r '.pointer_moved_by_read' | grep -q true; then
  echo "POINTER_MOVED_BY_READ=true"
else
  echo "POINTER_MOVED_BY_READ=false"
fi

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
