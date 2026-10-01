#!/usr/bin/env bash
# MS-rn-1 AC1 (the run is stored where the builder says): deliverables/0.9.0_WK_NFRA_MCPMSP~6/r2_e4r_run.json names
# {firm, run_id, date}; under address('gateway', firm, 'bronze', 'msp_runs', date)/<run_id>/ the three objects
# transcript.jsonl, audit.jsonl and manifest.json exist in S3; manifest.json's firm and run_id equal the run file's, and
# transcript.jsonl holds >= 1 user turn.
. "$(dirname "$0")/_root.sh"
RUN="$R2/0.9.0_WK_NFRA_MCPMSP~6/r2_e4r_run.json"
[ -f "$RUN" ] || { echo "$RUN absent (no run shipped)"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_e4r.XXXXXX")"
base=$(python -c "
import json,sys;sys.path.insert(0,'.');import lib.opal_naming as n
r=json.load(open(sys.argv[1],encoding='utf-8'))
print(n.address('gateway', r['firm'], 'bronze', 'msp_runs', r['date']) + '/' + r['run_id'])
" "$RUN" 2>&1 | tr -d '\r' | tail -1)
for o in transcript.jsonl audit.jsonl manifest.json; do timeout 60 "$AWS" s3 cp "$base/$o" "$(native "$T/$o")" >/dev/null 2>&1; done
res=$(python - "$RUN" "$T" <<'EOF' 2>&1 | tr -d '\r'
import json, os, sys
r = json.load(open(sys.argv[1], encoding='utf-8')); T = sys.argv[2]
have = [o for o in ('transcript.jsonl', 'audit.jsonl', 'manifest.json') if os.path.exists(os.path.join(T, o))]
m = {}
try:
    m = json.load(open(os.path.join(T, 'manifest.json'), encoding='utf-8'))
except Exception:
    pass
users = 0
try:
    for l in open(os.path.join(T, 'transcript.jsonl'), encoding='utf-8'):
        try:
            d = json.loads(l)
        except Exception:
            continue
        if d.get('type') == 'user' or (d.get('message') or {}).get('role') == 'user':
            users += 1
except Exception:
    pass
ok = len(have) == 3 and m.get('firm') == r.get('firm') and m.get('run_id') == r.get('run_id') and users >= 1
print('objects=%d/3 manifest_firm=%s run_id_match=%s user_turns=%d verdict=%s' % (len(have), m.get('firm'), m.get('run_id') == r.get('run_id'), users, 'OK' if ok else 'NO'))
EOF
)
rm -rf "$T"
echo "record base=$base; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
