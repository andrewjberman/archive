#!/usr/bin/env bash
# MP-z-6 AC1 (FWD-20 DONE WHEN, read on the server and in the stores): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~16/z6_run.json carries {"t0","t1","channel","code_tools","page_tools",
# "principal","store_tools","page_holder_tools"}. Inside [t0,t1] the gateway's own access log holds >=1
# GET /api/admin/gateway/breakdown answered 200 and each of the Control Plane page's four data routes (fabric boxes, overlap, gitstate, calls) answered 200 (owner only; amended 2026-10-19, no direct /control-plane request exists: the page is opened by in-app navigation); the channel's
# tool list read from the deployed code equals the list read off the page; and the principal's tools read from the grant
# store (and the chain) equal the tools the page lists that principal holding.
. "$(dirname "$0")/_root.sh"
CK=org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/fwd20/checks
RUN="${MP_Z6_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~16/z6_run.json}"
read -r T0 T1 EQT EQP < <(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print(d['t0'], d['t1'],
      'yes' if d['code_tools'] and sorted(d['code_tools'])==sorted(d['page_tools']) else 'no',
      'yes' if d['store_tools'] and sorted(d['store_tools'])==sorted(d['page_holder_tools']) else 'no')" "$RUN" 2>/dev/null | tr -d '\r')
[ -n "$T1" ] || { echo "no run: $RUN missing or unreadable"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_z6_$$"; mkdir -p "$T"
python "$CK/_z6_probe.py" "$T/params.json" "$T0" "$T1"
ssm_run "$T/params.json"; rm -rf "$T"
b=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^breakdown_200=//p' | head -1); c=$(printf '%s\n' "$SSM_OUT" | sed -n 's/^control_plane_200=//p' | head -1)
echo "window $T0 .. $T1; ssm status=$SSM_ST; breakdown 200s=${b:-?}; control-plane data routes 200 (of 4)=${c:-?}; channel tools code==page: $EQT; principal tools store==page: $EQP"
if [ "$SSM_ST" = Success ] && [ "${b:-0}" -ge 1 ] && [ "${c:-0}" -ge 4 ] && [ "$EQT" = yes ] && [ "$EQP" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
