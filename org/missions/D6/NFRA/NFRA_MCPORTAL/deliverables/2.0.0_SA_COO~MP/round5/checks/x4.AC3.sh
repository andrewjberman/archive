#!/usr/bin/env bash
# MP-x-4 AC3 (SERVED, on the host, R-13): /health=200 (control); GET /api/admin/fabric/boxes with NO identity answers 401 or
# 403 (the owner gate covers the new route on the served code); and the served handler's own _compute(6), run from the
# host's venv under the instance role, returns >=1 reporting box from the LIVE store in at most 30 s cold.
. "$(dirname "$0")/_root.sh"
T="${TMPDIR:-/tmp}/mp_x4_ac3_$$"; mkdir -p "$T"
python - "$T/params.json" <<'EOF'
import json, sys
probe = ('cd /opt/opal-gateway && sudo -u ec2-user .venv/bin/python -c "'
         'import time;from app import admin_fabric as a;t=time.time();r=a._compute(6);'
         'print(\'compute_s=%.1f reporting=%d scanned=%d\' % (time.time()-t, sum(1 for b in r[\'boxes\'] if b[\'status\']==\'reporting\'), r[\'records_scanned\']))'
         '" 2>&1 | tail -1')
cmd = ('for p in /health /api/admin/fabric/boxes; do echo "$p=$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8080$p)"; done; '
       + probe)
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"; rm -rf "$T"
h=$(printf '%s\n' "$SSM_OUT" | sed -n 's#^/health=##p'); f=$(printf '%s\n' "$SSM_OUT" | sed -n 's#^/api/admin/fabric/boxes=##p')
c=$(printf '%s\n' "$SSM_OUT" | grep -m1 'compute_s=' || echo "compute: $(printf '%s\n' "$SSM_OUT" | tail -1)")
secs=$(printf '%s' "$c" | sed -n 's/.*compute_s=\([0-9.]*\).*/\1/p'); rep=$(printf '%s' "$c" | sed -n 's/.*reporting=\([0-9]*\).*/\1/p')
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$h; /api/admin/fabric/boxes (no identity)=$f; $c"
ok=$(python -c "import sys;s=sys.argv[1];r=sys.argv[2];print('yes' if s and r and float(s)<=30.0 and int(r)>=1 else 'no')" "$secs" "$rep")
if [ "$SSM_ST" = Success ] && [ "$h" = 200 ] && { [ "$f" = 401 ] || [ "$f" = 403 ]; } && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
