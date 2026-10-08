set -u
# Ledger irpt-ycdgen-f1-svc-20261008 leg F1, condition 4 (CTO ruling d54e0b7515): count YCharts calls in the F1 run window from the
# resident's own journal. READ ONLY. The window and the request id are substituted before the send. Denominators printed.
SINCE='__SINCE__'
UNTIL='__UNTIL__'
REQ='__REQUEST_ID__'
UNIT=irpt-analysis-resident.service
J=$(journalctl -u $UNIT --since "$SINCE" --until "$UNTIL" --no-pager -o short-iso)
echo "F1Y window $SINCE .. $UNTIL; journal lines in window: $(printf '%s\n' "$J" | grep -c .)"
echo "F1Y lines naming the request id: $(printf '%s\n' "$J" | grep -c "$REQ")"
for m in IRPT_RESIDENT_VENDOR_REQUESTS IRPT_RESIDENT_STEP STEP_WAF_REFRESH READ_BACK_ IRPT_RESIDENT_RESOLVE IRPT_SESSION_ROTATION ycharts.com; do
  echo "F1Y marker $m: $(printf '%s\n' "$J" | grep -c "$m")"
done
echo "F1Y vendor-request counts reported in window:"
printf '%s\n' "$J" | grep -o 'IRPT_RESIDENT_VENDOR_REQUESTS[^ ]* kept=[0-9]*' | sort | uniq -c
echo "F1Y producer lines naming OPAL in window: $(printf '%s\n' "$J" | grep -c -i 'opal')"
echo "F1Y tracebacks in window: $(printf '%s\n' "$J" | grep -c Traceback)"
echo "F1Y positive control (polls in window): $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_POLL)"
