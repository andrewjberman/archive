#!/usr/bin/env bash
# NFRA_CLDGRPH.TO-CG-D-9 limb (i) -- ONE UNATTENDED NIGHT.
# Author: 0.9.0_WK_NFRA_CLDGRPH~1. READS ONLY. No AWS mutation, no rebuild provoked.
#
# WINDOW (fixed by the issuer's AMENDMENT 2026-09-05 ~02:4xZ): 2026-09-04T21:00Z -> 2026-09-05T06:00Z.
# The night that counts is 2026-09-05: TO-CG-D-1's digest pins landed 2026-09-04 ~17:2xZ, so the
# 09-04 nightly ran on PRE-PIN bytes and ROUND_ANALYSIS.round3.md s.2 item 2 rules that out.
#
# ATTRIBUTION RULE: the night's vintage is identified by the 3-of-3 join
# (nodes_snapshot_id / edges_snapshot_id / nessie_commit_hash) between the derive's own
# MARKER_STAMPED log line and the projection manifest -- NEVER by "newest vintage".
# A producer stamp advanced the pointer to 2026-09-05T00:52:45.603017+00:00 the same night with
# NO derive in the window, and "newest" would have picked that wrong artifact.
#
# AMENDMENT 2026-09-05 (1.0.0_SA_CTO ruling @b8eaa3323b, D9-AC2 re-cut to the CAUSAL form).
# The second arm of limb (i) no longer asks "did any seat invoke anything" (a PROXY that failed at
# 2150 of 2150 only because the issuing seat was driving the round all night). It asks: DID ANY
# INVOCATION IN THE WINDOW CAUSE THE REBUILD. Two instrument defects are fixed here and must not
# be reintroduced:
#   (1) NEVER filter the telemetry by command text -- no row in org/mcp/agent_telemetry carries a
#       command or argument field (schema: agent/kind/session_id/tool/ts, tool = the tool NAME).
#       Such a filter reads 0 STRUCTURALLY and would certify a fully worked night as unattended.
#       Section 6 below prints the field list so the limit is visible, never asserted.
#   (2) NEVER classify starters by an enumeration of role NAMES. The prior face named two
#       legitimate starters; this window holds four, and a name-list classifier convicted a
#       chronos-scheduled producer as a human (row W1-S15). Section 7 classifies by PROVENANCE
#       FORM (startedBy naming a rule / schedule / pipe / service) and CORROBORATES each label
#       against CloudTrail's own unspoofable userIdentity.invokedBy, printing every per-row label
#       beside the count so the labels and the total must agree.
set -u

BUCKET=opal-313476888478-globgrph
AWS=.tools/aws
JQ=.tools/jq.exe
LO=2026-09-04T21:00:00Z
HI=2026-09-05T06:00:00Z
DERIVE_LOG_GROUP=/ecs/globgrph/derive-runner
# The telemetry log is GITIGNORED (.gitignore:261) and therefore absent from EVERY worktree.
# Reading it at the worktree path returns a FALSE ZERO. It lives in the parent workspace.
TELEMETRY_DIR="${TELEMETRY_DIR:-/c/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/agent_telemetry}"

echo "=== TO-CG-D-9 LIMB (i): ONE UNATTENDED NIGHT"
echo "WINDOW=${LO} -> ${HI}"
echo "READ_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

# ---------------------------------------------------------------- 1. the vintage list
echo "--- 1. projection/ vintages (full list, no head)"
VLIST=$("$AWS" s3api list-objects-v2 --bucket "$BUCKET" --prefix projection/ --delimiter / \
          --query 'CommonPrefixes[].Prefix' --output text | tr -d '\r' | tr '\t' '\n' \
          | sed -e 's#^projection/##' -e 's#/$##' | grep -v '^$')
