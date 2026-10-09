#!/usr/bin/env bash
# MP-x-5 AC1 (A14, the owner opened it, read on the server): inside the window recorded in
# deliverables/0.9.0_WK_NFRA_MCPORTAL~5/x5_run.json ({"t0","t1","box","projects":[...]}), the gateway's own access log
# holds >=1 "GET /api/admin/fabric/boxes" answered 200 (only the verified owner can get 200: owner_gate.py), and the
# run file names one box and >=1 project.
. "$(dirname "$0")/_root.sh"
RUN="${MP_X5_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~5/x5_run.json}"
read -r T0 T1 BOX NP < <(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['t0'],d['t1'],d.get('box','-'),len(d.get('projects') or []))" "$RUN" 2>/dev/null | tr -d '\r')
[ -n "$T0" ] || { echo "no window: $RUN missing or unreadable"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_x5_$$"; mkdir -p "$T"
python - "$T/params.json" "$T0" "$T1" <<'EOF'
import json, sys
since, until = sys.argv[2].replace('T', ' ').rstrip('Z'), sys.argv[3].replace('T', ' ').rstrip('Z')
cmd = ('TZ=UTC journalctl -u opal-gateway --no-pager -o cat --utc --since "%s" --until "%s" '
       '| grep -cE "\\"GET /api/admin/fabric/boxes(\\?[^ ]*)? HTTP/1.1\\" 200"') % (since, until)
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"; rm -rf "$T"
n=$(printf '%s\n' "$SSM_OUT" | tail -1 | tr -dc '0-9')
echo "window $T0 .. $T1; ssm status=$SSM_ST; fabric/boxes 200s in window=${n:-?}; run file box=$BOX projects named=$NP"
if [ "$SSM_ST" = Success ] && [ "${n:-0}" -ge 1 ] && [ "$BOX" != "-" ] && [ "${NP:-0}" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
