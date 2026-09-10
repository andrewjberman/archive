#!/usr/bin/env bash
# TO-CG-F-2 -- ONE ASK AT ONE FIXED UTC INSTANT (the laptop half).
#
# usage: bash f2_ask_at.sh <label> <instant-iso-Z>
#   e.g. bash f2_ask_at.sh T0 2026-09-09T19:00:00Z
#
# THE SHAPE, taken from D-8's two_machines.sh (the SURFACES grant): the laptop
# asks through .tools/comp-kuzu --json, which POSTs ONE statement to the public
# gateway with a Secrets-Manager bearer and prints its VINTAGE line on STDERR.
# No local database is created, opened or downloaded; nothing is written to S3.
#
# THE WAIT IS POLLED, NEVER A BARE SLEEP: a while-loop on date -u +%s with a 5 s
# tick, printing the clock every 60 s. If the instant has already passed when
# this runs, the script prints MISSED with both clocks and exits 3 WITHOUT
# asking -- a late ask is not the ask the criterion is about.
#
# NO RETRY INSIDE AN INSTANT: one ask, recorded whole whatever it returns.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PY=${PYTHON:-python}
GATEWAY=https://mcp.opalinvest.dev/graph/cypher
CYPHER="MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t"

LABEL=$1
INSTANT_ISO=$2
INSTANT_EPOCH=$("$PY" -c "import datetime,sys;print(int(datetime.datetime.strptime(sys.argv[1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()))" "$INSTANT_ISO")

stamp() { "$PY" -c "import datetime;n=datetime.datetime.now(datetime.timezone.utc);print(n.strftime('%Y-%m-%dT%H:%M:%S.')+('%03d'%(n.microsecond//1000))+'Z')"; }
epochf() { "$PY" -c "import time;print(repr(time.time()))"; }

echo "=== f2_ask_at.sh $LABEL -- target instant $INSTANT_ISO (epoch $INSTANT_EPOCH) ==="
echo "QUESTION=$CYPHER"
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "SCRIPT_ENTERED_AT=$(stamp)"

NOW=$(date -u +%s)
if [ "$NOW" -ge "$INSTANT_EPOCH" ]; then
  echo "LAPTOP_STATUS_$LABEL=MISSED"
  echo "LAPTOP_MISSED_$LABEL=true  instant=$INSTANT_ISO  clock_now=$(stamp)  seconds_late=$((NOW - INSTANT_EPOCH))"
  echo "NO ASK WAS FIRED for $LABEL. A late ask is not the ask F2-AC1 measures, and this line is printed rather than the instant omitted."
  exit 3
fi

# ---- the polled wait --------------------------------------------------------
LAST_PRINT=0
while :; do
  NOW=$(date -u +%s)
  [ "$NOW" -ge "$INSTANT_EPOCH" ] && break
  REMAIN=$((INSTANT_EPOCH - NOW))
  if [ $((NOW - LAST_PRINT)) -ge 60 ]; then
    echo "  waiting: clock=$(date -u +%Y-%m-%dT%H:%M:%SZ) remaining=${REMAIN}s"
    LAST_PRINT=$NOW
  fi
  if [ "$REMAIN" -le 5 ]; then sleep 1; else sleep 5; fi
done

# ---- the ask ----------------------------------------------------------------
T_START=$(stamp)
T_START_E=$(epochf)
echo "LAPTOP_START_$LABEL=$T_START"
timeout 120 bash .tools/comp-kuzu --json "$CYPHER" \
  > "$D/f2_answer_$LABEL.json" 2> "$D/f2_answer_$LABEL.err"
ASK_RC=$?
T_END=$(stamp)
T_END_E=$(epochf)
echo "LAPTOP_END_$LABEL=$T_END"
echo "LAPTOP_ASK_RC_$LABEL=$ASK_RC"

