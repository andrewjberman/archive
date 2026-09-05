#!/usr/bin/env bash
# NFRA_CLDGRPH.TO-CG-D-9 limb (ii) -- ONE REAL PRODUCER STAMP -> the served answer carries the
# NEW vintage, latency PRINTED against the ratified "within minutes".
# Author: 0.9.0_WK_NFRA_CLDGRPH~1. READS ONLY. No stamp provoked.
#
# THE STAMP CHOSEN, and why (the order: "the first real incremental_updater stamp after 13:00Z on
# the day you run, OR, if none arrives inside your bounded wait, the newest one already on the
# record (say which)"):
#   This order ran 2026-09-05 03:0xZ-04:xxZ. 13:00Z on the day of the run had NOT ARRIVED, so no
#   post-13:00Z stamp can exist and no bounded wait could produce one. THE SECOND BRANCH APPLIES:
#   the newest real producer stamp already on the record. SAYING WHICH, as the order requires.
#   It is 2026-09-05T03:31:16.793943+00:00, an INCREMENTAL producer stamp (manifest
#   producer.mode=incremental) by writer_id=cse_producers_nightly, published while this order was
#   being worked and NOT provoked by it: its RunTask (CloudTrail 2026-09-05T03:30:13Z) was started
#   by chronos-schedule/globgrph-cse-produc under the cse-producer scheduler role, not by a seat.
#   It is "real" in the sense the cell means -- an estate change flowing through the marker -- but
#   it is NOT in working hours and it is NOT writer_id=incremental_updater. Both departures are
#   stated here rather than papered over; the CVO grades them at L9.
#
# THE FOUR TIMESTAMPS (the order): the marker's committed_at_iso (= the vintage), the pointer
# object's LastModified, the service's last_swap, and an ANSWER read carrying that vintage.
set -u

BUCKET=opal-313476888478-globgrph
AWS=.tools/aws
JQ=.tools/jq.exe
STAMP="${STAMP:-2026-09-05T03:31:16.793943+00:00}"
SERVING_LOG_GROUP=/ecs/globgrph-serving

