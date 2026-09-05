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
set -u

BUCKET=opal-313476888478-globgrph
AWS=.tools/aws
JQ=.tools/jq.exe
LO=2026-09-04T21:00:00Z
HI=2026-09-05T06:00:00Z
DERIVE_TASK=be97f46226f74bae86b9cf853e78763c
DERIVE_LOG_GROUP=/ecs/globgrph/derive-runner
DERIVE_LOG_STREAM="derive-runner/derive-runner/${DERIVE_TASK}"
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
          --query 'CommonPrefixes[].Prefix' --output text | tr '\t' '\n' \
          | sed -e 's#^projection/##' -e 's#/$##' | grep -v '^$')
VCOUNT=$(printf '%s\n' "$VLIST" | wc -l | tr -d ' ')
echo "VINTAGES_TOTAL=${VCOUNT}"
echo "--- vintages inside the window:"
printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi'
IN_WINDOW=$(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi' | wc -l | tr -d ' ')
echo "VINTAGES_IN_WINDOW=${IN_WINDOW}"
echo

# ------------------------------------------------- 2. the derive's OWN marker (durable instrument)
# ECS describe-tasks has already aged the task out (~1h retention); CloudWatch Logs is durable.
# POSITIVE CONTROL for the "only one derive in the window" claim: list ALL derive streams and
# show their event spans, so a zero is provably a zero and not a dead arm.
echo "--- 2. derive-runner log streams (durable instrument; ECS has aged the task out)"
"$AWS" logs describe-log-streams --log-group-name "$DERIVE_LOG_GROUP" \
  --order-by LastEventTime --descending --max-items 8 \
  --query 'logStreams[].[logStreamName,firstEventTimestamp,lastEventTimestamp]' --output text \
  | while IFS=$'\t' read -r s f l; do
      [ -z "${s:-}" ] && continue
      # --max-items adds a trailing pagination token row; it has no numeric timestamps.
      case "${f:-}" in ''|*[!0-9]*) continue ;; esac
      case "${l:-}" in ''|*[!0-9]*) continue ;; esac
      fi_=$(python -c "import datetime,sys;print(datetime.datetime.fromtimestamp(int(sys.argv[1])/1000,datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))" "$f")
      li_=$(python -c "import datetime,sys;print(datetime.datetime.fromtimestamp(int(sys.argv[1])/1000,datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))" "$l")
      inw=OUT
      case "$fi_" in 2026-09-04T2[1-3]*|2026-09-05T0[0-5]*) inw=IN_WINDOW ;; esac
      echo "  ${inw}  ${s}  ${fi_} -> ${li_}"
    done
echo
echo "--- the night derive's own lines (marker + the bucket-notification denominator)"
DLOG=$("$AWS" logs get-log-events --log-group-name "$DERIVE_LOG_GROUP" \
        --log-stream-name "$DERIVE_LOG_STREAM" --start-from-head \
        --query 'events[].message' --output text | tr '\t' '\n')
printf '%s\n' "$DLOG" | grep -E 'MARKER_STAMPED|buckets read=' | sed 's/^ *//' | sed 's/^/  /'
DENOM_LINE=$(printf '%s\n' "$DLOG" | grep -E 'buckets read=' | head -1 | sed 's/^ *//')
MARK_LINE=$(printf '%s\n' "$DLOG" | grep -E 'MARKER_STAMPED' | head -1)
D_HASH=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*hash=\([0-9a-f]*\).*/\1/p')
D_NSNAP=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*nodes_snap=\([0-9-]*\).*/\1/p')
D_ESNAP=$(printf '%s\n' "$MARK_LINE" | sed -n 's/.*edges_snap=\([0-9-]*\).*/\1/p')
echo "DERIVE_DENOMINATOR_LINE=${DENOM_LINE}"
echo

