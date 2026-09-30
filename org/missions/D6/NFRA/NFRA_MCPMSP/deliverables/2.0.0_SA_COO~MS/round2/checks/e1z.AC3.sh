#!/usr/bin/env bash
# MS-dn-1 AC3 (DELTA=0 on the served answers, read on the HOST through the gateway's own code): for every key in
# MS-c-1's baseline (deliverables/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json), the host's
# app.query_v0._fetch_capped(key) -- run over SSM with the service's venv and .env, i.e. the opal-internal path that now
# goes through the internal reader role -- returns bytes whose sha256 equals the baseline's. Prints n matched of n.
. "$(dirname "$0")/_root.sh"
F="$R2/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_e1z_ac3.XXXXXX")"
python - "$F" "$T/params.json" <<'EOF'
import json, sys
keys = [k['key'] for k in json.load(open(sys.argv[1], encoding='utf-8')).get('keys') or []]
py = ("import hashlib,json,sys;sys.path.insert(0,'/opt/opal-gateway');from app import query_v0 as q;"
      "ks=json.loads(sys.argv[1]);out={}\n"
      "for k in ks:\n"
      "  try:\n"
      "    b,n=q._fetch_capped(k); out[k]=hashlib.sha256(b).hexdigest()\n"
      "  except Exception as e: out[k]='ERR:'+type(e).__name__\n"
      "print('DELTA_JSON='+json.dumps(out))")
cmd = ("cd /opt/opal-gateway && set -a && . ./.env && set +a && sudo -E -u ec2-user .venv/bin/python -c %s %s"
       % (json.dumps(py), json.dumps(json.dumps(keys))))
json.dump({"commands": [cmd]}, open(sys.argv[2], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"
printf '%s\n' "$SSM_OUT" | sed -n 's/^DELTA_JSON=//p' > "$T/live.json"
res=$(python - "$F" "$T/live.json" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
base = {k['key']: k['sha256'] for k in json.load(open(sys.argv[1], encoding='utf-8')).get('keys') or []}
try:
    live = json.load(open(sys.argv[2], encoding='utf-8'))
except Exception:
    live = {}
m = sum(1 for k, v in base.items() if live.get(k) == v)
bad = [k for k, v in base.items() if live.get(k) != v][:4]
print('matched=%d of %d mismatched=%s verdict=%s' % (m, len(base), bad, 'OK' if base and m == len(base) else 'NO'))
EOF
)
rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