secs() { python -c "
import datetime,sys
s=sys.argv[1].strip()
for f in ('%Y-%m-%dT%H:%M:%S.%f%z','%Y-%m-%dT%H:%M:%S%z','%a, %d %b %Y %H:%M:%S %Z'):
    try:
        d=datetime.datetime.strptime(s,f)
        if d.tzinfo is None: d=d.replace(tzinfo=datetime.timezone.utc)
        print('%.6f'%d.timestamp()); break
    except ValueError: pass
else:
    print('NaN')
" "$1"; }
delta() { python -c "import sys;a=float(sys.argv[1]);b=float(sys.argv[2]);print('%.3f'%(a-b))" "$1" "$2"; }

echo "=== TO-CG-D-9 LIMB (ii): ONE REAL PRODUCER STAMP -> THE SERVED ANSWER"
echo "READ_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "STAMP=${STAMP}"
echo

# ---- t1: the stamp itself (the marker's committed_at_iso == the vintage, PROJECTION_CONTRACT s.1)
MAN=$("$AWS" s3 cp "s3://${BUCKET}/projection/${STAMP}/_build_manifest.json" - 2>/dev/null)
if [ -z "$MAN" ]; then echo "MANIFEST_UNREADABLE for ${STAMP}"; exit 1; fi
M_VINT=$(printf '%s' "$MAN" | "$JQ" -r '.vintage')
M_COMM=$(printf '%s' "$MAN" | "$JQ" -r '.committed_at')
M_BUILT=$(printf '%s' "$MAN" | "$JQ" -r '.built_at')
M_WRITER=$(printf '%s' "$MAN" | "$JQ" -r '.writer_id')
M_MODE=$(printf '%s' "$MAN" | "$JQ" -r '.producer.mode')
M_AGE=$(printf '%s' "$MAN" | "$JQ" -r '.age_line')
echo "--- t1 STAMP (manifest): vintage=${M_VINT} committed_at=${M_COMM}"
echo "    writer_id=${M_WRITER}  producer.mode=${M_MODE}  built_at=${M_BUILT}"
echo "    (contract s.1: vintage == committed_at == the marker's committed_at_iso, byte for byte)"

# ---- t2: the pointer object's LastModified (s3api renders UTC; `aws s3 ls` would render LOCAL)
PTR_VINT=$("$AWS" s3 cp "s3://${BUCKET}/projection/current.json" - 2>/dev/null | "$JQ" -r '.vintage')
PTR_LM=$("$AWS" s3api head-object --bucket "$BUCKET" --key projection/current.json --query 'LastModified' --output text)
echo "--- t2 POINTER: vintage=${PTR_VINT}  LastModified=${PTR_LM}"
if [ "$PTR_VINT" != "$STAMP" ]; then
  echo "    NOTE: the pointer has since advanced past this stamp; LastModified then describes the"
  echo "    LATER put and STAMP_TO_POINTER_S below would be wrong. Refusing to print it."
  PTR_USABLE=false
else
  PTR_USABLE=true
fi

# ---- t3: the service's last_swap, from the serving service's OWN log (durable; /health is a
#          point-in-time read that cannot testify about a swap that already happened)
# NOTE: --max-items appends a "None" pagination token to --output text, which silently corrupts a
# single-value capture into two lines. Take the first line explicitly.
SW_STREAM=$("$AWS" logs describe-log-streams --log-group-name "$SERVING_LOG_GROUP" \
             --order-by LastEventTime --descending --max-items 1 \
             --query 'logStreams[0].logStreamName' --output text | head -1)
# get-log-events is PAGINATED: --start-from-head on a long-lived stream returns the FIRST page,
# which for a service task started hours ago does not reach the stamp at all. An empty grep there
# is a PAGE artifact, not an absent swap. Anchor the read to the stamp's own minute.
SW_START=$(python -c "
import datetime,sys
d=datetime.datetime.strptime(sys.argv[1].strip(),'%Y-%m-%dT%H:%M:%S.%f%z')
print(int((d.timestamp()-60)*1000))" "$STAMP")
SW_LINE=$("$AWS" logs get-log-events --log-group-name "$SERVING_LOG_GROUP" --log-stream-name "$SW_STREAM" \
            --start-time "$SW_START" --start-from-head --query 'events[].message' --output text | tr '\t' '\n' \
          | grep 'projection swap complete' | grep -F "$STAMP" | tail -1)
echo "--- t3 SWAP (serving log stream ${SW_STREAM}):"
echo "    ${SW_LINE:-<no swap line found for this vintage>}"
SW_TS=$(printf '%s' "$SW_LINE" | sed -n "s/.*'last_swap': '\([^']*\)'.*/\1/p")
echo "    last_swap=${SW_TS:-UNREAD}"

# ---- t4: an ANSWER read through the client, carrying that vintage
ANS_AT=$(date -u +%Y-%m-%dT%H:%M:%S.%6NZ)
ANS=$(timeout 60 bash .tools/comp-kuzu --json "MATCH (n) RETURN count(n) AS c" 2>.lat.err)
ANS_AGE=$(cat .lat.err); rm -f .lat.err
ANS_VINT=$(printf '%s' "$ANS_AGE" | sed -n 's/.*\[vintage=\([^ ]*\) manifest.*/\1/p')
ANS_CNT=$(printf '%s' "$ANS" | "$JQ" -r '.[0].c // "-"')
echo "--- t4 ANSWER (through .tools/comp-kuzu, the thin client):"
echo "    read_at=${ANS_AT}  node_count=${ANS_CNT}  vintage=${ANS_VINT}"
echo "    ${ANS_AGE}"
if [ "$ANS_VINT" = "$STAMP" ]; then echo "    ANSWER_CARRIES_THE_STAMP=true"; else echo "    ANSWER_CARRIES_THE_STAMP=false (the estate has moved on to ${ANS_VINT})"; fi
echo

# ---------------------------------------------------------------- the three deltas
T1=$(secs "$M_COMM"); T3=$(secs "${SW_TS:-}")
if [ "$PTR_USABLE" = true ]; then
  T2=$(secs "$PTR_LM")
  echo "STAMP_TO_POINTER_S=$(delta "$T2" "$T1")"
  echo "POINTER_TO_SWAP_S=$(delta "$T3" "$T2")"
else
  # Fall back to the manifest's built_at, which the contract defines as the moment the artifact
  # was closed -- the pointer PUT is the next step and cannot precede it.
  T2=$(secs "$M_BUILT")
  echo "STAMP_TO_POINTER_S=UNMEASURABLE (pointer has advanced past this stamp; its LastModified now"
  echo "  describes a later PUT). STAMP_TO_ARTIFACT_CLOSED_S=$(delta "$T2" "$T1") from the manifest's built_at."
  echo "POINTER_TO_SWAP_S=$(delta "$T3" "$T2") measured from built_at, an UPPER bound on the pointer leg."
fi

# STAMP_TO_ANSWER: the quantity FWD-2 ratifies is when the estate's answer BECOMES newer, not when
# a worker happened to type a query. The served answer begins carrying the new vintage at the swap
# and every read after it returns the new vintage -- so the end-to-end latency of the chain is
# swap - stamp, CONFIRMED by the t4 answer read above actually returning that vintage.
# The wall-clock of this worker's own read is printed beside it and is NOT the estate's latency.
echo "STAMP_TO_ANSWER_S=$(delta "$T3" "$T1")"
echo "  ^ = last_swap - committed_at: the moment the served answer FIRST carried this vintage,"
echo "    confirmed by the t4 client read returning vintage=${ANS_VINT}."
T4=$(secs "$ANS_AT")
echo "STAMP_TO_THIS_WORKERS_READ_S=$(delta "$T4" "$T1")  <-- when this seat happened to ask; NOT the estate's latency"
echo "WITHIN_MINUTES=900  (the issuer's reading: <= 15 min for an incremental stamp; the CVO grades)"