# ------------------------------------------------- 3. the 3-of-3 join: which vintage IS this derive's
echo "--- 3. attribute the vintage by the 3-of-3 snapshot join (NEVER by 'newest')"
NIGHT_VINTAGE=""
for v in $(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" -v hi="2026-09-05T06:00" '$0>=lo && $0<hi'); do
  M=$("$AWS" s3 cp "s3://${BUCKET}/projection/${v}/_build_manifest.json" - 2>/dev/null)
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
PREV_EVENING=$(printf '%s\n' "$VLIST" | awk -v lo="2026-09-04T21:00" '$0<lo' | sort | tail -1)
echo
echo "NIGHT_VINTAGE=${NIGHT_VINTAGE}"
echo "NIGHT_WRITER=${NIGHT_WRITER:-} NIGHT_MODE=${NIGHT_MODE:-} NIGHT_BUILT_AT=${NIGHT_BUILT:-}"
echo "PREV_EVENING=${PREV_EVENING}"
if [ "$NIGHT_VINTAGE" \> "$PREV_EVENING" ]; then echo "NIGHT_LATER_THAN_PREV_EVENING=true"; else echo "NIGHT_LATER_THAN_PREV_EVENING=false"; fi
echo

# ------------------------------------------------- 4. arm (a): the seat invocation census
echo "--- 4. arm (a) seat invocation census -- org/mcp/agent_telemetry"
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
print("  The order's arm-(a) filter ('rows naming kuzu|derive|projection|globgrph|run-task')")
print("  is therefore UNSATISFIABLE ON THIS LOG: such a regex reads 0 for a STRUCTURAL reason")
print("  (the field does not exist), not because no seat touched the graph -- a vacuous zero.")
print("  The honest arm at the grain the log DOES carry: was any seat invoking anything at all.")
print("  -- seats active in the window:")
for k, v in bys.most_common():
    print("       %-32s %d tool call(s)" % (k, v))
print("SEAT_INVOCATIONS_IN_WINDOW=%d of %d" % (tot, tot))
PYEOF
fi
echo

# ------------------------------------------------- 5. arm (b): the CloudTrail RunTask census
echo "--- 5. arm (b) CloudTrail RunTask census in the window"
CT=$("$AWS" cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=RunTask \
      --start-time "$LO" --end-time "$HI" --max-results 50 \
      --query 'Events[].CloudTrailEvent' --output text | tr '\t' '\n')
ROWS=$(printf '%s\n' "$CT" | "$JQ" -r '[.eventTime,(.userIdentity.type),(.userIdentity.arn//"-"),(.requestParameters.cluster//"-"),(.requestParameters.taskDefinition//"-"),(.requestParameters.startedBy//"-")]|@tsv')
RT_TOTAL=$(printf '%s\n' "$ROWS" | grep -c . )
echo "  eventTime            type        principal / cluster / taskDefinition / startedBy"
# The order's rule: "every RunTask's userIdentity must be the Pipe's role or the EventBridge
# scheduler's, never a human/seat principal." Classify on BOTH the identity type and the
# startedBy provenance -- a service role alone is not enough, and a bare role-name allow-list
# lapses silently when a new scheduler is added (globgrph-cse-producer-scheduler was, tonight).
# ONE classifier does both the labelling and the count: two classifiers drift and disagree.
CLASSIFY='function verdict(ty,by) {
  if (ty=="AssumedRole") {
    if (by=="Started by Eventbridge Pipes") return "PIPE";
    if (by ~ /^events-rule\//) return "SCHEDULER";
    if (by ~ /^chronos-schedule\//) return "SCHEDULER";
    if (by ~ /^ecs-svc\//) return "SCHEDULER";
  }
  return "NONPIPE";
}'
printf '%s\n' "$ROWS" | awk -F'\t' "$CLASSIFY"'
  NF>1 { printf "  %-9s %s  %s  %s  cluster=%s  td=%s  startedBy=%s\n", verdict($2,$6), $1, $2, $3, $4, $5, $6 }'
RT_TOTAL=$(printf '%s\n' "$ROWS" | awk -F'\t' 'NF>1' | grep -c .)
RT_NONPIPE=$(printf '%s\n' "$ROWS" | awk -F'\t' "$CLASSIFY"'
  NF>1 && verdict($2,$6)=="NONPIPE"' | grep -c .)
echo "RUNTASK_NONPIPE_IN_WINDOW=${RT_NONPIPE} of ${RT_TOTAL}"
echo
echo "--- the nightly's own RunTask attribution (startedBy, recovered from CloudTrail"
echo "    because ECS describe-tasks has aged the task out):"
printf '%s\n' "$ROWS" | grep 'derive-runner-events' | sed 's/^/  /'
