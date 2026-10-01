#!/usr/bin/env bash
# MS-dn-1 AC3 (DELTA=0 on the served answers, read on the HOST through the gateway's own code, controlled against the
# SOURCE at the same moment): for every key in MS-c-1's baseline
# (deliverables/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json), the host's app.query_v0._fetch_capped(key) -- run over
# SSM with the service's venv and its .env parsed as KEY=VALUE in Python (the file cannot be shell-sourced: row
# Z-W1-S9), i.e. the opal-internal path that now goes through the internal reader role -- returns bytes whose sha256
# equals the sha256 of the same object read directly from S3 by this check in the same minute. Same-moment source, not
# the baseline's hash: the producers rewrite these objects daily, so a baseline hash differs by a day's data (Z-W1-S9).
# Prints n matched of n; any key the host could not read (ERR:...) is a mismatch.
. "$(dirname "$0")/_root.sh"
F="$R2/0.9.0_WK_NFRA_MCPMSP~1/r2_c1_delta_baseline.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_dn1_ac3.XXXXXX")"
python - "$F" "$T/params.json" <<'EOF'
import json, sys
keys = [k['key'] for k in json.load(open(sys.argv[1], encoding='utf-8')).get('keys') or []]
py = ("import hashlib,json,os,sys\n"
      "for l in open('/opt/opal-gateway/.env',encoding='utf-8'):\n"
      "  l=l.strip()\n"
      "  if l and not l.startswith('#') and '=' in l:\n"
      "    k,v=l.split('=',1); os.environ.setdefault(k.strip(),v.strip())\n"
      "sys.path.insert(0,'/opt/opal-gateway');from app import query_v0 as q\n"
      "ks=json.loads(sys.argv[1]);out={}\n"
      "for k in ks:\n"
      "  try:\n"
      "    b,n=q._fetch_capped(k); out[k]=hashlib.sha256(b).hexdigest()\n"
      "  except Exception as e: out[k]='ERR:'+type(e).__name__\n"
      "print('DELTA_JSON='+json.dumps(out))")
import base64, shlex
b64 = base64.b64encode(py.encode('utf-8')).decode('ascii')
cmd = ("cd /opt/opal-gateway && sudo -u ec2-user .venv/bin/python -c %s %s"
       % (shlex.quote("import base64;exec(base64.b64decode('%s').decode('utf-8'))" % b64), shlex.quote(json.dumps(keys))))
json.dump({"commands": [cmd]}, open(sys.argv[2], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"
printf '%s\n' "$SSM_OUT" | sed -n 's/^DELTA_JSON=//p' > "$T/live.json"
keys=$(python -c "import json,sys;print('\n'.join(k['key'] for k in json.load(open(sys.argv[1],encoding='utf-8')).get('keys') or []))" "$F" | tr -d '\r')
i=0; : > "$T/src.tsv"
for k in $keys; do i=$((i+1)); timeout 60 "$AWS" s3api get-object --bucket opal-data-portal-v2 --key "$k" "$(native "$T/s$i")" >/dev/null 2>&1; printf '%s\t%s\n' "$k" "$(native "$T/s$i")" >> "$T/src.tsv"; done
res=$(python - "$(native "$T/src.tsv")" "$(native "$T/live.json")" <<'EOF' 2>&1 | tr -d '\r'
import hashlib, json, os, sys
src = {}
for line in open(sys.argv[1], encoding='utf-8'):
    k, p = line.rstrip('\n').split('\t')
    src[k] = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None
try:
    live = json.load(open(sys.argv[2], encoding='utf-8'))
except Exception:
    live = {}
m = sum(1 for k, v in src.items() if v and live.get(k) == v)
bad = [(k, str(live.get(k))[:12]) for k, v in src.items() if not v or live.get(k) != v][:4]
print('matched=%d of %d mismatched=%s verdict=%s' % (m, len(src), bad, 'OK' if src and m == len(src) else 'NO'))
EOF
)
rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