# ---- the gateway's Date header: the SHARED clock reference ------------------
# Both seats read the Date header of the SAME server, so neither has to trust
# the other's clock and no handshake is needed. Local time is stamped
# immediately BEFORE the header request so the skew is not inflated by RTT on
# the local side.
LOCAL_BEFORE_HDR=$(epochf)
curl -sS -o /dev/null -D "$D/f2_gwhdr_$LABEL.txt" -X GET --max-time 30 "$GATEWAY"
HDR_RC=$?
LOCAL_AFTER_HDR=$(epochf)
echo "GATEWAY_HEADER_RC_$LABEL=$HDR_RC"

# ---- the printed record -----------------------------------------------------
"$PY" - "$LABEL" "$INSTANT_ISO" "$INSTANT_EPOCH" "$T_START" "$T_START_E" "$T_END" "$T_END_E" \
      "$D/f2_answer_$LABEL.json" "$D/f2_answer_$LABEL.err" "$D/f2_gwhdr_$LABEL.txt" \
      "$LOCAL_BEFORE_HDR" "$LOCAL_AFTER_HDR" <<'PY'
import email.utils
import hashlib
import io
import json
import re
import sys

(label, instant_iso, instant_epoch, t_start, t_start_e, t_end, t_end_e,
 ans_p, err_p, hdr_p, loc_before, loc_after) = sys.argv[1:13]

instant_epoch = float(instant_epoch)
offset = float(t_start_e) - instant_epoch
print("LAPTOP_OFFSET_S_%s=%.3f  (T_START - %s; F2-AC1 wants [0, 5))" % (label, offset, instant_iso))
print("LAPTOP_WINDOW_S_%s=%.3f  (T_END - T_START, one clock)" % (label, float(t_end_e) - float(t_start_e)))

err = io.open(err_p, encoding="utf-8", errors="replace").read()
m = re.search(r"vintage=([^\s\]]+)", err)
vintage = m.group(1) if m else "UNREAD"
print("LAPTOP_VINTAGE_%s=%s" % (label, vintage))

try:
    doc = json.load(io.open(ans_p, encoding="utf-8"))
except Exception as ex:
    print("LAPTOP_ANSWER_PARSE_%s=FAILED (%s)" % (label, ex))
    print("LAPTOP_ROWS_COUNT_%s=UNREAD" % label)
    print("LAPTOP_ROWS_SHA256_%s=UNREAD" % label)
    doc = None

if doc is not None:
    rows = doc.get("rows") if isinstance(doc, dict) else doc
    if rows is None:
        rows = []
    canon = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    print("LAPTOP_ANSWER_PARSE_%s=OK" % label)
    print("LAPTOP_ROWS_COUNT_%s=%d" % (label, len(rows)))
    print("LAPTOP_ROWS_SHA256_%s=%s"
          % (label, hashlib.sha256(canon.encode("utf-8")).hexdigest()))
    print("LAPTOP_ROWS_CANON_BYTES_%s=%d" % (label, len(canon)))

hdr = io.open(hdr_p, encoding="utf-8", errors="replace").read()
dm = re.search(r"^Date:\s*(.+?)\s*$", hdr, re.M | re.I)
if dm:
    gw_epoch = email.utils.parsedate_to_datetime(dm.group(1)).timestamp()
    mid = (float(loc_before) + float(loc_after)) / 2.0
    print("GATEWAY_DATE_%s=%s" % (label, dm.group(1)))
    print("LAPTOP_SKEW_S_%s=%.3f  (local midpoint of the header request minus the gateway Date; the header has 1 s resolution, so +/-0.5 s is floor noise)"
          % (label, mid - gw_epoch))
    print("SKEW_SOURCE=gateway Date header")
else:
    print("GATEWAY_DATE_%s=UNREAD" % label)
    print("LAPTOP_SKEW_S_%s=UNREAD" % label)
    print("SKEW_SOURCE=gateway Date header (NOT READ at this instant)")
print("LAPTOP_STATUS_%s=ASKED" % label)
PY
echo "=== f2_ask_at.sh $LABEL END ==="