VCOUNT=$(printf '%s\n' "$VLIST" | wc -l | tr -d ' ')
echo "VINTAGES_TOTAL=${VCOUNT}"
echo "--- vintages inside the window:"
printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi'
IN_WINDOW=$(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi' | wc -l | tr -d ' ')
echo "VINTAGES_IN_WINDOW=${IN_WINDOW}"
echo

# ------------------------------------- 2. CloudTrail, read ONCE: the causal instrument
# CloudTrail is the only durable record of WHO started each task: ECS describe-tasks ages a
# stopped task out in about an hour, so by the time this runs the task itself is gone. The
# night's derive task id is RECOVERED FROM THIS WINDOW (responseElements.tasks[].taskArn), never
# taken on trust from the issuer's face -- the issuer named be97f46226f74bae86b9cf853e78763c and
# this section either reproduces that id from the record or contradicts it out loud.
echo "--- 2. CloudTrail RunTask events in the window (the causal instrument, read once)"
CT=$("$AWS" cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=RunTask \
      --start-time "$LO" --end-time "$HI" --max-results 50 \
      --query 'Events[].CloudTrailEvent' --output text | tr -d '\r' | tr '\t' '\n' | grep -v '^$')
CT_N=$(printf '%s\n' "$CT" | grep -c .)
echo "RUNTASK_EVENTS_RETURNED=${CT_N} (API cap 50)"
if [ "$CT_N" -ge 50 ]; then echo "WARN: RESULT SET AT THE CAP -- the denominator may be TRUNCATED"; fi
echo "INSTRUMENT QUALIFIER: CloudTrail management-event delivery lags up to ~15 min; this window"
echo "  closed at ${HI} and is read after it, so no in-window event is undelivered."

DERIVE_EV=$(printf '%s\n' "$CT" | "$JQ" -c 'select((.requestParameters.taskDefinition|tostring)|test("derive-runner"))')
DERIVE_EV_N=$(printf '%s\n' "$DERIVE_EV" | grep -c .)
echo "DERIVE_RUNTASK_EVENTS_IN_WINDOW=${DERIVE_EV_N}"
DERIVE_TASK_ARN=$(printf '%s\n' "$DERIVE_EV" | "$JQ" -r '.responseElements.tasks[0].taskArn // "-"' | head -1)
DERIVE_TASK=${DERIVE_TASK_ARN##*/}
REBUILD_TRIGGER_V=$(printf '%s\n' "$DERIVE_EV" | "$JQ" -r '.requestParameters.startedBy // "-"' | head -1)
DERIVE_TD=$(printf '%s\n' "$DERIVE_EV" | "$JQ" -r '.requestParameters.taskDefinition // "-"' | head -1)
DERIVE_INVOKEDBY=$(printf '%s\n' "$DERIVE_EV" | "$JQ" -r '.userIdentity.invokedBy // "-"' | head -1)
DERIVE_EVTIME=$(printf '%s\n' "$DERIVE_EV" | "$JQ" -r '.eventTime' | head -1)
echo "  eventTime      = ${DERIVE_EVTIME}"
echo "  taskDefinition = ${DERIVE_TD}"
echo "  taskArn        = ${DERIVE_TASK_ARN}   (recovered FROM THE WINDOW)"
echo "  startedBy      = ${REBUILD_TRIGGER_V}"
echo "  invokedBy      = ${DERIVE_INVOKEDBY}   (CloudTrail-authored; the caller cannot set it)"
if [ "$DERIVE_TASK" = "be97f46226f74bae86b9cf853e78763c" ]; then
  echo "  ISSUER_TASK_ID_REPRODUCED=true  (the face's id matches the id read from the record)"
else
  echo "  ISSUER_TASK_ID_REPRODUCED=false CONTRADICTION: face said be97f46226f74bae86b9cf853e78763c, record says ${DERIVE_TASK}"
fi
DERIVE_LOG_STREAM="derive-runner/derive-runner/${DERIVE_TASK}"
REBUILD_TRIGGER=${REBUILD_TRIGGER_V}
echo "REBUILD_TRIGGER=${REBUILD_TRIGGER_V}"
echo

# ------------------------------------------------- 3. the derive's OWN marker (durable instrument)
# POSITIVE CONTROL for "exactly one derive ran in the window": list ALL derive streams with their
# event spans, so a zero is provably a zero and not a dead arm. (The aws shim emits CRLF; the
# previous revision of this control fed the trailing \r into a digit guard, which skipped every
# row and printed NOTHING -- a control that reads as silence. tr -d '\r' below is that fix.)
echo "--- 3. derive-runner log streams (durable; ECS has aged the task itself out)"
"$AWS" logs describe-log-streams --log-group-name "$DERIVE_LOG_GROUP" \
  --order-by LastEventTime --descending --max-items 8 \
  --query 'logStreams[].[logStreamName,firstEventTimestamp,lastEventTimestamp]' --output text \
  | tr -d '\r' \
  | DERIVE_TASK="$DERIVE_TASK" python "$(dirname "$0")/night_streams.py"
echo
echo "--- the night derive's own lines (marker + the bucket-notification denominator)"
DLOG=$("$AWS" logs get-log-events --log-group-name "$DERIVE_LOG_GROUP" \
        --log-stream-name "$DERIVE_LOG_STREAM" --start-from-head \
        --query 'events[].message' --output text | tr -d '\r' | tr '\t' '\n')
printf '%s\n' "$DLOG" | grep -E 'MARKER_STAMPED|buckets read=' | sed 's/^ *//' | sed 's/^/  /'
DENOM_LINE=$(printf '%s\n' "$DLOG" | grep -E 'buckets read=' | head -1 | sed 's/^ *//')
MARK_LINE=$(printf '%s\n' "$DLOG" | grep -E 'MARKER_STAMPED' | head -1)
D_HASH=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*hash=\([0-9a-f]*\).*/\1/p')
D_NSNAP=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*nodes_snap=\([0-9-]*\).*/\1/p')
D_ESNAP=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*edges_snap=\([0-9-]*\).*/\1/p')
echo "DERIVE_DENOMINATOR_LINE=${DENOM_LINE}"
echo

# ------------------------------------------------- 4. the 3-of-3 join: which vintage IS this derive's
echo "--- 4. attribute the vintage by the 3-of-3 snapshot join (NEVER by 'newest')"
NIGHT_VINTAGE=""
# The manifests are fetched in PARALLEL and then read in order: each aws shim start costs
# ~3 s on this box, and eight sequential fetches put the whole criterion invocation within
# a few seconds of its 120 s bound. Fetching concurrently changes no value that is read.
MTMP=$(mktemp -d)
WV=$(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi')
i=0
for v in $WV; do
  i=$((i+1))
  # stdout + SHELL redirection, never an aws-side destination path: the .tools/aws shim
  # converts a POSIX path only if it already EXISTS, so a not-yet-created output file is
  # handed to the Windows CLI unconverted and the fetch lands nowhere (measured here: eight
  # MANIFEST_UNREADABLE rows on a bucket that reads fine one call later).
  "$AWS" s3 cp "s3://${BUCKET}/projection/${v}/_build_manifest.json" - > "${MTMP}/m${i}.json" 2>/dev/null &
done
wait
i=0
for v in $WV; do
  i=$((i+1))
  M=$(cat "${MTMP}/m${i}.json" 2>/dev/null)
  [ -z "$M" ] && { echo "  ${v}  MANIFEST_UNREADABLE"; continue; }
  wid=$(printf '%s' "$M" | "$JQ" -r '.writer_id'); mode=$(printf '%s' "$M" | "$JQ" -r '.producer.mode')
  bat=$(printf '%s' "$M" | "$JQ" -r '.built_at')
  ns=$(printf '%s' "$M" | "$JQ" -r '.nodes_snapshot_id // "-"'); es=$(printf '%s' "$M" | "$JQ" -r '.edges_snapshot_id // "-"')
  nh=$(printf '%s' "$M" | "$JQ" -r '.nessie_commit_hash // "-"')
  j=0
  [ "$ns" = "$D_NSNAP" ] && j=$((j+1)); [ "$es" = "$D_ESNAP" ] && j=$((j+1)); [ "$nh" = "$D_HASH" ] && j=$((j+1))
  echo "  ${v}  writer=${wid} mode=${mode} built_at=${bat} JOIN=${j}/3"
  if [ "$j" -eq 3 ]; then NIGHT_VINTAGE="$v"; NIGHT_WRITER="$wid"; NIGHT_MODE="$mode"; NIGHT_BUILT="$bat"; fi
done
echo "MANIFESTS_READ=${i} of ${IN_WINDOW} in-window vintages"
rm -rf "$MTMP"
PREV_EVENING=$(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" '$0<lo' | sort | tail -1)
echo
echo "NIGHT_VINTAGE=${NIGHT_VINTAGE}"
echo "NIGHT_WRITER=${NIGHT_WRITER:-} NIGHT_MODE=${NIGHT_MODE:-} NIGHT_BUILT_AT=${NIGHT_BUILT:-}"
echo "PREV_EVENING=${PREV_EVENING}"
if [ "$NIGHT_VINTAGE" \> "$PREV_EVENING" ]; then echo "NIGHT_LATER_THAN_PREV_EVENING=true"; else echo "NIGHT_LATER_THAN_PREV_EVENING=false"; fi
echo
echo "--- THE CAUSAL CHAIN, end to end (each link a different instrument):"
echo "  projection manifest ${NIGHT_VINTAGE}"
echo "    <-3/3 snapshot join- MARKER_STAMPED in log stream ${DERIVE_LOG_STREAM}"
echo "      <-taskArn- CloudTrail RunTask ${DERIVE_EVTIME}"
echo "        <-startedBy- ${REBUILD_TRIGGER_V}"
echo

# ------------------------------------------------- 5. arm (a): the seat ACTIVITY census (context)
# RETAINED FOR THE RECORD, NOT AS THE ARM. Under the amendment this census no longer decides
# limb (i): a seat merely being ACTIVE does not void the arm, only a seat CAUSING a rebuild does.
echo "--- 5. seat ACTIVITY census -- org/mcp/agent_telemetry (context, not the arm)"
if [ ! -d "$TELEMETRY_DIR" ]; then
  echo "TELEMETRY_DIR_ABSENT=${TELEMETRY_DIR}"
  echo "SEAT_INVOCATIONS_IN_WINDOW=UNMEASURABLE of 0"
else
  echo "TELEMETRY_DIR=${TELEMETRY_DIR} (GITIGNORED at .gitignore:261 -- absent from every worktree;"
  echo "  reading it at the worktree path returns a FALSE ZERO, so the parent workspace is read)"
  python - "$TELEMETRY_DIR" "$LO" "$HI" <<'PYEOF'
import json, sys, os, glob, collections
d, lo, hi = sys.argv[1], sys.argv[2], sys.argv[3]
files = sorted(glob.glob(os.path.join(d, "*.jsonl")))
tot = 0
bys = collections.Counter()
keys = collections.Counter()
for f in files:
    with open(f, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            t = o.get("ts", "")
            if lo <= t < hi:
                tot += 1
                bys[o.get("serial") or o.get("agent") or "(none)"] += 1
                keys.update(o.keys())
print("  telemetry files scanned: %d" % len(files))
print("  FIELDS PRESENT ON WINDOW ROWS: %s" % ", ".join(sorted(keys)))
print("  INSTRUMENT LIMIT: no field carries the command text or arguments of a tool call.")
print("  A filter like 'rows naming kuzu|derive|projection|globgrph|run-task' is UNSATISFIABLE")
print("  on this log: it reads 0 for a STRUCTURAL reason (the field does not exist), not because")
print("  no seat touched the graph -- a vacuous zero that would certify a WORKED night as")
print("  unattended. This log can answer WHETHER SEATS WERE ACTIVE and nothing finer.")
print("  -- seats active in the window:")
for k, v in bys.most_common():
    print("       %-32s %d tool call(s)" % (k, v))
print("SEAT_INVOCATIONS_IN_WINDOW=%d of %d" % (tot, tot))
PYEOF
fi
echo

# ------------------------------------------------- 6. arm (b): DID ANY INVOCATION CAUSE A REBUILD
echo "--- 6. arm (b) CAUSAL: every task started in the window, classified BY PROVENANCE"
printf '%s\n' "$CT" | VLIST_ALL="$VLIST" python "$(dirname "$0")/night_classify.py"
echo

# ------------------------------------------------- 7. legacy arm (b) count, kept for continuity
echo "--- 7. the pre-amendment RunTask count, kept so the two frames can be compared"
LEGACY_NONPIPE=$(printf '%s\n' "$CT" | "$JQ" -r 'select((.requestParameters.startedBy // "-") | (test("^events-rule/") or test("^chronos-schedule/") or test("^ecs-svc/") or . == "Started by Eventbridge Pipes") | not) | .eventTime' | grep -c .)
echo "RUNTASK_NONPIPE_IN_WINDOW=${LEGACY_NONPIPE} of ${CT_N}"
echo "  (the pre-amendment arm; it counts a human-started task that constituted NO rebuild --"
echo "   a globgrph-trino query task -- which is exactly the PROXY the CTO's ruling replaced.)"
echo

# ------------------------------------------------- 8. THE CRITERION FIELDS
echo "=== CRITERION FIELDS"
echo "NIGHT_VINTAGE=${NIGHT_VINTAGE}"
echo "PREV_EVENING=${PREV_EVENING}"
echo "REBUILD_TRIGGER=${REBUILD_TRIGGER_V}"
