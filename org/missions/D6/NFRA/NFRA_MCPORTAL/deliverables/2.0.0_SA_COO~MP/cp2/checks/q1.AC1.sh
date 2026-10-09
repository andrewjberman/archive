#!/usr/bin/env bash
# MP-q-1 AC1 (A17, read on the server and in the store): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~12/q1_run.json ({"t0","t1","box","call_id","request_id","overlap_surface","gitstate_box"})
# names one close. Inside [t0,t1] the gateway's own access log holds >=1 "POST /api/admin/fabric/calls/close" answered 202
# (only the verified owner reaches 202); the store's result object box=<box>/request_results/<request_id>.json reads state
# APPLIED; and that box's open_calls.json shows call_id with state CLOSED.
. "$(dirname "$0")/_root.sh"
CK=org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/checks
RUN="${MP_Q1_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~12/q1_run.json}"
read -r T0 T1 BOX CID RID < <(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['t0'],d['t1'],d['box'],d['call_id'],d['request_id'])" "$RUN" 2>/dev/null | tr -d '\r')
[ -n "$RID" ] || { echo "no run: $RUN missing or unreadable"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_q1_$$"; mkdir -p "$T"
python "$CK/_q1_probe.py" "$T/params.json" "$T0" "$T1"
ssm_run "$T/params.json"
n=$(printf '%s\n' "$SSM_OUT" | tail -1 | tr -dc '0-9')
K="s3://opal-313476888478-globgrph/fabric/open-calls/v1/box=$BOX"
"$AWS" s3 cp "$K/request_results/$RID.json" "$T/res.json" --only-show-errors 2>&1 | tail -1
"$AWS" s3 cp "$K/open_calls.json" "$T/oc.json" --only-show-errors 2>&1 | tail -1
read -r RST CST < <(python -c "
import json, sys
try:
    r = json.load(open(sys.argv[1], encoding='utf-8')).get('state', '?')
except Exception as e:
    r = 'UNREAD:' + type(e).__name__
try:
    c = [x.get('state') for x in json.load(open(sys.argv[2], encoding='utf-8'))['rows'] if x.get('id') == sys.argv[3]]
    c = c[0] if c else 'ABSENT'
except Exception as e:
    c = 'UNREAD:' + type(e).__name__
print(r, c)" "$T/res.json" "$T/oc.json" "$CID" | tr -d '\r')
rm -rf "$T"
echo "window $T0 .. $T1; ssm status=$SSM_ST; close POST 202s in window=${n:-?}; result $RID state=$RST; call $CID on $BOX state=$CST"
if [ "$SSM_ST" = Success ] && [ "${n:-0}" -ge 1 ] && [ "$RST" = APPLIED ] && [ "$CST" = CLOSED ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
